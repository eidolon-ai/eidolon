from __future__ import annotations

import typing

from pydantic import Field, BaseModel


class CreateProcessArgs(BaseModel):
    agent: str = Field(description="The executable agent for the process.")
    title: typing.Optional[str] = Field(None, description="The title of the process")


class DeleteProcessResponse(BaseModel):
    process_id: str
    deleted: int


class StateSummary(BaseModel):
    agent: str = Field(..., description="The agent that is running the process.")
    process_id: str = Field(..., description="The ID of the conversation.")
    parent_process_id: typing.Optional[str] = Field(None, description="The ID of the parent conversation.")
    state: str = Field(..., description="The state of the conversation.")
    available_actions: typing.List[str] = Field(..., description="The actions available from the current state.")
    title: typing.Optional[str] = None
    created: str = None
    updated: str = None


class SyncStateResponse(StateSummary):
    data: typing.Any = Field(..., description="The data returned by the last state change.")


class ListProcessesResponse(BaseModel):
    total: int = Field(..., description="The total number of processes.")
    processes: typing.List[StateSummary] = Field(..., description="The list of processes.")
    next: typing.Optional[str] = Field(..., description="The next page of results, if any.")
