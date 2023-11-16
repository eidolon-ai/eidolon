from abc import ABC

from eidolon_sdk.cpu.agent_bus import BusParticipant, BusEvent
from eidolon_sdk.cpu.bus_messages import AddConversationHistory, OutputResponse


class ControlUnit(BusParticipant, ABC):
    pass


class ConversationalControlUnit(ControlUnit):
    async def bus_read(self, event: BusEvent):
        if event.message.event_type == "input_request":
            # send the event data to the llm
            self.request_write(BusEvent(
                event.process_id,
                event.thread_id,
                AddConversationHistory(messages = event.message.messages, output_format = event.message.output_format)
            ))
        elif event.message.event_type == "llm_response" and event.thread_id == 0:
            # send the event data to the llm
            self.request_write(BusEvent(
                event.process_id,
                event.thread_id,
                OutputResponse(response = event.message.message.content)
            ))
