import asyncio
from functools import wraps, partial


def make_async(func):
    """
    Decorator to make a sync function async and non-blocking by running them in a thread.
    """

    @wraps(func)
    async def run(*args, **kwargs):
        loop = asyncio.get_event_loop()
        # use default ThreadPoolExecutor. Executor will be cached on event loop, so we don't want to manage it ourselves
        return await loop.run_in_executor(executor=None, func=(partial(func, *args, **kwargs)))

    return run
