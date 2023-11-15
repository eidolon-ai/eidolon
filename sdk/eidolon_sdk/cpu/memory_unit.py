from abc import ABC
from typing import Any

from pydantic import BaseModel

from eidolon_sdk.agent_machine import AgentMachine
from eidolon_sdk.cpu.agent_bus import BusParticipant, Bus, BusEvent
from eidolon_sdk.cpu.llm_message import LLMMessage


class MemoryUnit(BusParticipant, ABC):

    def __init__(self, agent_machine: AgentMachine):
        self.agent_machine = agent_machine


class ConversationMemoryItem(BaseModel):
    process_id: str
    thread_id: int
    message: dict[str, Any]


class ConversationalMemoryUnit(MemoryUnit):
    async def bus_read(self, bus: Bus):
        if bus.current_event.event_type == "add_conversation_history":
            # lookup the conversation history in the machine memory and add it to the event data. Write a new "llm_event" event containing the updated event data.
            existingMessages = []
            async for message in self.agent_machine.agent_memory.find("conversation_memory", {
                "process_id": bus.current_event.process_id,
                "thread_id": bus.current_event.thread_id
            }):
                existingMessages.append(message["message"])
            newMessage = ConversationMemoryItem(process_id=bus.current_event.process_id, thread_id=bus.current_event.thread_id,
                                                message=bus.current_event.event_data["message"])
            print(bus.current_event.event_data["message"])
            print(newMessage.model_dump())
            await self.agent_machine.agent_memory.insert_one("conversation_memory", newMessage.model_dump())
            existingMessages.append(newMessage.message)
            self.request_write(BusEvent(
                bus.current_event.process_id,
                bus.current_event.thread_id,
                "llm_event", {
                    "messages": existingMessages
                }
            ))
        elif bus.current_event.event_type == "llm_response":
            # add the response message to the conversation history
            await self.agent_machine.agent_memory.insert_one("conversation_memory", ConversationMemoryItem(
                process_id=bus.current_event.process_id,
                thread_id=bus.current_event.thread_id,
                message=bus.current_event.event_data["message"]
            ).model_dump())
