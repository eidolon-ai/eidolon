import json
from typing import Literal, Optional, AsyncIterable, cast

from jinja2 import Environment, StrictUndefined, Template
from pydantic import BaseModel

from eidolon_ai_client.events import StartStreamContextEvent, ObjectOutputEvent, AgentStateEvent, EndStreamContextEvent, \
    UserInputEvent, StringOutputEvent
from eidolon_ai_client.util.logger import logger
from eidolon_ai_sdk.agent.agent import register_program, register_action
from eidolon_ai_sdk.agent.sql_agent.client import SqlClient
from eidolon_ai_sdk.agent.sql_agent.logic_unit import SqlLogicUnit
from eidolon_ai_sdk.apu.agent_io import SystemAPUMessage, UserTextAPUMessage
from eidolon_ai_sdk.apu.apu import APU
from eidolon_ai_sdk.apu.processing_unit import ProcessingUnitLocator
from eidolon_ai_sdk.system.reference_model import AnnotatedReference, Specable
from eidolon_ai_sdk.util.stream_collector import stream_manager


class SqlRequestBody(BaseModel):
    message: str
    allow_conversation: bool = True


class SqlAgentSpec(BaseModel):
    client: AnnotatedReference[SqlClient]
    apu: AnnotatedReference[APU]
    description: str = "An agent for interacting with data. Can respond to queries provided in natural language."
    system_prompt: str = """
    You are a helpful assistant that is a sql expert and helps a user query a {{ protocol }} database and analyse the response.
    
    Here is the database schema:
    {{ metadata }} 
    
    Think carefully.
    """
    user_prompt: str = "{{ message }}"
    clarification_prompt: str = "What clarifying information do you need? Phrase your response as an explicit question or several questions."
    response_prompt: str = "What is your response? Be explicit and concise."
    error_prompt: str = "An error occurred executing the query \"{{ query }}\": {{ error }}"
    num_retries: int = 9
    allow_thought: bool = True
    simplify_apu: bool = True


