from typing import Optional, List, AsyncIterator

from pydantic import BaseModel

from eidolon_ai_sdk.agent_os import AgentOS


class AgentCallHistory(BaseModel):
    parent_process_id: str
    parent_thread_id: Optional[str]
    machine: str
    agent: str
    remote_process_id: str
    state: str
    available_actions: List[str]

    async def upsert(self):
        query = {
            "parent_process_id": self.parent_process_id,
            "parent_thread_id": self.parent_thread_id,
            "agent": self.agent,
            "remote_process_id": self.remote_process_id,
        }
        await AgentOS.symbolic_memory.upsert_one("agent_logic_unit", self.model_dump(), query)

    @classmethod
    async def get_agent_state(cls, parent_process_id: str, parent_thread_id: Optional[str] = None):
        query = {
            "parent_process_id": parent_process_id,
            "parent_thread_id": parent_thread_id,
        }
        return [
            AgentCallHistory.model_validate(o) async for o in AgentOS.symbolic_memory.find("agent_logic_unit", query)
        ]

    @classmethod
    async def get_child_pids(cls):
        return {
            o["remote_process_id"]: o["parent_process_id"]
            async for o in AgentOS.symbolic_memory.find(
                "agent_logic_unit", {}, projection={"remote_process_id": 1, "parent_process_id": 1}
            )
        }

    @classmethod
    async def get_children(cls, parent_process_id: str) -> AsyncIterator[str]:
        async for record in AgentOS.symbolic_memory.find(
            "agent_logic_unit", {"parent_process_id": parent_process_id}, projection={"remote_process_id": 1}
        ):
            yield record["remote_process_id"]

    @classmethod
    async def delete(cls, query):
        return await AgentOS.symbolic_memory.delete("agent_logic_unit", query)
