from typing import Set, List

from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.security.security_manager import (
    ProcessAuthorizer,
    Permission,
    PermissionException,
    User,
)
from eidolon_ai_sdk.system.processes import MongoDoc


class AuthDoc(MongoDoc):
    collection = "resource_auth_records"
    resource_type: str
    resource_id: str
    subject_type: str
    subject_id: str
    permissions: List[Permission]
    extra: dict = {}


class PrivateAuthorization(ProcessAuthorizer):
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
