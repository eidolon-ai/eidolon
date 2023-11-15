from unittest.mock import MagicMock

import pytest

from eidolon_sdk.cpu.agent_bus import BusParticipant, Bus, BusEvent, BusController


# Assuming the provided classes are in a module named 'bus_system', which needs to be imported here.
# from bus_system import BusEvent, Bus, BusParticipant, BusController

# Mocking the abstract BusParticipant for testing purposes
class MockBusParticipant(BusParticipant):
    def __init__(self):
        self.read_events = []

    async def bus_read(self, bus: Bus):
        self.read_events.append(bus.current_event)


@pytest.fixture
def bus_event():
    return BusEvent(process_id="process1", thread_id=1, event_type="test_event", event_data={"key": "value"})


@pytest.fixture
def bus_controller():
    return BusController()


def make_bus_participant(bus_controller):
    participant = MockBusParticipant()
    participant.controller = bus_controller
    return participant


@pytest.mark.asyncio
class TestBusSystem:
    async def test_request_write(self, bus_controller, bus_event):
        bus_participant = make_bus_participant(bus_controller)
        bus_controller.request_write_access = MagicMock()
        bus_participant.request_write(bus_event)
        bus_controller.request_write_access.assert_called_once_with(bus_participant, bus_event)

    async def test_add_remove_participant(self, bus_controller):
        bus_participant = make_bus_participant(bus_controller)
        bus_controller.add_participant(bus_participant)
        assert bus_participant in bus_controller.participants
        assert bus_participant.controller == bus_controller

        bus_controller.remove_participant(bus_participant)
        assert bus_participant not in bus_controller.participants
        assert bus_participant.controller is None

    async def test_event_loop_single_participant(self, bus_controller, bus_event):
        bus_participant = make_bus_participant(bus_controller)
        bus_controller.add_participant(bus_participant)
        await bus_controller.start()

        bus_participant.request_write(bus_event)

        await bus_controller._process_one_event(False)

        assert bus_participant.read_events == [bus_event]
        assert bus_controller.bus.current_event is None

    async def test_event_write_is_read_by_multiple_participants(self, bus_controller, bus_event):
        # Create multiple participants and add them to the controller
        participants = [make_bus_participant(bus_controller) for _ in range(3)]
        for participant in participants:
            bus_controller.add_participant(participant)

        await bus_controller.start()

        # Write an event as one of the participants
        participants[0].request_write(bus_event)

        # Process the events
        await bus_controller._process_one_event(False)

        # Check that all participants have read the event
        for participant in participants:
            assert bus_event in participant.read_events

    async def test_multiple_writes_are_read_in_order(self, bus_controller, bus_event):
        # Create multiple participants and add them to the controller
        participants = [make_bus_participant(bus_controller) for _ in range(3)]
        for participant in participants:
            bus_controller.add_participant(participant)

        await bus_controller.start()

        # First write
        first_event = BusEvent("process1", 1, "test_event1", {"key": "value1"})
        participants[0].request_write(first_event)

        # Second write
        second_event = BusEvent("process2", 2, "test_event2", {"key": "value2"})
        participants[1].request_write(second_event)

        # Process the events
        await bus_controller._process_one_event(False)

        # Check the order of events read by each participant
        for participant in participants:
            assert participant.read_events == [first_event, second_event]

    async def test_event_loop_stops_processing_on_stop(self, bus_controller, bus_event):
        bus_participant = make_bus_participant(bus_controller)
        # Add participant and event
        bus_controller.add_participant(bus_participant)
        bus_participant.request_write(bus_event)

        # Start the event loop and then stop it immediately
        await bus_controller.start()
        bus_controller.stop()

        # Process events
        await bus_controller._process_one_event(False)

        # Check that no events were processed since the loop was stopped
        assert len(bus_participant.read_events) == 0

    async def test_no_processing_after_stop_called(self, bus_controller, bus_event):
        bus_participant = make_bus_participant(bus_controller)
        # Add participant and write event
        bus_controller.add_participant(bus_participant)
        bus_participant.request_write(bus_event)

        # Start the event loop and process events
        await bus_controller.start()
        await bus_controller._process_one_event(False)

        # Now stop the controller and add another event
        bus_controller.stop()
        bus_participant.request_write(bus_event)

        # Process events again
        await bus_controller._process_one_event(False)

        # The new event should not be processed as the loop has been stopped
        assert bus_participant.read_events.count(bus_event) == 1

    async def test_dynamic_participant_management(self, bus_controller, bus_event):
        # Create participants and add them to the controller
        participant_to_remove = make_bus_participant(bus_controller)
        bus_controller.add_participant(participant_to_remove)

        await bus_controller.start()

        # Write event and process
        participant_to_remove.request_write(bus_event)
        await bus_controller._process_one_event(False)

        # Remove the participant and process again
        bus_controller.remove_participant(participant_to_remove)
        assert participant_to_remove.controller is None

        await bus_controller._process_one_event(False)

        # The participant's read_events should not change since it was removed before the second write
        assert len(participant_to_remove.read_events) == 1

    async def test_stop(self, bus_controller):
        await bus_controller.start()
        assert not bus_controller.is_stopped
        bus_controller.stop()
        assert bus_controller.is_stopped
