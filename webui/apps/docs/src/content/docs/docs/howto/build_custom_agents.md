---
title: How to Build Custom Agent Templates
description: Reference - Building Custom Agent Templates
---

Eidolon defines several useful built-in [AgentTemplates](/docs/components/agents/overview) out of the box, but for domain 
specific problems, you may need to create your own.

## Why
Many projects will end up needing custom agents with domain specific logic. It is crucial for an agentic framework to be 
flexible enough to "hand over the keys" when developers just need to write their own code. 

## Do I need a custom tool or agent template?
If you just need enhanced capabilities, you likely just need to define a [custom tool](/docs/howto/build_custom_tools/).
Custom agent templates are for when you need to define a new agent architecture to solve a specific problem.

# How to Build Custom Agent Templates
For this example, we will create a custom agent template that will check a company specific api to validate a response 
against a company policy. Simple right? Well, let's do our validation as the results stream out.

## 1. Defining your Agent Template's Configuration

To create a new agent template, extend the `AgentBuilder` class with your template's configuration. This is just a 
pydantic BaseModel, so we can define the configuration as you are used to with 
[pydantic](https://docs.pydantic.dev/latest/).

For this example we are going to create an agent that will plan how to answer the user's question in a separate llm call 
before actually answering it. As such we will define a system prompt for planning, a system prompt for the agent, and a 
user prompt template that will be used to present the plan to the user.

```python
from eidolon_ai_sdk.system.agent_builder import AgentBuilder

class MyPlanningAgent(AgentBuilder):
    planning_system_prompt: str = "You are a helpful assistant. Users will come to you with questions. You will respond with a list of steps to follow when answering the question. Consider what tools you have available when creating a plan, but do not actually execute them. Think carefully."
    agent_system_prompt: str = "You are a helpful assistant"
    user_prompt_template: str = "{user_message}\n\nFollow the execution plan below:\n{steps}"
```

The AgentBuilder will also add an `apu` to your custom agent's template so that we can use make our LLM calls without needing to keep 
track of state or llm specific behavior like tool definitions, json mode, or multimedia support. It also comes with the 
ability to communicate with other agents (`agent_refs`), and the ability to add additional `tools`.

## 2. Adding Actions to your Agent Template

Now that we have defined our agent template's configuration, we can add an action to our agent. Since this is a simple 
chatbot, we will just add a single action `converse`.

```python
from eidolon_ai_sdk.system.agent_builder import AgentBuilder
from eidolon_ai_sdk.apu.apu import APU, Thread
from eidolon_ai_sdk.apu.agent_io import UserTextAPUMessage, SystemAPUMessage
from eidolon_ai_client.events import AgentStateEvent

class MyPlanningAgent(AgentBuilder):
    planning_prompt: str = "You are a helpful assistant. Users will come to you with questions. You will respond with a list of steps to follow when answering the question."
    system_prompt: str = "You are a helpful assistant"
    user_prompt_template: str = "{user_message}\n\nFollow the execution plan below:\n{steps}"

@MyPlanningAgent.action(description="Respond to user messages after putting together an execution plan.", allowed_states=["initialized", "idle"])
async def converse(process_id: str, user_message: Annotated[str, Body()], spec: MyPlanningAgent):
    # First, let's plan how to answer the user's question
    apu: APU = spec.apu_instance()
    planning_thread: Thread = apu.new_thread(process_id)
    steps: List[str] = await planning_thread.run_request(
      prompts=[SystemAPUMessage(prompt=spec.planning_system_prompt), UserTextAPUMessage(prompt=user_message)],
      output_format=List[str]
    )
    
    # Now that we have an execution plan, let's answer the user's question
    steps = "\n".join([f"<step>{step}</step>" for step in steps])
    async for event in apu.main_thread(process_id).stream_request(
      boot_messages=[SystemAPUMessage(prompt=spec.system_prompt)],
      prompts=[UserTextAPUMessage(prompt=spec.user_prompt_template.format(user_message=user_message, steps=steps))]
    ):
        yield event
    yield AgentStateEvent(state="idle")
```

### 2.1. State Machine:

You can see that we have defined the `allowed_states` for the action. This is because this action will only be valid 
after the process has been created (`initialized`) or is `idle`. This is a simple way to define a state machine for 
your agent. After our agent finishes responding to the user, we yield a state transition to allow our process to 
return to the `idle` state. If we do not do this it will instead move to the `terminated` state.

[//]: # (todo: add a section on state machines and link out to it)

### 2.2 APU

The APU is a powerful tool at the center of the Eidolon AI SDK. It allows you to make LLM calls without needing to keep 
track of state or model capabilities.

[//]: # (todo: add a section on the APU and link out to it)

### 2.3 Events

What are these events being yielded? This is how Eidolon supports streaming and state transitions. It also handles 
nested contexts. For example, if you wanted to see the steps being generated, you could stream that out as a nested 
context. If other agents are talking to this agent, they won't see it, but if you hook it up to the WebUI you will get
to explore the train of thought as it is created.

[//]: # (todo: add a section on events and link out to it)

## 3. Dynamically adding Actions

Now sometimes the actions you want to register may themselves rely on the Spec. For example, what if you want to make 
the action's description configurable? You can do this by dynamically adding actions to your agent template.

```python
class MyPlanningAgent(AgentBuilder):
    description: str = "Respond to user messages after putting together an execution plan."
    ...
    
@MyPlanningAgent.dynamic_contract
def build_actions(spec: MyPlanningAgent):
    @MyPlanningAgent.action(description=spec.description, allowed_states=["initialized", "idle"])
    async def converse(process_id: str, user_message: Annotated[str, Body()], spec: MyPlanningAgent):
        ...
```


## 4. Using your Custom Agent Template

Now that we have defined our custom agent template, we can use it in our project. To do this all we need to do is 
reference our agent by its Fully Qualified Name (FQN) in from an Agent Resource file.

```yaml
apiVersion: server.eidolonai.com/v1alpha1
kind: Agent
metadata:
  name: thoughtful-agent

spec:
  implementation: components.MyPlanningAgent
  description: My custom description override
```

Since every field in the template has a default, we don't actually need to override anything, but we can if we want to.
In this example I have overridden the `description` field.

> 🤔 How do I find my agent's Fully Qualified Name (FQN)?
> 
> This is where you would import the class normally. Make sure it is available on the `PYTHONPATH` of your Eidolon 
> Server Process.
