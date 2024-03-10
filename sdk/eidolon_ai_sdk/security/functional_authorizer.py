from __future__ import annotations

from abc import abstractmethod
from typing import Set

from eidolon_ai_sdk.security.permissions import Permission


class FunctionalAuthorizer:
    @abstractmethod
    async def check_functional_perms(self, permissions: Set[Permission], target):
        pass


class NoopFunctionalAuthorizer(FunctionalAuthorizer):
    async def check_functional_perms(self, *args, **kwargs):
        pass
