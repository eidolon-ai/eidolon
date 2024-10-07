import os
import shutil

from pydantic import BaseModel

from eidolon_ai_sdk.agent.crew.distributed_lock import managed_lock
from eidolon_ai_sdk.agent.crew.tempfile_syncronizer import sync_temp_loc
from eidolon_ai_sdk.system.reference_model import Specable


class CrewSpec(BaseModel):
    agents: dict
    tasks: dict


class CrewAgent(Specable[CrewSpec]):
    async def delete_process(self, process_id):
        crew_identifier = f"crew_file_sync_{process_id}"
        async with sync_temp_loc(crew_identifier) as tempdir:
            shutil.rmtree(tempdir)

    async def task(self, process_id):
        crew_identifier = f"crew_file_sync_{process_id}"
        async with managed_lock(crew_identifier), sync_temp_loc(crew_identifier) as synced_tempdir:
            # todo, I think there is a environ context manager, regardless we need to test that this does not bleed between simultaneous requests
            os.environ["CREWAI_STORAGE_DIR"] = synced_tempdir
