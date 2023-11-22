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


class FileManagerConfig(LogicUnitConfig):
    root_dir: str


class FileManager(LogicUnit, Specable[FileManagerConfig]):
    repo: Repo

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.spec.root_dir = os.path.expandvars(self.spec.root_dir)
        self.repo = Repo(self.spec.root_dir)

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
    async def get_file(self, file_path: str) -> dict:
        """
        Get the contents of a file in the project
        """
        try:
            with open(os.path.join(self.spec.root_dir, file_path), 'r') as f:
                return dict(exists=True, content=f.read())
        except FileNotFoundError:
            return dict(exists=False)

    @llm_function
    async def upsert_file(
            self,
            update_summary: Annotated[str, Field(description="A summary of the changes. Will be included in commit message")],
            file_path: Annotated[str, Field(description="The path to the file to be updated")],
            content: Annotated[str, Field(description="The new content of the file")],
    ) -> dict:
        """
        replace the contents a file or create it if it doesn't exist and commit the changes.
        """
        # todo, limit to files in project
        file_path = os.path.join(self.spec.root_dir, file_path)
        with open(file_path, 'w') as f:
            f.write(content)
        self.repo.git.add(file_path)
        self.repo.index.commit(update_summary)
        return dict(revision=self.repo.head.commit.hexsha)

    @llm_function
    async def revert(self, revision: Annotated[str, Field(description="The commit hexsha to revert to")]) -> dict:
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
