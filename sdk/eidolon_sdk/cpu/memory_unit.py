from abc import ABC

from pydantic import BaseModel, SerializeAsAny

from eidolon_sdk.cpu.agent_bus import BusParticipant, BusEvent
from eidolon_sdk.cpu.bus_messages import LLMEvent
from eidolon_sdk.cpu.llm_message import LLMMessage
from eidolon_sdk.reference_model import Specable


class MemoryUnitConfig(BaseModel):
    ms: str = 'llm.le'
    # msf: str  # input port doesn't need to define mapping


class MemoryUnit(BusParticipant, Specable[MemoryUnitConfig], ABC):
    def __init__(self, agent_machine: 'AgentMachine', spec: MemoryUnitConfig = None):
        self.agent_machine = agent_machine


class ConversationMemoryItem(BaseModel):
    process_id: str
    thread_id: int
    message: SerializeAsAny[LLMMessage]


class ConversationalMemoryUnit(MemoryUnit):
    async def bus_read(self, event: BusEvent):
        if event.message.event_type == "add_conversation_history":
            # lookup the conversation history in the machine memory and add it to the event data. Write a new "llm_event" event containing the updated event data.
            existingMessages = []
            async for message in self.agent_machine.agent_memory.symbolic_memory.find("conversation_memory", {
                "process_id": event.process_id,
                "thread_id": event.thread_id
            }):
                existingMessages.append(LLMMessage.model_validate(message["message"]))

            for message in event.message.messages:
                newMessage = ConversationMemoryItem(process_id=event.process_id, thread_id=event.thread_id, message=message)
                await self.agent_machine.agent_memory.symbolic_memory.insert_one("conversation_memory", newMessage.model_dump())
                existingMessages.append(newMessage.message)

            self.request_write(BusEvent(
                event.process_id,
                event.thread_id,
                LLMEvent(messages=existingMessages, output_format=event.message.output_format)
            ))
        elif event.message.event_type == "llm_response":
            # add the response message to the conversation history
            await self.agent_machine.agent_memory.symbolic_memory.insert_one("conversation_memory", ConversationMemoryItem(
                process_id=event.process_id,
                thread_id=event.thread_id,
                message=event.message.message
            ).model_dump())
