from __future__ import annotations

from typing import Optional, Set

from pydantic import BaseModel

from eidolon_ai_sdk.security.authentication_processor import AuthenticationProcessor
from eidolon_ai_sdk.security.functional_authorizer import FunctionalAuthorizer
from eidolon_ai_sdk.security.permissions import Permission
from eidolon_ai_sdk.security.process_authorizer import ProcessAuthorizer
from eidolon_ai_sdk.system.reference_model import Specable, AnnotatedReference


class SecurityManagerSpec(BaseModel):
    authentication_processor: AnnotatedReference[AuthenticationProcessor]
    functional_authorizer: AnnotatedReference[FunctionalAuthorizer]
    process_authorizer: AnnotatedReference[ProcessAuthorizer]

    safe_paths: Set[str] = {"/system/health", "/docs", "/favicon.ico", "/openapi.json"}


class SecurityManager(Specable[SecurityManagerSpec]):
    authentication_processor: AuthenticationProcessor
    functional_authorizer: FunctionalAuthorizer
    process_authorizer: ProcessAuthorizer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.authentication_processor = self.spec.authentication_processor.instantiate()
        self.functional_authorizer = self.spec.functional_authorizer.instantiate()
        self.process_authorizer = self.spec.process_authorizer.instantiate()

    async def check_permissions(
        self, permissions: Permission | Set[Permission], agent: str, process_id: Optional[str] = None
    ):
        permissions = {permissions} if isinstance(permissions, str) else permissions
        await self.functional_authorizer.check_functional_perms(permissions, f"agents/{agent}/processes")
        if process_id:
            await self.process_authorizer.check_process_perms(permissions, agent, process_id)
