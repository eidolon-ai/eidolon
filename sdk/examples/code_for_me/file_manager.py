import asyncio
import json
import os
import tempfile
from asyncio import subprocess
from typing import List, Annotated

from git import Repo
from pydantic import BaseModel, Field

from eidolon_sdk.cpu.logic_unit import LogicUnit, LogicUnitConfig, llm_function
from eidolon_sdk.reference_model import Specable


class FileUpdate(BaseModel):
    file_path: Annotated[str, Field(description="The path to the file to be updated")]
    content: Annotated[str, Field(description="The new content of the file")]


class FileManagerConfig(LogicUnitConfig):
    root_dir: str


class FileManager(LogicUnit, Specable[FileManagerConfig]):
    repo: Repo

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repo = Repo.init(self.spec.root_dir)

    @llm_function
    async def list_files(self) -> List[str]:
        """
        List all files in the project
        """
        all_files = []
        for root, dirs, files in os.walk(self.spec.root_dir):
            for file in files:
                all_files.append(os.path.relpath(os.path.join(root, file), self.spec.root_dir))
        return all_files

    @llm_function
    async def update_files(
            self,
            update_summary: Annotated[str, Field(description="A summary of the changes. Will be included in commit message")],
            updates: Annotated[List[FileUpdate], Field(description="A list of update instructions")],
    ) -> dict:
        """
        Update the contents of one or more files in the project and commit the changes.
        """
        # todo, limit to files in project
        for update in updates:
            file_path = os.path.join(self.spec.root_dir, update.file_path)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as f:
                f.write(update.content)
        self.repo.index.add([u.file_path for u in updates])
        self.repo.index.commit(update_summary)
        return dict(revision=self.repo.head.commit.hexsha)

    @llm_function
    async def revert(self, revision) -> dict:
        """
        Revert the project to a previous revision.
        """
        self.repo.git.reset('--hard', revision)
        return dict(revision=self.repo.head.commit.hexsha)

    @llm_function
    async def run_pytest_async(self) -> dict:
        """
        Run pytest in the project directory and return the results.
        :return:
        """
        with tempfile.NamedTemporaryFile(suffix='.json', mode='w+', delete=True) as tmpfile:
            cmd = ["pytest", self.spec.root_dir, "--json-report", "--json-report-file=" + tmpfile.name]

            # Run pytest in a new process
            process = await asyncio.create_subprocess_exec(*cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Wait for the process to complete
            await process.wait()

            # Go back to the start of the file and read the content
            tmpfile.seek(0)
            report = json.load(tmpfile)

        return report
