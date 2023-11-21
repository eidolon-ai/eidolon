from dataclasses import dataclass
from typing import Optional


@dataclass
class CallContext:
    def __init__(self, process_id: str, thread_id: Optional[str]):
        self.process_id = process_id
        self.thread_id = thread_id
