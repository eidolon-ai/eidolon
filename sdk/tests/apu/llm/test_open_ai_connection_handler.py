import pytest
from pytest import fail
from httpx import Response, Request
from openai import AsyncOpenAI, NotFoundError

from eidolon_ai_sdk.apu.apu import APUException
from eidolon_ai_sdk.apu.llm.open_ai_connection_handler import OpenAIConnectionHandler


class TestOpenAIConnectionHandler(OpenAIConnectionHandler):
    def makeClient(self) -> AsyncOpenAI:
        raise NotFoundError(
            self.connection_response_message(),
            response=Response(
                404,
                request=Request("POST", "https://example.com")
            ),
            body=None,
        )

    def connection_response_message(self):
        return "The model `gpt-4-turbo` does not exist or you do not have access to it."


@pytest.fixture(scope="module")
async def connection():
    # noinspection PyTypeChecker
    return TestOpenAIConnectionHandler(spec=None)


async def test_not_found_response(connection, **kwargs):
    """
    Asserts that when a NotFoundException is thrown by the OpenAI client then an appropriate message is returned
    to the user as part of an APUException
    """
    try:
        await connection.completion(**kwargs)
        fail("Expected to raise APUException")
    except APUException as e:
        message = str(e)
        assert connection.connection_response_message() in message
        assert "OpenAI accounts that do not have sufficient credits may not have access to some models." in message
