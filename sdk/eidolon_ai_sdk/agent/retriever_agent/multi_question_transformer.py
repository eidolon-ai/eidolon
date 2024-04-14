import uuid
from jinja2 import Environment, StrictUndefined
from pydantic import Field, BaseModel
from typing import List

from eidolon_ai_sdk.agent.retriever_agent.question_transformer import QuestionTransformerSpec, QuestionTransformer
from eidolon_ai_sdk.cpu.agent_cpu import APU
from eidolon_ai_sdk.cpu.agent_io import UserTextAPUMessage
from eidolon_ai_sdk.system.reference_model import Specable, AnnotatedReference


class MultiQuestionTransformerSpec(QuestionTransformerSpec):
    cpu: AnnotatedReference[APU]
    keep_original: bool = Field(default=True, description="Whether to keep the original question in the output")
    number_to_generate: int = Field(default=3, description="The number of questions to generate")
    prompt: str = Field(
        default="""You are an AI language model assistant. Your task is to generate {{number_to_generate}} different versions of the given user 
    question to retrieve relevant documents from a vector  database. By generating multiple perspectives on the user question, 
    your goal is to help the user overcome some of the limitations of distance-based similarity search. Provide these alternative 
    questions separated by newlines. Original question: {{question}}""",
        description="The prompt to be used for the question transformer. This should be a template where the user question is the field {{question}}",
    )


class QuestionList(BaseModel):
    questions: List[str]


class MultiQuestionTransformer(QuestionTransformer, Specable[MultiQuestionTransformerSpec]):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cpu = self.spec.cpu.instantiate()
        self.cpu.record_memory = False

    async def transform(self, question: str) -> List[str]:
        thread = await self.cpu.main_thread(str(uuid.uuid4()))
        env = Environment(undefined=StrictUndefined)
        userPrompt = env.from_string(self.spec.prompt).render(
            question=question, number_to_generate=self.spec.number_to_generate
        )
        response = await thread.run_request(
            prompts=[UserTextAPUMessage(prompt=userPrompt)], output_format=QuestionList.model_json_schema()
        )

        if self.spec.keep_original:
            return [question] + response["questions"]
        else:
            return response.questions
