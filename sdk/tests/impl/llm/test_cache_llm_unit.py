import hashlib
import json
from typing import List
from unittest.mock import MagicMock, Mock

import pytest

from eidos.cpu.call_context import CallContext
from eidos.cpu.llm_message import AssistantMessage, SystemMessage
from eidos.cpu.llm_unit import LLMCallFunction
from eidos.memory.in_memory_file_memory import InMemoryFileMemory, InMemoryFileMemoryConfig
from eidos.cpu.llm import CacheLLMSpec, CacheLLM


# Assuming 'your_llm_reference' and 'your_module' are placeholders for actual implementations

class TestCacheLLM:
    @pytest.fixture
    def file_memory(self):
        return InMemoryFileMemory(spec=InMemoryFileMemoryConfig())

    @pytest.fixture
    def llm_mock(self):
        async def execute_llm(call_context: CallContext, inMessages: List[SystemMessage], inTools: List[LLMCallFunction], output_format: dict) -> AssistantMessage:
            return AssistantMessage(content={"response": "Test response"}, tool_calls=[])

        mock = MagicMock()
        mock.execute_llm = execute_llm
        return mock

    @pytest.fixture
    def cache_llm_spec(self):
        return CacheLLMSpec(dir="test_cache")

    @pytest.fixture
    def cache_llm_unit(self, cache_llm_spec, file_memory, llm_mock):
        memoryMock = Mock()
        memoryMock.file_memory = file_memory
        llm = CacheLLM(spec=cache_llm_spec, agent_memory=memoryMock, processing_unit_locator=None)
        llm.llm = llm_mock
        return llm

    @pytest.fixture
    def call_context(self):
        return CallContext(process_id="test_process_id", thread_id="test_thread_id")

    @pytest.mark.asyncio
    async def test_cache_creation(self, cache_llm_unit):
        # Test if the cache directory is created
        assert cache_llm_unit.memory.file_memory.exists(cache_llm_unit.dir)

    @pytest.mark.asyncio
    async def test_valid_llm_call_and_caching(self, cache_llm_unit, call_context):
        system_message = SystemMessage(content="Test message", is_boot_message=False)
        response = await cache_llm_unit.execute_llm(call_context, [system_message], [], {})

        assert isinstance(response, AssistantMessage)
        # Additional checks for response content can be added here

        # Check if the response is cached
        combined_str = ''.join(message.model_dump_json() for message in [system_message]) + \
                       ''.join(tool.model_dump_json() for tool in []) + \
                       json.dumps({})
        hash_object = hashlib.sha256()
        hash_object.update(combined_str.encode())
        hash_hex = hash_object.hexdigest()
        file_name = f"{cache_llm_unit.dir}/{hash_hex}.json"
        assert cache_llm_unit.memory.file_memory.exists(file_name)

    @pytest.mark.asyncio
    async def test_cache_retrieval(self, cache_llm_unit, call_context):
        system_message = SystemMessage(content="Test message for cache retrieval", is_boot_message=False)

        # First call to cache the response
        await cache_llm_unit.execute_llm(call_context, [system_message], [], {})

        # Second call should retrieve from cache
        response = await cache_llm_unit.execute_llm(call_context, [system_message], [], {})
        assert isinstance(response, AssistantMessage)
        # Additional checks to ensure the response is from cache can be added here

    @pytest.mark.asyncio
    async def test_cache_miss(self, cache_llm_unit, call_context):
        new_system_message = SystemMessage(content="New message for cache miss test", is_boot_message=False)
        response = await cache_llm_unit.execute_llm(call_context, [new_system_message], [], {})

        assert isinstance(response, AssistantMessage)

    @pytest.mark.asyncio
    async def test_cache_integrity(self, cache_llm_unit, call_context):
        system_message = SystemMessage(content="Message for cache integrity test", is_boot_message=False)
        expected_response = await cache_llm_unit.execute_llm(call_context, [system_message], [], {})

        combined_str = ''.join(message.model_dump_json() for message in [system_message]) + \
                       ''.join(tool.model_dump_json() for tool in []) + \
                       json.dumps({})
        hash_object = hashlib.sha256()
        hash_object.update(combined_str.encode())
        hash_hex = hash_object.hexdigest()
        file_name = f"{cache_llm_unit.dir}/{hash_hex}.json"

        cached_response = json.loads(cache_llm_unit.memory.file_memory.read_file(file_name).decode())
        assert cached_response == expected_response.model_dump()
