import asyncio
import os
import shutil
from concurrent.futures.process import ProcessPoolExecutor
from pathlib import Path
from typing import Optional, Annotated, List

from crewai import Agent, Task, Crew, Process
from fastapi import Body
from pydantic import BaseModel

from eidolon_ai_sdk.agent.agent import register_program
from eidolon_ai_sdk.agent.crew.distributed_lock import managed_lock
from eidolon_ai_sdk.agent.crew.tempfile_syncronizer import sync_temp_loc
from eidolon_ai_sdk.system.reference_model import Specable


class CrewSpec(BaseModel):
    max_workers: Optional[int] = None
    agents: dict = {}
    tasks: dict = {}
    crew: dict = {}
    process: Process = Process.sequential


class CrewAgent(Specable[CrewSpec]):
    pool: ProcessPoolExecutor

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pool = ProcessPoolExecutor(max_workers=self.spec.max_workers)

    async def delete_process(self, process_id):
        crew_identifier = f"crew_file_sync_{process_id}"
        async with sync_temp_loc(crew_identifier) as tempdir:
            shutil.rmtree(tempdir)

    @register_program()
    async def kickoff(self, process_id, body: Annotated[dict, Body()] = None):
        body = body or {}
        crew_identifier = f"crew_file_sync_{process_id}"
        async with managed_lock(crew_identifier), sync_temp_loc(crew_identifier) as synced_tempdir:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                self.pool,
                do_crew_things,
                body, self.spec, str(synced_tempdir)
            )
        if isinstance(result, Exception):
            raise result
        return result


def do_crew_things(body, spec: CrewSpec, loc: Path):
    try:
        os.environ["CREWAI_STORAGE_DIR"] = str(loc)
        agents = {k: Agent(**a) for k, a in spec.agents.items()}

        contexts = {}
        for k, t in spec.tasks.items():
            if "context" in t:
                contexts[k] = t.pop("context")
            if "agent" in t:
                if t["agent"] not in agents:
                    raise ValueError(f"Agent {t['agent']} not found in agents")
                t["agent"] = agents[t["agent"]]

        tasks = {k: Task(**t) for k, t in spec.tasks.items()}
        for k, xs in contexts.items():
            tasks[k].context = []
            for x in xs:
                if x not in tasks:
                    raise ValueError(f"Task {x} not found in tasks")
                tasks[k].context.append(tasks[x])

        # todo add support for tool calls

        crew = Crew(
            agents=list(agents.values()),
            tasks=list(tasks.values()),
            process=spec.process,
            **spec.crew,
        )
        resp = crew.kickoff(body)
        return resp.raw
    except Exception as e:
        return RuntimeError(f"{type(e).__name__}: {str(e)}")
