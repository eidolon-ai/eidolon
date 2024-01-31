import pytest

from eidos_sdk.io.events import StringOutputEvent, ErrorEvent, StartStreamContextEvent, EndStreamContextEvent
from eidos_sdk.util.stream_collector import StreamCollector, ManagedContextError, stream_manager


async def raising_stream(error=None):
    yield StringOutputEvent(content="test")
    if error:
        raise error


async def test_terminates_without_raising():
    events = [event async for event in StreamCollector(stream=raising_stream())]
    assert events == [StringOutputEvent(content="test")]


async def test_adds_context():
    events = [event async for event in stream_manager(raising_stream(), StartStreamContextEvent(context_id="foo"))]
    assert events == [
        StartStreamContextEvent(context_id="foo"),
        StringOutputEvent(stream_context="foo", content="test"),
        EndStreamContextEvent(context_id="foo"),
    ]


async def test_stream_manager_records_errors_and_reraises():
    events = []
    error = RuntimeError("test error")
    with pytest.raises(ManagedContextError) as e:
        async for event in stream_manager(raising_stream(error), StartStreamContextEvent(context_id="foo")):
            events.append(event)
    assert events == [
        StartStreamContextEvent(context_id="foo"),
        StringOutputEvent(stream_context="foo", content="test"),
        ErrorEvent(stream_context="foo", reason=error),
        EndStreamContextEvent(context_id="foo"),
    ]
    assert e.value.args[0] == "Error in stream context foo"
