---
title: Next Steps
description: Dive deeper into developing with EidOS.
---

## Goals
This document serves as a hands-on overview of different features within EidOS.

## Prerequisites

* [Quickstart](https://github.com/eidolon-ai/eidOS/wiki/Quickstart): This doc assumes some level of familiarity with EidOS. The quickstart guide is a great place to start
* Python project with an eidOS dependency. If you do not have one already, use the following script to create a poetry project. It will also create some empty files.
```bash
poetry new getting_started
cd getting_started
poetry add eidos-sdk
touch getting_started/hello_world.py
touch getting_started/qa.py
mkdir resources
touch resources/qa_agent.yaml
touch resources/hello_world_agent.yaml
```

## 1. Agent Communication

EidOS simplifies agent-to-agent communication with a built-in mechanism enabling seamless interaction between agents. In the example below we will reuse the `hello_world` agent from our quickstart guide, and create a second `qa` agent who will interface with the hello world agent.

**hello_world_agent.yaml**
```yaml
apiVersion: eidolon/v1
kind: GenericAgent
metadata:
  name: hello_world

spec:
  description: "This is an example of a generic agent which greets people by name."
  system_prompt: "You are a friendly greeter who greets people by name while using emojis"
  user_prompt: "Hi, my name is {{name}}"
  input_schema:
    name:
      type: string
      description: The caller's name
```

**qa_agent.yaml**
```yaml
apiVersion: eidolon/v1
kind: GenericAgent
metadata:
  name: qa

spec:
  description: "This is a qa agent responsible for making sure the hello_agent is functioning properly"
  agent_refs: ["hello_world"]
  system_prompt: >-
    You are a qa agent who is responsible for testing your tools. When asked to test
    a tool, you will call all methods related to the tool with reasonable inputs and
    determine if they are operating in a justifiable manner. When you have performed
    all your tests, respond with "Error: {description}" if there is an issue, otherwise
    return "Success: [{test1 description, {test2 description}, ...}]"
  user_prompt: "Test the hello_world agent"
```

Now if you run your machine and hit the "question" endpoint on your qa agent, in the machine logs you should notice that there will be log lines for the hello_world agent. Your qa agent is now able to communicate with the hello_world agent! 🎉

## 2. Custom Agents

### 2.1 Code Programs
With EidOS, you can customize your agents by defining their implementation and referencing it in a YAML file.

**hello_world.py**
```python
from typing import Annotated
from fastapi import Body
from eidos_sdk.agent.agent import register_program


class HelloWorld:
    @register_program()
    async def execute(self, name: Annotated[str, Body(description="Your name", embed=True)]) -> str:
        """
        I greet people with a smile!
        """
        return f"Hello {name}!👋😀"
```

**hello_world_agent.yaml**
```yaml
apiVersion: eidolon/v1
kind: Agent
metadata:
  name: hello_world

implementation: "getting_started.getting_started.hello_world.HelloWorld"
```

The python class should look very similar to a [FastAPI endpoint](https://fastapi.tiangolo.com/tutorial/first-steps/). That is all it is. You can transparently use FastAPI types and annotations to define the contract for your program. You will get the swagger ui and validation under the covers for free. This can be dynamically defined through the program or action registration decorator as well.

### 2.2 Changing State and Follow Up Actions
To manage the agent's state, return an `AgentState` object with the desired state and register actions to operate on it.

**hello_world.py**
```python
from typing import Annotated
from fastapi import Body
from eidos_sdk.agent.agent import register_program, register_action, AgentState


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
        return "Goodbye! Don't forget your coat!👋🧥☃️😀"
```

Now if you hit the `enter` endpoint, you will notice that the returned state is "shopping" instead of "terminated". You will also see that there is a follow up action `exit` available.

**Note**: Actions can operate on multiple states.

### 2.3 Agent Programs
The previous example was a pure code program without access to a LLM. That is great for hello_world, but if we want to customize our qa_agent we will need access to our **AgentCPU**. There is a builtin objec Agent which gives you easy access to the AgentCPU, as well as some other nicities (like hooking up `agent_refs`).

**qa.py**
```python
from textwrap import dedent
from typing import Annotated, Literal, List
from fastapi import Body
from pydantic import BaseModel
from eidos_sdk.agent.agent import register_program, Agent
from eidos_sdk.cpu.agent_io import SystemCPUMessage, UserTextCPUMessage
from eidos_sdk.util.logger import logger


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

**qa_agent.yaml**
```yaml
apiVersion: eidolon/v1
kind: Agent
metadata:
  name: qa

implementation: "getting_started.getting_started.qa.QualityAssurance"
spec:
  description: "This is a qa agent responsible for making sure the hello_agent is functioning properly"
  agent_refs: ["hello_world"]
```

### 2.4 Configuration
Make your agent a "Specable" object for customizable configurations, referenced in the YAML file. For agents it is best to extend AgentSpec since Agent itself is Specable.

**qa.py**
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

**qa_agent.yaml**
```yaml
apiVersion: eidolon/v1
kind: Agent
metadata:
  name: qa

implementation: "getting_started.getting_started.qa.QualityAssurance"
spec:
  agent_refs: ["hello_world"]
  validate_agent: true
```

By making `QualityAssurance` a `Specable[QASpec]` we will validate the yaml spec against `QASpec` and pick up defaults. The spec then becomes available to use within the agent.

**Note** To define input schema, output schema, etc dynamically based on the spec, register_program and register_action both accept functions to override portions of the endpoint's contract

## 3. Pluggable Resources

### 3.1 Including Pluggable References in Configuration
Agents can include pluggable references to various components like CPUs. Let's use gpt 3.5 instead of 4 to save money and lower the temperature some for more repeatable results.

**qa_agent.yaml**
```yaml
apiVersion: eidolon/v1
implementation: getting_started.getting_started.qa.QualityAssurance
kind: Agent
metadata:
  name: qa

spec:
  agent_refs: ["hello_world"]
  cpu:
    spec:
      llm_unit:
        spec:
          force_json: 'True'
          max_tokens: '3000'
          model: gpt-3.5-turbo-1106
          temperature: '.1'
      max_num_function_calls: '20'
```

### 3.2 Named References
This is pretty verbose in our qa_agent.yaml, and would be redundant if we wanted other agents to run with the same cpu. Let's create a named resource `cpu.frugal` which we can reuse for our agents.

**frugal_cpu.yaml**
```yaml
apiVersion: eidolon/v1
kind: CPU
metadata:
  name: frugal

implementation: "eidos_sdk.cpu.conversational_agent_cpu.ConversationalAgentCPU"
spec:
  cpu:
    spec:
      llm_unit:
        spec:
          force_json: 'True'
          max_tokens: '3000'
          model: gpt-3.5-turbo-1106
          temperature: '.1'
      max_num_function_calls: '20'
```

**qa_agent.yaml**
```
apiVersion: eidolon/v1
kind: Agent
metadata:
  name: qa

implementation: getting_started.getting_started.qa.QualityAssurance
spec:
  agent_refs: ["hello_world"]
  cpu: "CPU.frugal"
```

We refer to our named resource as `{kind}.{metadata.name}`, or in this case `CPU.default`. We can create named resources for any type of `Reference` within a spec. For example, we could have created a named reference for the llm_unit instead (or in addition to) of the cpu.

## 4. Defining a Machine

Customize the server's machine by defining a "Machine" resource.

Like any other resource within EidOS, you can define your own machine as well. The primary purpose of the machine is to define shared singleton concepts like memory. Below we will use mongo for symbolic_memory rather than the in-memory implementation.

**machine.yaml**
```yaml
apiVersion: eidolon/v1
kind: Machine
spec:
  symbolic_memory:
    implementation: "eidos_sdk.memory.mongo_symbolic_memory.MongoSymbolicMemory"
    spec:
      mongo_database_name: "eidolon"
```

**Note**: Match the resource name with the flag used when starting the server. If unspecified (in either case), "DEFAULT" is used.