class SqlAgent(Specable[SqlAgentSpec]):
    _client: SqlClient
    _apu: APU
    _system_prompt: Template
    _user_prompt: Template
    _clarification_prompt: Template
    _error_prompt: Template

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._client = self.spec.client.instantiate()

        if self.spec.simplify_apu:
            if hasattr(self.spec.apu, "audio_unit"):
                self.spec.apu.audio_unit = None
            if hasattr(self.spec.apu, "image_unit"):
                self.spec.apu.image_unit = None
        self._apu = self.spec.apu.instantiate()

        if self.spec.allow_thought:
            if hasattr(self._apu, "logic_units"):
                self._apu.logic_units.append(SqlLogicUnit(client=self._client, apu=cast(self._apu, ProcessingUnitLocator)))
            else:
                raise ValueError("APU does not have logic units")
        else:
            self.spec.num_retries = 0

        environment = Environment(undefined=StrictUndefined)
        self._error_prompt = environment.from_string(self.spec.error_prompt)
        self._system_prompt = environment.from_string(self.spec.system_prompt)
        self._user_prompt = environment.from_string(self.spec.user_prompt)
        self._clarification_prompt = environment.from_string(self.spec.clarification_prompt)
        self._response_prompt = environment.from_string(self.spec.response_prompt)

    @register_program()
    @register_action("idle")
    async def query(self, process_id, agent_state, body: SqlRequestBody):
        schema = await self._client.get_schema()
        kwargs = dict(**body.model_dump(), metadata=schema, protocol=self._client.protocol)
        t = await self._apu.main_thread(process_id)
        if agent_state == "initialized":
            await t.set_boot_messages(
                prompts=[SystemAPUMessage(prompt=self._system_prompt.render(**kwargs))])
        message = UserTextAPUMessage(prompt=self._user_prompt.render(**kwargs))
        yield UserInputEvent(input=body.message)
        async for e in self.cycle(t, message, self.spec.num_retries, body=body):
            yield e

    async def cycle(self, thread, message, num_reties, body: SqlRequestBody, data_stream: Optional[AsyncIterable] = None):
        last_event = None
        output_format = self.get_response_object(body, include_validate=data_stream is not None)
        thinking_stream = thread.stream_request(prompts=[message], output_format=output_format)
        async for e in stream_manager(thinking_stream, StartStreamContextEvent(context_id='thinking', title='Thinking')):
            if isinstance(e, ObjectOutputEvent):
                last_event = e
            yield e

        if not last_event:
            raise ValueError("No response from llm")
        try:
            response = _AgentResponse(**last_event.content)
        except Exception as err:
            if num_reties > 0:
                logger.warning(f"Invalid response from llm: {last_event.content}")
                message = UserTextAPUMessage(prompt=f"Error parsing response, your response next response MUST match the following json schema: {json.dumps(output_format)}")
                async for e in self.cycle(thread, message, num_reties - 1, body=body):
                    yield e
                return
            else:
                raise err
        if data_stream and response.response_type != "confirm_query":
            num_reties -= 1

        if response.response_type == "confirm_query":
            if not data_stream:
                raise ValueError("No data stream provided to confirm")
            async for row in data_stream:
                yield ObjectOutputEvent(content=row)
            yield AgentStateEvent(state="idle") if body.allow_conversation else AgentStateEvent(state="terminated")
        elif response.response_type == "execute":
            try:
                logger.info(f"Executing query: {response.query}")
                first_row = None
                rows_generator = self._client.execute(response.query)
                async for row in rows_generator:
                    first_row = row
                    break
                if first_row:
                    prompt = UserTextAPUMessage(prompt=f"I've executed the query and received following row is the first result:\n{first_row}\n\nIs this correct? Or is there a better query I should execute to more directly answer my question?")
                else:
                    prompt = UserTextAPUMessage(prompt="I've executed the query and received no results. Is this correct? Or is there a better query I should execute to more directly answer my question?")
                async for e in self.cycle(thread, prompt, num_reties, body=body,data_stream=stream(first_row, rows_generator)):
                    yield e
            except Exception as e:
                if num_reties > 0:
                    yield StartStreamContextEvent(context_id='error', title='Error')
                    yield ObjectOutputEvent(content=dict(query=response.query, error=str(e)), stream_context='error')
                    yield EndStreamContextEvent(context_id='error')
                    message = UserTextAPUMessage(prompt=self._error_prompt.render(error=str(e), query=response.query))
                    yield UserInputEvent(input=message.prompt)
                    async for e in self.cycle(thread, message, num_reties - 1, body=body):
                        yield e
                else:
                    if body.allow_conversation:
                        yield StringOutputEvent(
                            content="I'm sorry, I'm having trouble executing a query. Can you provide more information?")
                        yield AgentStateEvent(state="idle")
                    else:
                        raise
        elif response.response_type == "clarify":
            prompt = UserTextAPUMessage(prompt=self._clarification_prompt.render(protocol=self._client.protocol))
            async for e in thread.stream_request(prompts=[prompt]):
                yield e
            yield AgentStateEvent(state="idle")
        elif response.response_type == "respond":
            prompt = UserTextAPUMessage(prompt=self._response_prompt.render(protocol=self._client.protocol))
            async for e in thread.stream_request(prompts=[prompt]):
                yield e
            yield AgentStateEvent(state="idle") if body.allow_conversation else AgentStateEvent(state="terminated")
        else:
            raise ValueError(f"Unexpected response type from llm: {response.response_type}")

    def get_response_object(self, body: SqlRequestBody, include_validate=False):
        responses = [dict(
            type="object",
            description="Suggest a query for the user to execute.",
            properties=dict(
                response_type=dict(const="execute"),
                query=dict(type="string"),
            ),
            required=["response_type", "query"],
        )]
        if body.allow_conversation:
            responses.append(dict(
                type="object",
                description="A query that will produce data that directly answers the provided question.",
                properties=dict(
                    response_type=dict(const="respond"),
                ),
                required=["response_type"],
            ))
            responses.append(dict(
                type="object",
                description="More information is required from the user to answer the provided question.",
                properties=dict(response_type=dict(const="clarify")),
                required=["response_type"],
            ))
        if include_validate:
            responses.append(dict(
                type="object",
                description="The data provided is the proper response to the user's query.",
                properties=dict(
                    response_type=dict(const="confirm_query"),
                ),
                required=["response_type"],
            ))

        if len(responses) > 1:
            return dict(anyOf=responses)
        elif len(responses) == 1:
            return responses[0]
        else:
            raise ValueError(
                "No valid response types")  # this should not be possible due to validation in SqlRequestBody


class _AgentResponse(BaseModel):
    response_type: Literal['execute', 'clarify', 'respond', 'confirm_query']
    query: Optional[str] = None


async def stream(maybe_first: Optional, rest: AsyncIterable):
    if maybe_first:
        yield maybe_first
    async for e in rest:
        yield e
