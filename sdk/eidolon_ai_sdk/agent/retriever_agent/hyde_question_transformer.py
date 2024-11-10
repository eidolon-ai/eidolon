from typing import List

from jinja2 import Environment, StrictUndefined
from pydantic import Field

from eidolon_ai_sdk.agent.retriever_agent.question_transformer import QuestionTransformerSpec, QuestionTransformer
from eidolon_ai_sdk.apu.agent_io import UserTextAPUMessage
from eidolon_ai_sdk.apu.apu import APU
from eidolon_ai_sdk.system.specable import Specable


class HydeQuestionTransformerSpec(QuestionTransformerSpec):
    prompt: str = Field(
        default="Please write a passage to answer the question \nQuestion: {{question}}?\nPassage:",
        description="The prompt to be used for the question transformer. This should be a template where the user question is the field {{question}}",
    )


class HydeQuestionTransformer(QuestionTransformer, Specable[HydeQuestionTransformerSpec]):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def transform(self, apu: APU, process_id: str, question: str) -> List[str]:
        thread = apu.new_thread(process_id)
        env = Environment(undefined=StrictUndefined)
        userPrompt = env.from_string(self.spec.prompt).render(question=question)
        response = await thread.run_request(prompts=[UserTextAPUMessage(prompt=userPrompt)], output_format="str")

        return [response]
