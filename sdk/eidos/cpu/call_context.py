from typing import Optional

from bson import ObjectId
from pydantic import BaseModel


class CallContext(BaseModel):
    process_id: str
    thread_id: Optional[str] = None

    def derive_call_context(self):
        return CallContext(process_id=self.process_id, thread_id=str(ObjectId()))
