from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Callable

from eidolon_ai_sdk.memory.chroma_vector_store import ChromaVectorStore
from eidolon_ai_sdk.memory.local_file_memory import LocalFileMemory
from eidolon_ai_sdk.memory.local_symbolic_memory import LocalSymbolicMemory
from eidolon_ai_sdk.memory.similarity_memory import SimilarityMemoryImpl
from eidolon_ai_sdk.system.agent_machine import MachineSpec
from eidolon_ai_sdk.system.resources.machine_resource import MachineResource
from eidolon_ai_sdk.system.resources.resources_base import Metadata
from eidolon_ai_sdk.util.class_utils import fqn

skip_decorator: Callable[[type[TestMachine]], type[TestMachine]]

try:
    import pytest
    skip_decorator = pytest.mark.skip(reason="This test class should not be run by pytest")
except ImportError:
    # Define a no-op decorator if pytest is not installed
    def skip_decorator(cls):
        return cls


@skip_decorator
class TestMachine(MachineResource):
    __test__ = False
    _file_memory: str
    _similarity_memory: str

    def __init__(self, storage_loc: str | Path):
        similarity_memory = str(Path(storage_loc) / "similarity_memory")
        file_memory = str(Path(storage_loc) / "file_memory")
        os.mkdir(file_memory)
        os.mkdir(similarity_memory)
        super().__init__(
            apiVersion="v1",
            metadata=Metadata(name="test_machine"),
            spec=MachineSpec(
                symbolic_memory=fqn(LocalSymbolicMemory),
                file_memory=dict(
                    implementation=fqn(LocalFileMemory),
                    root_dir=storage_loc,
                ),
                similarity_memory=dict(
                    implementation=fqn(SimilarityMemoryImpl),
                    vector_store=dict(
                        implementation=fqn(ChromaVectorStore),
                        url=f"file://{similarity_memory}", )),
            ),
        )
        self._file_memory = file_memory
        self._similarity_memory = similarity_memory

    def reset_state(self):
        LocalSymbolicMemory.db = {}
        shutil.rmtree(self._file_memory)
        shutil.rmtree(self._similarity_memory)
        os.mkdir(self._file_memory)
        os.mkdir(self._similarity_memory)
