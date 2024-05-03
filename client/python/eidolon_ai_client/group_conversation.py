from typing import List, Any, Optional, Tuple

from pydantic import BaseModel

from eidolon_ai_client.client import Process, Agent, ProcessStatus, AgentResponseIterator, DeleteProcessResponse
from eidolon_ai_client.events import StartStreamContextEvent, EndStreamContextEvent
from eidolon_ai_client.util.stream_collector import merge_streams


class GroupConversation:
    def __init__(self, agents: List[ProcessStatus]):
        self.agents = agents

    @classmethod
    async def create(cls, agents: List[str]):
        agent_pids = []
        for agent in agents:
            agent_pids.append(await Agent.get(agent).create_process())
        return cls(agent_pids)

    @classmethod
    async def restore(cls, processes: List[ProcessStatus]):
        return cls(processes)

    async def action(self, action_name: str, body: dict | BaseModel | str | None = None, **kwargs) -> List[ProcessStatus]:
        statuses = []
        for agent in self.agents:
            statuses.append(await agent.action(action_name, body, **kwargs))
        self.agents = statuses
        return statuses

    async def stream_action(self, action_name: str, body: Optional[Any] = None, **kwargs) -> AgentResponseIterator:
        async def run_one(agent_name: str, agent_pid: str):
            yield StartStreamContextEvent(context_id=agent_name, title=agent_name)
            agent = Agent.get(agent_name)
            try:
                async for a_event in (
                        Process(machine=agent.machine, process_id=agent_pid).stream_action(agent.agent, action_name, body, **kwargs)
                ):
                    a_event.stream_context = agent_name
                    yield a_event
            finally:
                yield EndStreamContextEvent(context_id=agent_name)

        tasks = []
        for process in self.agents:
            tasks.append(run_one(process.agent, process.process_id))

        combined_calls = merge_streams(tasks)
        async for event in combined_calls:
            yield event

        self.agents = await self.status()

    async def status(self) -> List[ProcessStatus]:
        statuses = []
        for agent in self.agents:
            statuses.append(await agent.status())
        return statuses

    async def delete(self) -> List[Tuple[Process, DeleteProcessResponse]]:
        deleted = []
        for agent in self.agents:
            deleted.append((agent, await agent.delete()))
        return deleted
