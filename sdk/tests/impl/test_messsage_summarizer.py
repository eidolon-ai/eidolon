from typing import Any

import pytest
from bson import ObjectId

from eidolon_sdk.agent_memory import AgentMemory
from eidolon_sdk.cpu.call_context import CallContext
from eidolon_sdk.cpu.llm_message import LLMMessage, SystemMessage
from eidolon_sdk.cpu.llm_unit import LLMUnit, LLMUnitConfig
from eidolon_sdk.impl.local_symbolic_memory import LocalSymbolicMemory
from eidolon_sdk.impl.message_summarizer import MessageSummarizer, MessageSummarizerConfig


# Assuming the necessary imports and the LocalSymbolicMemory class are already defined

@pytest.fixture
def call_context():
    return CallContext(
        process_id=str(ObjectId()),
        thread_id=str(ObjectId())
    )


@pytest.fixture
def local_symbolic_memory():
    memory = LocalSymbolicMemory()
    memory.start()
    yield memory
    memory.stop()


@pytest.fixture
def agent_memory(local_symbolic_memory):
    memory = AgentMemory(symbolic_memory=local_symbolic_memory)
    return memory


@pytest.fixture
def message_summarizer(agent_memory):
    return MessageSummarizer(agent_memory=agent_memory, spec=MessageSummarizerConfig(summary_word_limit=100))


class TestLLMUnit(LLMUnit):
    def __init__(self, config: LLMUnitConfig, agent_memory: AgentMemory, message: str):
        super().__init__(config=config, memory=agent_memory)
        self.message = message

    async def execute_llm(self, call_context: CallContext, messages: list[LLMMessage], input_data: dict[str, Any], output_format: dict[str, Any]) -> LLMMessage:
        return SystemMessage(content=self.message)


@pytest.fixture
def make_llm(agent_memory):
    def _make_llm(message: str = "test summary"):
        return TestLLMUnit(config=LLMUnitConfig(model="gpt-4-1106-preview"), agent_memory=agent_memory, message=message)

    return _make_llm


class TestMessageSummarizer:
    @pytest.mark.asyncio
    async def test_summarize_messages_no_existing(self, message_summarizer, call_context, local_symbolic_memory, make_llm):
        llm_unit = make_llm()

        # Perform the summarization
        await message_summarizer.summarize_messages(call_context, llm_unit)

        # Assert that the summary is the only message in the symbolic memory
        all_docs = [doc async for doc in local_symbolic_memory.find("conversation_memory", {})]
        assert len(all_docs) == 1
        assert all_docs[0]['message']['content'] == "test summary"

    @pytest.mark.asyncio
    async def test_summarize_messages_with_existing(self, message_summarizer, call_context, local_symbolic_memory, make_llm):
        llm_unit = make_llm()

        # Add existing messages to the symbolic memory
        await local_symbolic_memory.insert_one("conversation_memory", {
            "process_id": call_context.process_id,
            "thread_id": call_context.thread_id,
            "message": {"type": "system", "content": "existing message"}
        })

        # Perform the summarization
        await message_summarizer.summarize_messages(call_context, llm_unit)

        # Assert that the existing message is included in the summary
        summary_in_db = await local_symbolic_memory.find_one(
            "conversation_memory",
            {"process_id": call_context.process_id, "thread_id": call_context.thread_id, "archive": None}
        )
        assert summary_in_db['message']['content'] == "test summary"

    @pytest.mark.asyncio
    async def test_summarize_updates_existing_to_archived(self, message_summarizer, call_context, local_symbolic_memory, make_llm):
        llm_unit = make_llm()

        # Add existing message to the symbolic memory
        await local_symbolic_memory.insert_one("conversation_memory", {
            "process_id": call_context.process_id,
            "thread_id": call_context.thread_id,
            "message": {"type": "system", "content": "existing message"}
        })

        # Perform the summarization
        await message_summarizer.summarize_messages(call_context, llm_unit)

        # Assert that the existing message has been updated with an 'archive' field
        all_docs = [doc async for doc in local_symbolic_memory.find("conversation_memory", {})]
        for doc in all_docs:
            if doc['message']['content'] == "existing message":
                assert 'archive' in doc

    @pytest.mark.asyncio
    async def test_summarize_order_with_new_messages(self, message_summarizer, call_context, local_symbolic_memory, make_llm):
        llm_unit = make_llm()

        # Add initial messages to the symbolic memory
        await local_symbolic_memory.insert("conversation_memory", [
            {"process_id": call_context.process_id, "thread_id": call_context.thread_id, "message": {"type": "system", "content": "message 1"}},
            {"process_id": call_context.process_id, "thread_id": call_context.thread_id, "message": {"type": "system", "content": "message 2"}}
        ])

        # Perform the first summarization
        await message_summarizer.summarize_messages(call_context, llm_unit)

        # Add more messages after summarization
        await local_symbolic_memory.insert("conversation_memory", [
            {"process_id": call_context.process_id, "thread_id": call_context.thread_id, "message": {"type": "system", "content": "message 3"}},
            {"process_id": call_context.process_id, "thread_id": call_context.thread_id, "message": {"type": "system", "content": "message 4"}}
        ])

        # Perform another find to simulate the order
        all_docs = [doc async for doc in local_symbolic_memory.find("conversation_memory", {
            "process_id": call_context.process_id,
            "thread_id": call_context.thread_id,
            "archive": None
        })]

        # Assert that the summary message comes first, followed by new messages
        assert all_docs[0]['message']['content'] == "test summary"
        assert all_docs[1]['message']['content'] == "message 3"
        assert all_docs[2]['message']['content'] == "message 4"
