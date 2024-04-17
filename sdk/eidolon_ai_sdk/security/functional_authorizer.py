from __future__ import annotations

import fnmatch
from abc import abstractmethod
from typing import Set

from eidolon_ai_sdk.security.permissions import PermissionException
from eidolon_ai_sdk.agent_os_interfaces import Permission
from eidolon_ai_sdk.security.user import User


class FunctionalAuthorizer:
    @abstractmethod
    async def check_functional_perms(self, permissions: Set[Permission], target):
        pass


class NoopFunctionalAuth(FunctionalAuthorizer):
    async def check_functional_perms(self, permissions: Set[Permission], target):
        pass


class GlobPatternFunctionalAuthorizer(FunctionalAuthorizer):
    async def check_functional_perms(self, permissions: Set[Permission], target):
        try:
            patterns = User.get_current().extra["permissions"]
        except KeyError:
            raise RuntimeError(
                "'permissions' not set on user object, this likely indicates an incompatible AuthenticationProcessor"
            )
        missing = permissions.copy()
        for p in permissions:
            for pattern in patterns:
                if fnmatch.fnmatch(target + "/" + p, pattern):
                    missing.remove(p)
            if not missing:
                return
        raise PermissionException(missing)
