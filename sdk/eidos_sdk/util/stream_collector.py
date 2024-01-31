from __future__ import annotations

from collections import deque
from typing import Optional, AsyncIterator, Deque

from eidos_sdk.io.events import BaseStreamEvent, StringOutputEvent, ObjectOutputEvent, ErrorEvent, StreamEvent, \
    StartStreamContextEvent, EndStreamContextEvent


class StreamCollector(AsyncIterator[StreamEvent]):
    contents: Optional[str | dict]
    stream: Optional[AsyncIterator[StreamEvent]]

    def __init__(self, stream: Optional[AsyncIterator[StreamEvent]] = None, wrap_with_context: Optional[StartStreamContextEvent] = None):
        self.contents = None
        self.stream = stream
        self._wrap_with_context = wrap_with_context
        self._has_wrapped_start = False
        self._tail_events: Deque[BaseStreamEvent | Exception] = deque()
        if self._wrap_with_context:
            self._tail_events.append(EndStreamContextEvent(context_id=self._wrap_with_context.context_id))

    def process_event(self, event: BaseStreamEvent):
        if event.is_root_and_type(StringOutputEvent):
            if self.contents is None:
                self.contents = event.content
            elif isinstance(self.contents, str):
                self.contents += event.content
            else:
                self.contents = str(self.contents) + event.content
        elif event.is_root_and_type(ObjectOutputEvent):
            if self.contents is None:
                self.contents = event.content
            else:
                self.contents = str(self.contents) + "\n" + str(event.content)
        elif event.is_root_and_type(ErrorEvent):
            if self.contents is None:
                self.contents = str(event.reason)
            else:
                self.contents = str(self.contents) + "\n" + str(event.reason)

    async def __anext__(self):
        if self._wrap_with_context and not self._has_wrapped_start:
            self._has_wrapped_start = True
            return self._wrap_with_context
        try:
            next_event = await self.stream.__anext__()
            self.process_event(next_event)
        except StopAsyncIteration:
            if not self._tail_events:
                raise
            next_ = self._tail_events.popleft()
            if isinstance(next_, BaseException):
                raise next_
            else:
                return next_
        except Exception as e:
            self._tail_events.appendleft(ErrorEvent(reason=str(e)))
            self._tail_events.append(e)
            return await self.__anext__()
        if self._wrap_with_context:
            next_event.stream_context = self._wrap_with_context.context_id
        return next_event

    async def fill_and_retrieve_response(self):
        async for event in self.stream:
            self.process_event(event)
        return self.contents
