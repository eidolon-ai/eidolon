from abc import ABC

from eidolon_sdk.cpu.agent_bus import BusParticipant, Bus, BusEvent


class ControlUnit(ABC, BusParticipant):
    pass


class ConversationalControlUnit(ControlUnit):
    async def bus_read(self, bus: Bus):
        if bus.current_event.event_type == "input_request":
            # send the event data to the llm
            # todo -- piece together the template from the input and put a add_conversation_history event on the bus
            # well -- wait, how do I handle a response from the LLM to do the next thing?
            # Need to think about user interaction...
            # What about the final_answer tool or equiv here?
            await self.request_write(BusEvent(
                bus.current_event.process_id,
                bus.current_event.thread_id,
                "add_conversation_history", {
                    "messages": bus.current_event.event_data["messages"]
                }
            ))
