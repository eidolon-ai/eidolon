from typing import List

from jinja2 import StrictUndefined, Environment
from pydantic import Field, BaseModel

from eidolon_ai_sdk.cpu.agent_cpu import APU
from eidolon_ai_sdk.cpu.agent_io import UserTextAPUMessage
from eidolon_ai_sdk.agent.tot_agent.prompts import CHECKER_PROMPT
from eidolon_ai_sdk.agent.tot_agent.thought import ThoughtValidity
from eidolon_ai_sdk.system.reference_model import Specable


class TotCheckerConfig(BaseModel):
    prompt: str = CHECKER_PROMPT
    examples: str = ""


class ToTChecker(Specable[TotCheckerConfig]):
    spec: TotCheckerConfig
    cpu: APU

    def __init__(self, cpu, spec):
        super().__init__(spec)
        self.cpu = cpu
        self.spec = spec

    """
    Tree of Thought (ToT) checker.

    This is an abstract ToT checker that can be implemented by the user. You
    can implement a simple rule-based checker or a more sophisticated
    neural network based classifier.
    """

    async def evaluate(
        self,
        process_id: str,
        problem_description: str,
        thoughts: List[str] = Field(default_factory=list),
    ) -> ThoughtValidity:
        """
        Evaluate the response to the problem description and return the solution type.
        """

        checker_prompt = (
            Environment(undefined=StrictUndefined)
            .from_string(self.spec.prompt)
            .render(
                problem=problem_description,
                thoughts=thoughts,
                examples=self.spec.examples,
            )
        )

        thread = await self.cpu.new_thread(process_id)
        resp = await thread.run_request(
            prompts=[UserTextAPUMessage(prompt=checker_prompt)],
            output_format=ThoughtValidity.model_json_schema(),
        )

        return ThoughtValidity.model_validate(resp)
