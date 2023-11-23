from dataclasses import dataclass
from typing import Optional

from bson import ObjectId


@dataclass
class CallContext:
    def __init__(self, process_id: str, thread_id: Optional[str]):
        self.process_id = process_id
        self.thread_id = thread_id
    
    def derive_call_context(self):
        return CallContext(process_id=self.process_id, thread_id=str(ObjectId()))
