import uuid
from jinja2 import Environment, StrictUndefined
from pydantic import Field
from typing import List

from eidolon_ai_sdk.agent.retriever_agent.question_transformer import QuestionTransformerSpec, QuestionTransformer
from eidolon_ai_sdk.cpu.agent_cpu import APU
from eidolon_ai_sdk.cpu.agent_io import UserTextAPUMessage
from eidolon_ai_sdk.system.reference_model import Specable, AnnotatedReference


class HydeQuestionTransformerSpec(QuestionTransformerSpec):
    cpu: AnnotatedReference[APU]
    prompt: str = Field(
        default="Please write a passage to answer the question \nQuestion: {{question}}?\nPassage:",
        description="The prompt to be used for the question transformer. This should be a template where the user question is the field {{question}}",
    )


class HydeQuestionTransformer(QuestionTransformer, Specable[HydeQuestionTransformerSpec]):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cpu = self.spec.cpu.instantiate()
        self.cpu.record_memory = False

    async def transform(self, question: str) -> List[str]:
        thread = await self.cpu.main_thread(str(uuid.uuid4()))
        env = Environment(undefined=StrictUndefined)
        userPrompt = env.from_string(self.spec.prompt).render(question=question)
        response = await thread.run_request(prompts=[UserTextAPUMessage(prompt=userPrompt)], output_format="str")

        return [response]
