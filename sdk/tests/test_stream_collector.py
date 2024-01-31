import pytest

from eidos_sdk.io.events import StringOutputEvent, ErrorEvent, StartStreamContextEvent, EndStreamContextEvent
from eidos_sdk.util.stream_collector import StreamCollector


async def raising_stream(error=None):
    yield StringOutputEvent(content="test")
    if error:
        raise error


async def test_process_event_raises():
    events = []
    with pytest.raises(RuntimeError) as e:
        async for event in StreamCollector(stream=raising_stream(RuntimeError("test error"))):
            events.append(event)
    assert events == [
        StringOutputEvent(content='test'),
        ErrorEvent(reason='test error'),
    ]
    assert e.value.args[0] == "test error"


async def test_terminates_without_raising():
    events = [event async for event in StreamCollector(stream=raising_stream())]
    assert events == [StringOutputEvent(content='test')]


async def test_adds_context():
    events = [event async for event in StreamCollector(stream=raising_stream(), wrap_with_context=StartStreamContextEvent(context_id="foo"))]
    assert events == [
        StartStreamContextEvent(context_id='foo'),
        StringOutputEvent(stream_context='foo', content='test'),
        EndStreamContextEvent(context_id='foo'),
    ]
