from __future__ import annotations

import typing

from pydantic import Field, BaseModel


class AsyncStateResponse(BaseModel):
    process_id: str = Field(..., description="The ID of the conversation.")


class SyncStateResponse(AsyncStateResponse):
    state: str = Field(..., description="The state of the conversation.")
    data: typing.Any = Field(..., description="The data returned by the last state change.")
    available_actions: typing.List[str] = Field(..., description="The actions available from the current state.")
