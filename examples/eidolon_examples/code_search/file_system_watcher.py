import threading
from typing import Callable

from watchdog.events import FileSystemEventHandler, FileSystemEvent


class FileSystemWatcher(FileSystemEventHandler):
    def __init__(self, debounce_time, event_handler: Callable[[FileSystemEvent], None]):
        self.debounce_time = debounce_time
        self.timer = None
        self.lock = threading.Lock()
        self.event_handler = event_handler

    def on_any_event(self, event: FileSystemEvent):
        with self.lock:
            if self.timer is not None:
                self.timer.cancel()
            self.timer = threading.Timer(self.debounce_time, self.handle_event, [event])
            self.timer.start()

    def handle_event(self, event: FileSystemEvent):
        self.event_handler(event)
