import asyncio
from collections import defaultdict

import pytest
from aiostream import stream
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.trace import get_current_span


@pytest.mark.skip(reason="Currently preventing us from automatically generating spans on context objects automatically")
async def test_recurse_streaming_context():
    trace.set_tracer_provider(TracerProvider())

    async def stream_fn(title):
        with tracer.start_as_current_span(title):
            context = get_current_span().get_span_context()
            yield (title, format(context.span_id, "016x"))
            await asyncio.sleep(0)
            context2 = get_current_span().get_span_context()
            yield (title, format(context2.span_id, "016x"))

    acc = defaultdict(list)
    tracer = trace.get_tracer("test_tracer")
    with tracer.start_as_current_span("test span"):
        async for e in stream.merge(*[stream_fn(f"child_{i}") for i in range(2)]):
            acc[e[0]].append(e[1])

    assert acc["child_0"][0] == acc["child_0"][1]
    # AssertionError: assert 'caa5694e43a514db' == '57adf8fb9e10a596'