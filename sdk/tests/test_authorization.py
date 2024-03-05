from typing import Optional, Set, List

from fastapi import HTTPException
from openai import BaseModel
from starlette.requests import Request

from eidolon_ai_sdk.security.security_manager import AuthenticationProcessor, Permission, PermissionException
from eidolon_ai_sdk.system.reference_model import Specable


class TestAuthenticationProcessorSpec(BaseModel):
    raise_on_check_auth: bool = False
    should_record_resource: bool = True
    recorded_resources: List[str] = []
    functional_perms: Set[Permission] = set()
    resource_perms: Set[Permission] = set()

class TestAuthenticationProcessor(Specable[TestAuthenticationProcessorSpec], AuthenticationProcessor):
    async def check_auth(self, request: Request):
        if self.spec.raise_on_check_auth:
            raise HTTPException(status_code=401, detail="Unauthenticated")

    async def check_permission(self, permissions: Permission | Set[Permission], agent: str,
                               process: Optional[str] = None):
        permissions = [permissions] if isinstance(permissions, str) else permissions
        missing_functional_perms = self.spec.functional_perms.difference(permissions)
        if missing_functional_perms:
            raise PermissionException(missing_functional_perms)
        missing_resource_perms = self.spec.resource_perms.difference(permissions)
        if process and process not in self.spec.recorded_resources or missing_resource_perms:
            raise PermissionException(missing_resource_perms, process)

    async def record_resource(self, agent: str, process: Optional[str] = None):
        if self.spec.should_record_resource:
            self.spec.recorded_resources.append(process)


def test_system_health_does_not_require_permissions():
    assert False

def test_version_does_not_require_permissions():
    assert False

def test_processes_requires_read_permissions():
    assert False

def test_processes_does_not_return_records_with_no_read_permission():
    assert False
