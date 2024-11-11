---
title: How to Build Custom Agent Templates
description: A guide to creating custom agent templates in Eidolon
---
A guide to creating custom agent templates in Eidolon

## Overview
While Eidolon provides several built-in [AgentTemplates](/docs/components/agents/overview), you may need to create custom agents for domain-specific problems.

## When to Create a Custom Agent Template
- If you only need enhanced capabilities, consider creating a [custom tool](/docs/howto/build_custom_tools/) instead
- Create a custom agent template when you need to define a new agent architecture for a specific problem

## Building a Custom Agent Template
Let's create an example agent template that plans responses before executing them.

This guide will assume you already have an `agent-machine` that you are building with. If you don't, you create a new 
repository using the [agent-machine template](https://github.com/new?template_name=agent-machine&template_owner=eidolon-ai). 
Once you have created a new repository, clone it to your local machine and follow the steps below.

🚨 All commands will assume you are in the root directory of your agent-machine repository.

### 1. Define the Configuration
First, let's create a new file `components/planning_agent.py` to implement our Agent template.

```bash
touch components/planning_agent.py
```

Next, create your agent template configuration by extending the `AgentBuilder` class:

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

The `AgentBuilder` provides some default configuration as well that is not shown:
- `apu`: Make LLM calls without managing state or model-specific behavior
- `agent_refs`: Communicate with other agents
- `tools`: Add additional capabilities

### 2. Add Agent Action(s)
Define actions for your agent as separate functions decorated with your agent template:

```python
# ...
from typing import List, Annotated
from fastapi import Body
from eidolon_ai_sdk.apu.apu import APU, Thread
from eidolon_ai_sdk.apu.agent_io import UserTextAPUMessage, SystemAPUMessage
from eidolon_ai_client.events import AgentStateEvent

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
signature. The first two come from the function name and docstrings respectively (but can be overridden by parameter), 
while the third is determined by how [FastAPI](https://fastapi.tiangolo.com/) interprets the function signature.

> The `APU` is at the center of the Eidolon AI SDK. It allows you to make LLM calls without needing to keep
track of state or model capabilities. It is a multi-modal, model-agnostic interface.

> `Threads` are used to manage the state of a conversation. Each thread has its own memory, so llm requests can be 
siloed. You can create new threads (with no memory), or clone an existing thread to reuse it's previous memories without 
adding to them.

### 3. Add Dynamic Actions
To create actions that depend on template configuration:

```python
class PlanningAgent(AgentBuilder):
    description: str = "Custom agent that plans before responding"

@PlanningAgent.dynamic_contract
def build_actions(spec: PlanningAgent):
    @PlanningAgent.action(description=spec.description, allowed_states=["initialized", "idle"])
    async def converse(process_id: str, user_message: Annotated[str, Body()], spec: PlanningAgent):
        ...
```

### 4. Using Your Custom Agent Template
Now, to use your custom agent template, create a new agent resource and reference the PlanningAgent 
implementation by its using its [Fully Qualified Name (FQN)](https://peps.python.org/pep-3155/):

```bash
touch resources/planning_agent.eidolon.yaml
```

```yaml
apiVersion: server.eidolonai.com/v1alpha1
kind: Agent
metadata:
  name: planning-agent
spec:
  # Implementation is the FQN of your agent template class.
  implementation: components.planning_agent.PlanningAgent
  description: "Custom agent that plans before responding"  # Optional: Override default configuration
```

> The FQN is the complete import path to your agent template class, which must be on the server's `PYTHONPATH`

### 5. Build and Deploy
Finally, build and deploy your agent to the Eidolon server and your agent will now start planning responses before executing them.

```bash
make docker-deploy
```

If you want to see this in action, but don't want to build it yourself, you can find the example available on 
[github](https://github.com/eidolon-ai/howto-custom-agent).
