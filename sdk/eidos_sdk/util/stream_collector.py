from __future__ import annotations

from eidos_sdk.io.events import BaseStreamEvent, StringOutputEvent, ObjectOutputEvent


class StringStreamCollector:
    contents: str

    def __init__(self):
        self.contents = None

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
                self.contents = str(self.contents) + str(event.content)
