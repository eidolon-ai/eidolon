from typing import Annotated, List, Dict

from bson import ObjectId
from pydantic import Field

from eidolon_sdk.cpu.agent_bus import CallContext, BusEvent
from eidolon_sdk.cpu.llm_message import LLMMessage, SystemMessage
from eidolon_sdk.cpu.llm_unit import LLMUnit, LLMUnitConfig
from eidolon_sdk.cpu.logic_unit import LogicUnit, llm_function, LogicUnitConfig, DO_NOT_WRITE_RESPONSE

PROMPT = f"""
Your job is to summarize a history of previous messages in a conversation between an AI persona and a human.
The conversation you are given is a from a fixed context window and may not be complete.
Messages sent by the AI are marked with the 'assistant' role.
The AI 'assistant' can also make calls to functions, whose outputs can be seen in messages with the 'function' role.
Things the AI says in the message content are considered inner monologue and are not seen by the user.
The only AI messages seen by the user are from when the AI uses 'send_message'.
Messages the user sends are in the 'user' role.
The 'user' role is also used for important system events, such as login events and heartbeat events (heartbeats run the AI's program without user action, allowing the AI to act without prompting from the user sending them a message).
Summarize what happened in the conversation from the perspective of the AI (use the first person).
Keep your summary less than {{WORD_LIMIT}} words, do NOT exceed this word limit.
Only output the summary, do NOT include anything else in your output.
"""


class MessageSummarizerConfig(LogicUnitConfig):
    summary_word_limit: int = Field(default=100, description="The word limit for the summary")


class MessageSummarizer(LogicUnit):
    llm_config: LLMUnitConfig = None
    outstanding_calls: Dict[str, (CallContext, List[str])] = {}

    def _getOrFetchLLMConfig(self) -> LLMUnitConfig:
        if not self.llm_config:
            llm = self.cpu.get_processing_unit(LLMUnit.__class__)
            self.llm_config = llm.spec
        return self.llm_config

    @llm_function
    async def summarize_messages(self, call_context: Annotated[CallContext, Field(description="The current call context")]) \
            -> Annotated[LLMMessage, Field(description="The summary of the messages")]:
        """
        Summarizes a list of messages into a single message using a new thread from the cpu.

        Args:
            call_context (CallContext): The current call context

        Returns:
            LLMMessage: The summary of the messages
        """
        existingMessages = []
        async for message in self.agent_memory.symbolic_memory.find("conversation_memory", {
            "process_id": call_context.process_id,
            "thread_id": call_context.thread_id
        }):
            existingMessages.append(LLMMessage.from_dict(message["message"]))

        # todo -- handle messages that are > the max call context
        new_context = self.cpu.new_call_context(call_context)
        # store the new context as the key to an object as a local object, so we can retrieve it later in bus_read to make sure the LLM event is for us
        self.outstanding_calls[new_context.thread_id] = (call_context, [message._id for message in existingMessages])

        summarizer_message = SystemMessage(content=PROMPT)

        # get the LLMUnit from the cpu
        if not self.llm_config:
            llm = self.cpu.get_processing_unit(LLMUnit.__class__)
            self.llm_config = llm.spec

        # get the llm_read port from the llm config and call bus_write with the new context and messages
        self.request_write(BusEvent(
            new_context,
            self._getOrFetchLLMConfig().llm_read,
            existingMessages + [summarizer_message]
        ))

        return DO_NOT_WRITE_RESPONSE

    async def bus_read(self, event: BusEvent):
        if event.event_type == self._getOrFetchLLMConfig().llm_write and self.outstanding_calls.get(event.call_context.thread_id):
            call_context, message_ids = self.outstanding_calls.pop(event.call_context.thread_id)
            assistant_message = event.messages[0]
            # create a new object id for the summary message
            summary_id = str(ObjectId())
            # update existing messages and set the archive column to the new object id and insert the new message into the database with the object id all using an upsert in the db
            await self.agent_memory.symbolic_memory.update_many("conversation_memory", {
                "process_id": call_context.process_id,
                "thread_id": call_context.thread_id
            }, {
                "$set": {
                    "archive": summary_id
                }
            })

            await self.agent_memory.symbolic_memory.insert_one("conversation_memory", {
                "_id": summary_id,
                "process_id": call_context.process_id,
                "thread_id": call_context.thread_id,
                "message": assistant_message.model_dump()
            })

            # write the response to the bus
            self.write_response(call_context, "summarize_messages", {"summary": assistant_message.content})
