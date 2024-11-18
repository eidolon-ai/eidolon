---
title: How to Build Custom Agent Templates
description: How to create custom agentic AI templates with Eidolon
---
A guide for software developers to create custom agentic AI templates with Eidolon

## Overview
Eidolon provides built-in [Agent Templates](/docs/components/agent/overview) that automate workflows and serve people. The [SimpleAgent](/docs/components/agent/simpleagent), for example, is a general-purpose, conversational agent template that can be configured at deployment to perform a wide variety of tasks. 

Sometimes, however, you have a domain-specific problem that needs a custom agent. 

Eidolon includes an <a href="https://github.com/eidolon-ai/eidolon/tree/main/sdk" target=_blank>agent SDK</a> that makes it easy for software developers to create custom agents. The ease of creating custom agent templates in Eidolon expands the reach of agentic AI to more real-world business use cases.

*Audience: software developers*

## When to Create a Custom Agent Template
- If an existing agent template works for you, but you want to extend its capabilities, attach an existing tool or consider creating a [custom tool](/docs/howto/build_custom_tools/).
- If you want an agent to behave differently to solve a specific problem, create a custom agent template.

> Not sure how tools can extend an agent's capabilities? See [Eidolon's pre-built tools](/docs/components/logicunit/overview) for some examples. (*Note: tools were formerly referred to as "LogicUnits".*)

## Building a Custom Agent Template
For this example, you'll create a custom agent template that plans responses before executing them.

Notes:
> A completed example is available for reference at <a href="https://github.com/eidolon-ai/howto-custom-agent" target=_blank>Eidolon's github page</a>.
 
> This guide assumes you have an Eidolon **agent-machine** running. If you don't, create a new GitHub repository using the [agent-machine template](https://github.com/new?template_name=agent-machine&template_owner=eidolon-ai). Then clone your repository to your local machine and follow the steps below.

🚨 All commands assume you are in the root directory of your **agent-machine** repository.

### 1. Define the Configuration
Create a new file `components/planning_agent.py` to implement our custom agent template.

```bash
touch components/planning_agent.py
```

Edit `planning_agent.py` to create the agent template configuration. Extend the `AgentBuilder` class as follows:

```python
from eidolon_ai_sdk.system.agent_builder import AgentBuilder

class PlanningAgent(AgentBuilder):
    planning_system_prompt: str = (
        "You are a helpful assistant. Users will come to you with questions. "
        "You will respond with a list of steps to follow when answering the question. "
        "Consider available tools when creating a plan, but do not execute them. "
        "Think carefully."
    )
    agent_system_prompt: str = "You are a helpful assistant"
    user_prompt_template: str = "{user_message}\n\nFollow the execution plan below:\n{steps}"
```

The <a href="https://github.com/eidolon-ai/eidolon/blob/main/sdk/eidolon_ai_sdk/system/agent_builder.py" target=_blank>AgentBuilder</a> provides configuration defaults for core capabilities:
- `apu`: Makes LLM calls without managing state or model-specific behavior
- `agent_refs`: Communicates with other agents
- `tools`: Adds additional capabilities

These built-in capabilities make your job as a developer faster and easier without compromising flexibility.

### 2. Add Agent Actions

Update the imports section at the top of the file. Import Eidolon and any other libraries needed for agent actions.

```python
# ...
from typing import List, Annotated
from fastapi import Body
from eidolon_ai_sdk.apu.apu import APU, Thread
from eidolon_ai_sdk.apu.agent_io import UserTextAPUMessage, SystemAPUMessage
from eidolon_ai_client.events import AgentStateEvent
```
Define actions for your agent as separate functions decorated with your agent template:

```python
@PlanningAgent.action(allowed_states=["initialized", "idle"])
async def converse(process_id: str, user_message: Annotated[str, Body()], spec: PlanningAgent):
  """Respond to user messages after creating an execution plan."""
  # Create a response plan
  apu: APU = spec.apu_instance()
  planning_thread: Thread = apu.new_thread(process_id)
  steps: List[str] = await planning_thread.run_request(
    prompts=[
      SystemAPUMessage(prompt=spec.planning_system_prompt),
      UserTextAPUMessage(prompt=user_message)
    ],
    output_format=List[str]
  )

  # Execute the plan
  steps_formatted = "\n".join([f"<step>{step}</step>" for step in steps])
  user_prompt = spec.user_prompt_template.format(user_message=user_message, steps=steps_formatted)
  async for event in apu.main_thread(process_id).stream_request(
    boot_messages=[SystemAPUMessage(prompt=spec.agent_system_prompt)],
    prompts=[UserTextAPUMessage(prompt=user_prompt)]
  ):
    yield event
  yield AgentStateEvent(state="idle")
```
#### Notes:
> The action `name`, `description`, and `body` are automatically built using the function 
signature. `name` and `description` come from the function name and docstrings respectively (but can be overridden by parameter), 
while `body` is determined by how <a href="https://fastapi.tiangolo.com/" target=_blank>FastAPI</a> interprets the function signature.

> The `APU` (Agent Processing Unit) is at the center of the Eidolon AI SDK. It allows you to make LLM calls without needing to keep
track of state or model capabilities. It is a multi-modal, model-agnostic interface. To learn more, see the <a href="/docs/architecture/agent_apu" target=blank>architecture documentation</a> and the Eidolon blog <a href="/what_is_apu" target=_blank>What is an APU?</a>.

> `Threads` are used to manage the state of a conversation. Each thread has its own memory, so LLM requests can be 
siloed. You can create new threads (with no memory), or clone an existing thread to reuse its previous memories without 
adding to them.

### 3. Using Your Custom Agent Template
To use your custom agent template, create a new agent resource and reference the `PlanningAgent` 
implementation by its <a href="https://peps.python.org/pep-3155" target=_blank>Fully Qualified Name (FQN)</a>:

```bash
touch resources/planning_agent.eidolon.yaml
```

```yaml
apiVersion: server.eidolonai.com/v1alpha1
kind: Agent
metadata:
  name: planning-agent # The name you give your agent for deployment. You can use hyphens, but no underscores, spaces, or other punctuation.
spec:
  # Implementation is the FQN of your agent template class.
  implementation: components.planning_agent.PlanningAgent
  description: "Custom agent that plans before responding"  # Optional: Override default configuration
```

> The FQN is the complete import path to your agent template class, which must be on the server's `PYTHONPATH`

### 4. Build and Deploy
Build and deploy your agent to the Eidolon server by running the script at the root of your **agent-machine**. Your custom agent will now start planning responses before executing them.

```bash
make docker-serve
```
## Add Dynamic Actions

To take this example to the next level, you can code the agent to dynamically configure actions based on runtime values.

In the example below, `description` is added to the `PlanningAgent` spec. Compare this with the code in step [1. Define the Configuration](#1-define-the-configuration).

```python
class PlanningAgent(AgentBuilder):
    description: str = "Custom agent that plans before responding"
```

The outer `build_actions` function can dynamically modify the action based on the value of `spec.description`. Compare this with the code in step [2. Add Agent Actions](#2-add-agent-actions)

```python
@PlanningAgent.dynamic_contract
def build_actions(spec: PlanningAgent):
    @PlanningAgent.action(description=spec.description, allowed_states=["initialized", "idle"])
    async def converse(process_id: str, user_message: Annotated[str, Body()], spec: PlanningAgent):
        ...
```
