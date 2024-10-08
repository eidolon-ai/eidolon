import os
import shutil
from concurrent.futures.process import ProcessPoolExecutor
from pathlib import Path
from typing import Optional, List

from crewai import Agent, Task, Crew, Process
from pydantic import BaseModel

from eidolon_ai_sdk.agent.crew.distributed_lock import managed_lock
from eidolon_ai_sdk.agent.crew.tempfile_syncronizer import sync_temp_loc
from eidolon_ai_sdk.system.reference_model import Specable


class CrewSpec(BaseModel):
    agents: List[dict]
    tasks: List[dict]
    process: Process = Process.sequential
    max_workers: Optional[int] = None


class CrewAgent(Specable[CrewSpec]):
    pool: ProcessPoolExecutor

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pool = ProcessPoolExecutor(max_workers=self.spec.max_workers)

    async def delete_process(self, process_id):
        crew_identifier = f"crew_file_sync_{process_id}"
        async with sync_temp_loc(crew_identifier) as tempdir:
            shutil.rmtree(tempdir)

    async def task(self, process_id):
        crew_identifier = f"crew_file_sync_{process_id}"
        async with managed_lock(crew_identifier), sync_temp_loc(crew_identifier) as synced_tempdir:
            # todo, this needs to be an async pool of some sort
            result = await self.pool.submit(do_crew_things, self.spec, synced_tempdir)
        return result


def do_crew_things(spec: CrewSpec, loc: Path):
    os.environ["CREWAI_STORAGE_DIR"] = str(loc)
    agents = [Agent(**a) for a in spec.agents]
    tasks = [Task(**t) for t in spec.tasks]
    crew = Crew(
        agents=agents,
        tasks=tasks,
        process=spec.process
    )
    return crew.kickoff()
