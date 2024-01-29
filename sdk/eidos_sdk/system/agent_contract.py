from __future__ import annotations

import typing

from pydantic import Field, BaseModel


class StateSummary(BaseModel):
    process_id: str = Field(..., description="The ID of the conversation.")
    state: str = Field(..., description="The state of the conversation.")
    available_actions: typing.List[str] = Field(..., description="The actions available from the current state.")


class SyncStateResponse(StateSummary):
    data: typing.Any = Field(..., description="The data returned by the last state change.")


class ListProcessesResponse(BaseModel):
    total: int = Field(..., description="The total number of processes.")
    processes: typing.List[StateSummary] = Field(..., description="The list of processes.")
    next: typing.Optional[str] = Field(..., description="The next page of results, if any.")
