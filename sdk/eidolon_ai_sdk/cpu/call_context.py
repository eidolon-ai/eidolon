from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field

from eidolon_ai_client.util.request_context import RequestContext


class CallContext(BaseModel):
    process_id: str = Field(default_factory=lambda: RequestContext.get("process_id"))
    thread_id: Optional[str] = None

    def derive_call_context(self):
        return CallContext(process_id=self.process_id, thread_id=str(ObjectId()))
