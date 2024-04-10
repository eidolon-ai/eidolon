---
title: Custom Agents
description: References - Custom Agents
---

### Code Programs
With Eidolon, you can customize your agents by defining their implementation and referencing it in a YAML file.

_hello_world.py_
```python
from typing import Annotated
from fastapi import Body
from eidolon_ai_sdk.agent.agent import register_program


class HelloWorld:
    @register_program()
    async def execute(self, name: Annotated[str, Body(description="Your name", embed=True)]) -> str:
        """
        I greet people with a smile!
        """
        return f"Hello {name}!👋😀"
```

_hello_world_agent.yaml_
```yaml
apiVersion: eidolon/v1
kind: Agent
metadata:
  name: hello_world

spec: "getting_started.hello_world.HelloWorld"
```

The python class should look very similar to a [FastAPI endpoint](https://fastapi.tiangolo.com/tutorial/first-steps/). That is all it is. You can transparently use FastAPI types and annotations to define the contract for your program. You will get the swagger ui and validation under the covers for free. This can be dynamically defined through the program or action registration decorator as well.

### Changing State and Follow Up Actions
To manage the agent's state, return an `AgentState` object with the desired state and register actions to operate on it.

_hello_world.py_
```python
from typing import Annotated
from fastapi import Body
from eidolon_ai_sdk.agent.agent import register_program, register_action, AgentState


class HelloWorld:
    @register_program()
    async def enter(self, name: Annotated[str, Body(description="Your name", embed=True)]) -> AgentState[str]:
        """
        I greet people with a smile!
        """
        return AgentState(name="shopping", data=f"Hello {name}!👋😀")

    @register_action("shopping")
    async def exit(self) -> str:
        """
        I say goodbye to people with a smile!
        """
        return "Goodbye! Don't forget your coat!👋🧥"
```

Now if you hit the `enter` endpoint, you will notice that the returned state is "shopping" instead of "terminated". You will also see that there is a follow up action `exit` available.

**Note**: Actions can operate on multiple states.

### Agent Programs
The previous example was a pure code program without access to a LLM. That is great for hello_world, but if we want to 
customize our qa_agent we will need access to our **AgentCPU**. There is a builtin objec Agent which gives you easy 
access to the AgentCPU, as well as some other niceties (like hooking up `agent_refs`). Let's reimplement our qa_agent 
with some custom logging and nicer response formatting.

_qa.py_
```python
from textwrap import dedent
from typing import Annotated, Literal, List
from fastapi import Body
from pydantic import BaseModel
from eidolon_ai_sdk.agent.agent import register_program, Agent
from eidolon_ai_sdk.cpu.agent_io import SystemCPUMessage, UserTextCPUMessage
from eidolon_ai_client.util.logger import logger


class TestCase(BaseModel):
    name: str
    details: str
    passed: bool


class QAResponse(BaseModel):
    outcome: Literal["success", "failure"]
    test_cases: List[TestCase]
    synopsis: str


system_message = dedent("""\
    You are a qa agent who is responsible for testing your tools. When asked to test
    a tool, you will call all methods related to the tool with reasonable inputs and
    determine if they are operating in a justifiable manner.""")


class QualityAssurance(Agent):
    @register_program()
    async def test(self, process_id, agent: Annotated[str, Body()]) -> QAResponse:
        thread = await self.cpu.main_thread(process_id)
        await thread.set_boot_messages([SystemCPUMessage(prompt=system_message)])
        await thread.schedule_request(prompts=[UserTextCPUMessage(prompt=f"Please test all tools related to {agent}")])
        logger.info(f"Tests Complete for {agent}")
        response: QAResponse = await thread.schedule_request(
            prompts=[UserTextCPUMessage(prompt="Please summarize your test results")],
            output_format=QAResponse,
        )
        if response.outcome != "success":
            logger.error(f"QA failed for agent {agent}, somebody fix it!\n{response.synopsis}",)
        return response
```

_qa_agent.yaml_
```yaml
apiVersion: eidolon/v1
kind: Agent
metadata:
  name: qa

spec:
  implementation: "getting_started.qa.QualityAssurance"
  description: "This is a qa agent responsible for making sure the hello_agent is functioning properly"
  agent_refs: ["hello_world"]
```

### Configuration
Make your agent a "Specable" object for customizable configurations, referenced in the YAML file. For agents it is best to extend AgentSpec since Agent itself is Specable.

_qa.py_
```python
# ...
class QASpec(AgentSpec):
    validate_agent: bool = False


class QualityAssurance(Agent, Specable[QASpec]):
    def __init__(self, **kwargs):
        Agent.__init__(self, **kwargs)

    @register_program()
    async def test(self, process_id, agent: Annotated[str, Body()]) -> QAResponse:
        if self.spec.validate_agent and agent not in self.spec.agent_refs:
            raise HTTPException(status_code=404, detail=f"Unable to communicate with {agent}")
# ...
```

_qa_agent.yaml_
```yaml
apiVersion: eidolon/v1
kind: Agent
metadata:
  name: qa

spec:
  implementation: "getting_started.qa.QualityAssurance"
  agent_refs: ["hello_world"]
  validate_agent: true
```

By making `QualityAssurance` a `Specable[QASpec]` we will validate the yaml spec against `QASpec` and pick up defaults. The spec then becomes available to use within the agent.

**Note** To define input schema, output schema, etc dynamically based on the spec, register_program and register_action both accept functions to override portions of the endpoint's contract