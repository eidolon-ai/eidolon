import asyncio
import json
import time
from io import IOBase
from typing import List, Dict, Any, Type, Optional, Literal, Union

from openai import AsyncOpenAI
from openai.types.beta import Assistant
from openai.types.beta.assistant_create_params import ToolAssistantToolsFunction
from openai.types.beta.threads import ThreadMessage
from openai.types.beta.threads.run_submit_tool_outputs_params import ToolOutput
from pydantic import Field

from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.cpu.agent_cpu import AgentCPUSpec, AgentCPU, Thread
from eidolon_ai_sdk.cpu.agent_io import CPUMessageTypes
from eidolon_ai_sdk.cpu.call_context import CallContext
from eidolon_ai_sdk.cpu.llm_message import ToolResponseMessage, LLMMessage
from eidolon_ai_sdk.cpu.logic_unit import LogicUnit, LLMToolWrapper
from eidolon_ai_sdk.cpu.processing_unit import ProcessingUnitLocator, PU_T
from eidolon_ai_sdk.system.reference_model import Specable, Reference
from eidolon_ai_sdk.util.logger import logger


class OpenAIAssistantsCPUSpec(AgentCPUSpec):
    logic_units: List[Reference[LogicUnit]] = []
    model: str = Field(default="gpt-4-1106-preview", description="The model to use for the LLM.")
    temperature: float = 0.3
    max_wait_time_secs: int = 600
    llm_poll_interval_ms: int = 500
    enable_retrieval: bool = True
    enable_code_interpreter: bool = True


