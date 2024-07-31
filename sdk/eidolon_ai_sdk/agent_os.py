from __future__ import annotations

import os

from eidolon_ai_client.util.request_context import RequestContext
from eidolon_ai_sdk.agent_os_interfaces import (
    ProcessFileSystem,
    FileMemory,
    SymbolicMemory,
    SecurityManager,
    SimilarityMemory,
)
from eidolon_ai_sdk.security.user import User


class AgentOS:
    file_memory: FileMemory = ...  # noqa: F821
    symbolic_memory: SymbolicMemory = ...  # noqa: F821
    similarity_memory: SimilarityMemory = ...  # noqa: F821
    security_manager: SecurityManager = ...  # noqa: F821
    process_file_system: ProcessFileSystem = ...  # noqa: F821
    machine_name: str = ...

    @staticmethod
    def current_machine_url() -> str:
        return os.environ.get("EIDOLON_LOCAL_MACHINE", "http://localhost:8080")

    @staticmethod
    def current_user() -> User:
        return User.get_current()

    @staticmethod
    def current_agent_name() -> str:
        return RequestContext["agent_name"]

    @staticmethod
    def current_process_id() -> str:
        return RequestContext["process_id"]
