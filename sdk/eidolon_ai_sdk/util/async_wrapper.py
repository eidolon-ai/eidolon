import asyncio
from concurrent.futures import ThreadPoolExecutor
from functools import wraps, partial
from typing import Callable

from opentelemetry import context as otel_context, trace
from opentelemetry.trace import Tracer


# opentelemetry traces are lost in thread pool executor, this preserves them
# https://stackoverflow.com/questions/70772036/is-it-possible-to-get-open-telemetry-tracing-in-python-to-record-spans-that-happ
class TracedThreadPoolExecutor(ThreadPoolExecutor):
    """Implementation of :class:`ThreadPoolExecutor` that will pass context into sub tasks."""

    def __init__(self, tracer: Tracer, *args, **kwargs):
        self.tracer = tracer
        super().__init__(*args, **kwargs)

    def with_otel_context(self, context: otel_context.Context, fn: Callable):
        otel_context.attach(context)
        return fn()

    def submit(self, fn, *args, **kwargs):
        """Submit a new task to the thread pool."""

        # get the current otel context
        context = otel_context.get_current()
        if context:
            return super().submit(
                lambda: self.with_otel_context(
                    context, lambda: fn(*args, **kwargs)
                ),
            )
        else:
            return super().submit(lambda: fn(*args, **kwargs))


tracer = trace.get_tracer(__name__)
executor = TracedThreadPoolExecutor(tracer)


def make_async(func, exe=executor):
    """
    Decorator to make a sync function async and non-blocking by running them in a thread.
    """

    @wraps(func)
    async def run(*args, **kwargs):
        loop = asyncio.get_event_loop()
        # use default ThreadPoolExecutor. Executor will be cached on event loop, so we don't want to manage it ourselves
        return await loop.run_in_executor(executor=exe, func=(partial(func, *args, **kwargs)))

    return run
