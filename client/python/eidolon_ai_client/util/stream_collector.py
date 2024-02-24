from typing import AsyncIterator, List

from aiostream import stream


async def merge_streams(streams: List[AsyncIterator]) -> AsyncIterator:
    if len(streams) > 1:
        merged_stream = stream.merge(streams[0], *streams[1:])
        async with merged_stream.stream() as s:
            async for value in s:
                yield value
    elif len(streams) == 1:
        async for v in streams[0]:
            yield v
