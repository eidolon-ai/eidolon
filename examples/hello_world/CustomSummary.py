from typing import List

from transformers import AutoTokenizer, AutoModelWithLMHead

from eidos.cpu.agent_bus import CallContext
from eidos.cpu.llm_message import LLMMessage, AssistantMessage
from eidos.cpu.llm_unit import LLMUnit
from eidos.cpu.message_summarizer import MessageSummarizer


class CustomSummarizer(MessageSummarizer):

    async def summarize_messages(self, call_context: CallContext, existing_messages: List[LLMMessage], llm_unit: LLMUnit) -> LLMMessage:
        """
        Summarizes a list of messages into a single message using a new thread from the cpu.

        Args:
            call_context (CallContext): The current call context
            existing_messages (List[LLMMessage]): The list of messages to summarize
            llm_unit (LLMUnit): The llm unit to use to execute the llm

        Returns:
            LLMMessage: The summary of the messages
        """

        # format prompt with word limit and existing_messages using jinja2
        message = self.template.render(WORD_LIMIT=self.spec.summary_word_limit, messages=existing_messages)

        tokenizer = AutoTokenizer.from_pretrained('t5-small')
        model = AutoModelWithLMHead.from_pretrained('t5-small', return_dict=True)
        input_ids = tokenizer.encode(message, return_tensors='pt')
        outputs = model.generate(input_ids=input_ids, max_length=self.spec.summary_word_limit)
        summary = tokenizer.decode(outputs[0])

        assistant_message = AssistantMessage(content={"response": summary}, tool_calls=[])

        return assistant_message
