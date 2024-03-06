from typing import Optional, Set, cast

from eidolon_ai_client.util.request_context import RequestContext, User
from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.security.security_manager import AuthorizationProcessor, Permission, AuthenticationProcessor, \
    PermissionException
from eidolon_ai_sdk.system.processes import MongoDoc


class AuthDoc(MongoDoc):
    collection = "resource_auth_records"
    resource_type: str
    resource_id: str
    subject_type: str
    subject_id: str
    permissions: Set[Permission]
    extra: dict = {}


class PrivateAuthorization(AuthorizationProcessor):
    async def check_permission(self, permissions: Permission | Set[Permission], agent: str, process_id: Optional[str] = None):
        permissions: Set[Permission] = {permissions} if isinstance(permissions, str) else permissions
        user: User = RequestContext.current_user
        functional = user.agent_process_permissions(agent)
        missing_functional = permissions.difference(functional)
        if missing_functional:
            raise PermissionException(missing_functional)
        user: User = RequestContext.current_user

        missing_resource = permissions
        async for doc in AuthDoc.find(
                query=dict(subject_id=user.id, subject_type='user'),
                projection=dict(permissions=1),
        ):
            doc: AuthDoc = doc
            missing_resource = missing_resource.difference(doc.permissions)
        if missing_resource:
            raise PermissionException(missing_resource, process_id)

    async def record_resource(self, agent: str, process_id: str):
        user: User = RequestContext.current_user
        await AuthDoc.create(
            resource_type=f"{agent}/process",
            resource_id=process_id,
            subject_type="user",
            subject_id=user.id,
            permissions={"read", "update", "delete"},
            extra=dict(username=user.name),
        )

    async def delete_process(self, process_id):
        await AgentOS.symbolic_memory.delete(AuthDoc.collection, {"resource_id": process_id})
