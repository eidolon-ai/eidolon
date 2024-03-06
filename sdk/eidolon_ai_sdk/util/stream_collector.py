from __future__ import annotations

from typing import Optional, AsyncIterator, List, Callable

from eidolon_ai_client.events import (
    BaseStreamEvent,
    StringOutputEvent,
    ObjectOutputEvent,
    ErrorEvent,
    StreamEvent,
    StartStreamContextEvent,
    EndStreamContextEvent,
    SuccessEvent,
)
from eidolon_ai_client.util.logger import logger


class StreamCollector(AsyncIterator[StreamEvent]):
    _content: List[str | dict]
    stream: Optional[AsyncIterator[StreamEvent]]

    def __init__(
        self,
        stream: Optional[AsyncIterator[StreamEvent]] = None,
        context_level: Optional[str] = None,
    ):
        self._content = []
        self.stream = stream
        self._context_level = context_level
        self._last_seen_event = None

    def process_event(self, event: BaseStreamEvent):
        if event.stream_context == self._context_level:
            if isinstance(event, StringOutputEvent):
                if isinstance(self._last_seen_event, StringOutputEvent):
                    self._content[-1] += event.content
                else:
                    self._content.append(event.content)
                self._last_seen_event = event
            elif isinstance(event, ObjectOutputEvent):
                self._content.append(event.content)
                self._last_seen_event = event
            elif isinstance(event, ErrorEvent):
                self._content.append(event.reason)
                self._last_seen_event = event

    def get_content(self):
        if not self._content:
            return None
        elif len(self._content) == 1:
            return self._content[0]
        else:
            return self._content

    def get_content_as_string(self):
        pass

    async def __anext__(self):
        event = await self.stream.__anext__()
        self.process_event(event)
        return event


def stream_manager(
    stream: AsyncIterator[StreamEvent] | Callable[[], AsyncIterator[StreamEvent]], context: StartStreamContextEvent
):
    async def _iter():
        yield context.model_copy()
        try:
            received_end_event = False
            async for event in stream() if callable(stream) else stream:
                if not received_end_event:
                    received_end_event = event.is_root_end_event()
                    acc = [context.get_nested_context()]
                    if event.stream_context:
                        acc.append(event.stream_context)
                    event.stream_context = ".".join(acc)
                    yield event
                else:
                    logger.warning(f"Received event ({event.event_type}) after end event, ignoring")
            if not received_end_event:
                yield SuccessEvent(stream_context=context.get_nested_context())
        except Exception as e:
            # record error on stream context, but will reraise for outer context to handle
            yield ErrorEvent(stream_context=context.get_nested_context(), reason=f"{type(e).__name__}: {e}")
            # no need to log since we are re-raising
            raise ManagedContextError(f"Error in stream context {context.get_nested_context()}") from e
        finally:
            yield EndStreamContextEvent(stream_context=context.stream_context, context_id=context.context_id)

    return StreamCollector(_iter(), context_level=context.get_nested_context())


class ManagedContextError(Exception):
    pass
