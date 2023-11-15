from abc import ABC

from eidolon_sdk.cpu.agent_bus import BusParticipant, Bus, BusEvent


class ControlUnit(ABC, BusParticipant):
    pass


class ConversationalControlUnit(ControlUnit):
    async def bus_read(self, bus: Bus):
        if bus.current_event.event_type == "input_request":
            # send the event data to the llm
            await self.request_write(BusEvent(
                bus.current_event.process_id,
                bus.current_event.thread_id,
                "add_conversation_history", {
                    "messages": bus.current_event.event_data["messages"]
                }
            ))
        elif bus.current_event.event_type == "llm_response" and bus.current_event.thread_id == 0:
            # send the event data to the llm
            await self.request_write(BusEvent(
                bus.current_event.process_id,
                bus.current_event.thread_id,
                "output_response", {
                    "messages": bus.current_event.event_data["messages"]
                }
            ))