class OpenAIAssistantsCPU(AgentCPU, Specable[OpenAIAssistantsCPUSpec], ProcessingUnitLocator):
    llm: AsyncOpenAI = None
    logic_units: List[LogicUnit] = None

    def __init__(self, spec: OpenAIAssistantsCPUSpec = None):
        super().__init__(spec)
        self.tool_defs = None
        kwargs = dict(processing_unit_locator=self)
        self.logic_units = [logic_unit.instantiate(**kwargs) for logic_unit in self.spec.logic_units]

    def locate_unit(self, unit_type: Type[PU_T]) -> PU_T:
        found = super().locate_unit(unit_type)
        return found if found else self._locate_unit(unit_type)

    def _locate_unit(self, unit_type: Type[PU_T]) -> Optional[PU_T]:
        for unit in self.logic_units:
            if isinstance(unit, unit_type):
                return unit
        raise ValueError(f"Could not locate {unit_type}")

    def _getLLM(self):
        if not self.llm:
            self.llm = AsyncOpenAI()
        return self.llm

    async def processFile(self, prompt: CPUMessageTypes) -> str:
        # rip out the image messages, store them in the file system, and replace them file Ids
        # collect the user messages
        llm = self._getLLM()
        image_file: IOBase = prompt.image
        # read the prompt.image file into memory
        image_data = image_file.read()
        file = await llm.files.create(file=image_data, purpose="assistants")
        return file.id

    async def get_or_create_assistant(
        self, call_context: CallContext, system_message: str = "", file_ids=None
    ) -> (Assistant, str):
        # fetch the existing conversation from symbolic memory
        existingConversation = await AgentOS.symbolic_memory.find_one(
            "open_ai_conversations",
            {
                "process_id": call_context.process_id,
                "thread_id": call_context.thread_id,
            },
        )

        llm = self._getLLM()
        if existingConversation:
            assistant_thread_id = existingConversation["assistant_thread_id"]
            assistant = await llm.beta.assistants.retrieve(existingConversation["assistant_id"])
            return assistant, assistant_thread_id

        request = {"model": self.spec.model}
        if len(system_message) > 0:
            request["instructions"] = system_message

        if file_ids and len(file_ids) > 0:
            request["file_ids"] = file_ids

        logger.info("creating assistant with request " + str(request))
        assistant = await llm.beta.assistants.create(**request)
        thread = await llm.beta.threads.create()

        await AgentOS.symbolic_memory.insert_one(
            "open_ai_conversations",
            {
                "process_id": call_context.process_id,
                "thread_id": call_context.thread_id,
                "assistant_id": assistant.id,
                "assistant_thread_id": thread.id,
            },
        )

        return assistant, thread.id

    async def set_boot_messages(self, call_context: CallContext, boot_messages: List[CPUMessageTypes]):
        # separate out the system messages from the user messages
        system_message: str = ""
        user_messages = []
        file_ids = []
        for message in boot_messages:
            if message.type == "system":
                system_message += message.prompt + "\n"
            elif message.type == "user":
                user_messages.append(message.prompt)
            elif message.type == "image":
                file_ids.append(await self.processFile(message))
            else:
                raise ValueError(f"Unknown message type {message.type}")

        assistant, thread_id = await self.get_or_create_assistant(call_context, system_message, file_ids)
        llm = self._getLLM()
        for user_message in user_messages:
            await llm.beta.threads.messages.create(thread_id=thread_id, content=user_message, role="user")

    async def schedule_request(
        self,
        call_context: CallContext,
        prompts: List[CPUMessageTypes],
        output_format: Union[Literal["str"], Dict[str, Any]],
    ) -> Any:
        # separate out the system messages from the user messages
        user_messages = []
        file_ids = []
        for message in prompts:
            if message.type == "user":
                user_messages.append(message.prompt)
            elif message.type == "image":
                file_ids.append(await self.processFile(message))
            else:
                raise ValueError(f"Unknown message type {message.type}")
        if not output_format == "str":
            schema_message = (
                f"\nYour response MUST be valid JSON satisfying the following schema:\n{json.dumps(output_format)}."
            )
            schema_message += "\nALWAYS reply with json in the following format:\njson```<insert json here>```\n"
            user_messages.append(schema_message)

        assistant, thread_id = await self.get_or_create_assistant(call_context)
        llm = self._getLLM()
        if len(user_messages) == 0:
            user_messages.append("")

        last_message_id = None
        for idx, user_message in enumerate(user_messages):
            request = {"thread_id": thread_id, "content": user_message, "role": "user"}
            if idx == len(user_messages) - 1:
                request["file_ids"] = file_ids
            last_message = await llm.beta.threads.messages.create(**request)
            last_message_id = last_message.id

        # start the run
        return await self.run_llm_and_tools(call_context, assistant.id, thread_id, last_message_id)

    async def _get_tools_defs(self, call_context: CallContext):
        conversation = []
        conversation_from_memory = AgentOS.symbolic_memory.find(
            "open_ai_conversation_data",
            {
                "process_id": call_context.process_id,
                "thread_id": call_context.thread_id,
            },
        )
        async for item in conversation_from_memory:
            conversation.append(LLMMessage.from_dict(item["tool_result"]))

        return await LLMToolWrapper.from_logic_units(self.logic_units, conversation=conversation)

    async def run_llm_and_tools(
        self,
        call_context: CallContext,
        assistant_id: str,
        assistant_thread_id: str,
        last_message_id: str,
    ):
        llm = self._getLLM()
        tool_defs = await self._get_tools_defs(call_context)
        tools = []
        logger.info("tool defs are " + str(tool_defs.keys()))
        for tool_def in tool_defs.values():
            tools.append(
                ToolAssistantToolsFunction(
                    **{
                        "type": "function",
                        "function": {
                            "name": tool_def.llm_message.name,
                            "description": tool_def.llm_message.description,
                            "parameters": tool_def.llm_message.parameters,
                        },
                    }
                )
            )
        if self.spec.enable_retrieval:
            tools.append({"type": "retrieval"})

        if self.spec.enable_code_interpreter:
            tools.append({"type": "code_interpreter"})
        request = {"assistant_id": assistant_id, "thread_id": assistant_thread_id}
        if len(tools) > 0:
            request["tools"] = tools

        run = await llm.beta.threads.runs.create(**request)
        num_iterations = 0
        while num_iterations < self.spec.max_num_function_calls:
            run = await self.run_llm(run.id, assistant_thread_id)
            if run.status == "requires_action":
                results = []

                for tool_call in run.required_action.submit_tool_outputs.tool_calls:
                    tool_call_id = tool_call.id
                    function_call = tool_call.function
                    arguments = json.loads(function_call.arguments)
                    logger.info("executing tool " + function_call.name + " with args " + str(function_call.arguments))
                    tool_def = tool_defs[function_call.name]
                    tool_result = await tool_def.execute(call_context=call_context, args=arguments)
                    logger.info("tool result is " + str(tool_result))
                    result_as_json_str = self._to_json(tool_result)
                    message = ToolOutput(tool_call_id=tool_call_id, output=result_as_json_str)
                    message_to_store = ToolResponseMessage(
                        logic_unit_name=tool_def.logic_unit.__class__.__name__,
                        tool_call_id=tool_call_id,
                        result=result_as_json_str,
                        name=function_call.name,
                    )
                    await AgentOS.symbolic_memory.insert_one(
                        "open_ai_conversation_data",
                        {
                            "process_id": call_context.process_id,
                            "thread_id": call_context.thread_id,
                            "assistant_id": assistant_id,
                            "assistant_thread_id": assistant_thread_id,
                            "tool_call_id": tool_call_id,
                            "tool_result": message_to_store.model_dump(),
                        },
                    )
                    results.append(message)

                run = await llm.beta.threads.runs.submit_tool_outputs(
                    thread_id=assistant_thread_id, run_id=run.id, tool_outputs=results
                )
                num_iterations += 1
            else:
                messages = await llm.beta.threads.messages.list(thread_id=assistant_thread_id, before=last_message_id)
                first_item: ThreadMessage = None
                async for item in messages:
                    first_item = item
                    break

                content = ""
                for text in first_item.content:
                    if text.type == "image_url":
                        logger.warning("Unsupported image url")
                    else:
                        content += text.text.value + "\n"
                return content

        raise ValueError(f"Exceeded maximum number of function calls {self.spec.max_num_function_calls}")

    async def run_llm(self, run_id: str, thread_id: str):
        llm = self._getLLM()
        finished_states = [
            "completed",
            "requires_action",
            "cancelled",
            "failed",
            "expired",
        ]
        start_time = time.time()
        run = await llm.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
        while (time.time() - start_time) < self.spec.max_wait_time_secs:
            if run.status in finished_states:
                break
            await asyncio.sleep(self.spec.llm_poll_interval_ms / 1000)
            run = await llm.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)

        if run.status not in finished_states or run.status == "expired":
            raise RuntimeError("Timeout while waiting for LLM to finish")
        elif run.status == "requires_action":
            return run
        elif run.status == "completed":
            return run
        elif run.status == "cancelled":
            raise RuntimeError("LLM run was cancelled")
        else:
            is_rate_limit = run.last_error.code == "rate_limit"
            raise RuntimeError(
                "LLM run failed because " + run.last_error.message + (" (rate limit)" if is_rate_limit else "")
            )

    async def clone_thread(self, call_context: CallContext) -> Thread:
        pass
