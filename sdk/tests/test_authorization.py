from typing import Optional, Set, List

from fastapi import HTTPException
from openai import BaseModel
from starlette.requests import Request

from eidolon_ai_client.util.request_context import User
from eidolon_ai_sdk.security.security_manager import AuthenticationProcessor, Permission, PermissionException
from eidolon_ai_sdk.system.reference_model import Specable


class TestAuthenticationProcessor(AuthenticationProcessor):
    user: User

    def __init__(self):
        self.reset()

    def reset(self):
        self.user = User(
            id="DEFAULT",
            name="default user",
            functional_permissions={"eidolon/agents/*/processes": {"create", "read", "update", "delete"}}
        )

    async def check_auth(self, request: Request) -> User:
        return TestAuthenticationProcessor.user


def test_system_health_does_not_require_permissions():
    assert False


def test_version_does_not_require_permissions():
    assert False


def test_list_processes_requires_read_permissions():
    assert False


def test_get_process_requires_read_permission():
    assert False


def test_get_process_no_read_response_matches_missing_response():
    assert False


def test_cannot_maliciously_propigate_user_from_header():
    assert False
