import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from eidolon_sdk.cpu.bus_messages import BusMessage


@dataclass
class BusEvent:
    process_id: str
    thread_id: int
    message: BusMessage


class Bus:
    current_event: BusEvent = None


class BusParticipant(ABC):
    controller: 'BusController' = None

    def __init__(self, controller: 'BusController'):
        self.controller = controller

    def request_write(self, event: BusEvent):
        self.controller.request_write_access(self, event)

    @abstractmethod
    async def bus_read(self, event: BusEvent):
        pass


class BusController:
    def __init__(self):
        self.in_event_loop = False
        self.is_stopped = True
        self.bus = Bus()
        self.participants = []
        self.access_queue: List[(BusParticipant, BusEvent)] = []
        self.lock = asyncio.Event()

    async def start(self):
        if self.is_stopped:
            self.is_stopped = False
            asyncio.create_task(self.event_loop())

    def stop(self):
        if not self.is_stopped:
            self.is_stopped = True
            self.lock.set()

    def add_participant(self, participant: BusParticipant):
        self.participants.append(participant)
        participant.controller = self

    def remove_participant(self, participant: BusParticipant):
        self.participants.remove(participant)
        participant.controller = None

    def request_write_access(self, participant: BusParticipant, event: BusEvent):
        self.access_queue.append((participant, event))
        self.lock.set()

    async def _process_one_event(self, should_run_async: bool = True):
        while not self.is_stopped and len(self.access_queue) > 0:
            _, event = self.access_queue.pop(0)
            self.bus.current_event = event
            # then we allow all participants to read from the bus. This will allow any participant to read from the bus and execute their logic
            for participant in self.participants:
                if should_run_async:
                    asyncio.create_task(participant.bus_read(event))
                else:
                    await participant.bus_read(event)
        self.bus.current_event = None

    async def event_loop(self):
        self.in_event_loop = True
        while not self.is_stopped:
            self.lock.clear()
            await self._process_one_event()
            await self.lock.wait()
        self.in_event_loop = False
