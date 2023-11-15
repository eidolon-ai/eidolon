import asyncio
from abc import ABC, abstractmethod
from typing import Any, List


class BusEvent:
    def __init__(self, thread_id: int, event_type: str, event_data: dict[str, Any]):
        self.thread_id = thread_id
        self.event_type = event_type
        self.event_data = event_data


class Bus:
    current_event: BusEvent


class BusParticipant(ABC):
    controller: 'BusController' = None

    def request_write(self, event: BusEvent):
        self.controller.request_write_access(self, event)

    @abstractmethod
    async def bus_read(self, bus: Bus):
        pass


class BusController:
    def __init__(self):
        self.stop = False
        self.bus = Bus()
        self.participants = []
        self.access_queue: List[(BusParticipant, BusEvent)] = []
        self.lock = asyncio.Event()

    async def start(self):
        asyncio.create_task(self.event_loop())

    def stop(self):
        self.stop = True
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

    async def event_loop(self):
        while not self.stop:
            self.lock.clear()
            while len(self.access_queue) > 0:
                _, event = self.access_queue.pop(0)
                self.bus.current_event = event
                # then we allow all participants to read from the bus. This will allow any participant to read from the bus and execute their logic
                for participant in self.participants:
                    asyncio.create_task(participant.bus_read(self.bus))
            self.bus.current_event = None
            await self.lock.wait()
