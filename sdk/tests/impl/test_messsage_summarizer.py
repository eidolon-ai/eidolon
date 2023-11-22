from unittest.mock import AsyncMock, MagicMock

import pytest
from bson import ObjectId
from pydantic import ValidationError

# Assume the presence of other necessary imports from eidolon_sdk
from eidolon_sdk.agent_memory import AgentMemory
from eidolon_sdk.cpu.agent_bus import CallContext
from eidolon_sdk.cpu.llm_message import SystemMessage, AssistantMessage
from eidolon_sdk.cpu.llm_unit import LLMUnit
from eidolon_sdk.impl.message_summarizer import MessageSummarizer, MessageSummarizerConfig


# Test fixtures
@pytest.fixture
def agent_memory():
    mock = MagicMock(spec=AgentMemory)
    mock.symbolic_memory = MagicMock()
    return mock


@pytest.fixture
def summarizer_config():
    return MessageSummarizerConfig(model="gpt-4-1106-preview")


@pytest.fixture
def llm_unit():
    mock = MagicMock(spec=LLMUnit)
    return mock


@pytest.fixture
def call_context():
    return CallContext(
        process_id=str(ObjectId()),
        thread_id=str(ObjectId())
    )


@pytest.fixture
def message_summarizer(agent_memory, summarizer_config):
    return MessageSummarizer(agent_memory=agent_memory, spec=summarizer_config)


def make_async_find_generator(messages):
    async def async_find_generator(_, __):
        for message in messages:
            yield message

    return async_find_generator


# The test suite
class TestMessageSummarizer:
    def test_init(self, agent_memory, summarizer_config):
        summarizer = MessageSummarizer(agent_memory=agent_memory, spec=summarizer_config)
        assert summarizer.agent_memory is agent_memory
        assert summarizer.spec is summarizer_config

    def test_config_defaults(self):
        config = MessageSummarizerConfig()
        assert config.summary_word_limit == 100

    def test_config_validation_error(self):
        with pytest.raises(ValidationError):
            MessageSummarizerConfig(summary_word_limit="not_an_int")

    @pytest.mark.asyncio
    async def test_summarize_messages_no_existing(self, message_summarizer, call_context, llm_unit):
        # Setup the mocks
        llm_unit.execute_llm = AsyncMock(return_value=SystemMessage(content="test summary"))
        message_summarizer.agent_memory.symbolic_memory.find = make_async_find_generator([])
        message_summarizer.agent_memory.symbolic_memory.update_many = AsyncMock()
        message_summarizer.agent_memory.symbolic_memory.insert_one = AsyncMock()

        # Call the method
        result = await message_summarizer.summarize_messages(call_context, llm_unit)

        # Assert the results
        assert isinstance(result, SystemMessage)
        assert result.content == "test summary"
        message_summarizer.agent_memory.symbolic_memory.update_many.assert_awaited()
        message_summarizer.agent_memory.symbolic_memory.insert_one.assert_awaited()

    @pytest.mark.asyncio
    async def test_summarize_messages_with_existing(self, message_summarizer, call_context, llm_unit):
        # Setup the mocks
        existing_message = SystemMessage(content="existing message")
        llm_unit.execute_llm = AsyncMock(return_value=AssistantMessage(content={"result": "test summary"}, tool_calls=[]))
        message_summarizer.agent_memory.symbolic_memory.find = make_async_find_generator([{"message": existing_message.model_dump()}])
        message_summarizer.agent_memory.symbolic_memory.update_many = AsyncMock()
        message_summarizer.agent_memory.symbolic_memory.insert_one = AsyncMock()

        # Call the method
        result = await message_summarizer.summarize_messages(call_context, llm_unit)

        # Assert the results
        assert isinstance(result, AssistantMessage)
        assert result.content == {"result": "test summary"}
        message_summarizer.agent_memory.symbolic_memory.update_many.assert_awaited()
        message_summarizer.agent_memory.symbolic_memory.insert_one.assert_awaited()

