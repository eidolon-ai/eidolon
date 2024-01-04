import uuid
from jinja2 import Environment, StrictUndefined
from pydantic import Field
from typing import List

from eidos_sdk.agent.retriever_agent.question_transformer import QuestionTransformerSpec, QuestionTransformer
from eidos_sdk.cpu.agent_cpu import AgentCPU
from eidos_sdk.cpu.agent_io import UserTextCPUMessage
from eidos_sdk.cpu.no_memory_cpu import NoMemoryCPU
from eidos_sdk.system.reference_model import Specable, AnnotatedReference


class HydeQuestionTransformerSpec(QuestionTransformerSpec):
    cpu: AnnotatedReference[AgentCPU, NoMemoryCPU]
    prompt: str = Field(
        default="Please write a passage to answer the question \nQuestion: {{question}}?\nPassage:",
        description="The prompt to be used for the question transformer. This should be a template where the user question is the field {{question}}",
    )


class HydeQuestionTransformer(QuestionTransformer, Specable[HydeQuestionTransformerSpec]):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cpu = self.spec.cpu.instantiate()

    async def transform(self, question: str) -> List[str]:
        thread = await self.cpu.main_thread(str(uuid.uuid4()))
        env = Environment(undefined=StrictUndefined)
        userPrompt = env.from_string(self.spec.prompt).render(question=question)
        response = await thread.schedule_request(prompts=[UserTextCPUMessage(prompt=userPrompt)], output_format="str")

        return [response]
