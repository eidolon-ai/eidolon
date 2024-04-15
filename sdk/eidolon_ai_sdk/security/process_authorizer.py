from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Set, List

from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.security.permissions import PermissionException
from eidolon_ai_sdk.agent_os_interfaces import Permission
from eidolon_ai_sdk.security.user import User
from eidolon_ai_sdk.system.processes import MongoDoc


class ProcessAuthorizer(ABC):
    @abstractmethod
    async def check_process_perms(self, permissions: Set[Permission], agent: str, process_id: str):
        """
        Checks if the authenticated user has the specified permission(s) to the provided agent process.
        :raises PermissionException: If the agent does not have the required permissions.
        """
        pass

    @abstractmethod
    async def record_process(self, agent: str, resource_id: str):
        """
        Called when a process is created. Should propagate any state needed for future resource checks.
        """
        pass


class AuthDoc(MongoDoc):
    collection = "resource_auth_records"
    resource_type: str
    resource_id: str
    subject_type: str
    subject_id: str
    permissions: List[Permission]
    extra: dict = {}


class PrivateAuthorizer(ProcessAuthorizer):
    async def check_process_perms(self, permissions: Set[Permission], agent: str, process_id: str):
        if process_id:
            missing_resource = permissions
            async for doc in AuthDoc.find(
                query=dict(
                    subject_id=User.get_current().id,
                    subject_type="user",
                    resource_type=f"{agent}/process",
                    resource_id=process_id,
                ),
                projection=dict(permissions=1),
                convert=False,
            ):
                missing_resource = missing_resource.difference(doc["permissions"])
            if missing_resource:
                raise PermissionException(missing_resource, process_id)

    async def record_process(self, agent: str, process_id: str):
        user = User.get_current()
        await AuthDoc.create(
            resource_type=f"{agent}/process",
            resource_id=process_id,
            subject_type="user",
            subject_id=user.id,
            permissions=["read", "update", "delete"],
            extra=dict(username=user.name),
        )

    @staticmethod
    async def delete_process(process_id):
        await AgentOS.symbolic_memory.delete(AuthDoc.collection, {"resource_id": process_id})
