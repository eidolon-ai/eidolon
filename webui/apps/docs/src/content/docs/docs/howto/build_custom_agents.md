---
title: How to Build Custom Agents
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

### 1. Define the Configuration
First, create your agent template configuration by extending the `AgentBuilder` class:

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

The `AgentBuilder` provides:
- `apu`: Make LLM calls without managing state or model-specific behavior
- `agent_refs`: Communicate with other agents
- `tools`: Add additional capabilities

### 2. Create Agent Actions
Define actions for your agent as separate functions decorated with your agent template:

```python
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

### 4. Use Your Custom Agent Template
Reference your agent template in an Agent Resource file using its [Fully Qualified Name (FQN)](#fqn):

```yaml
apiVersion: server.eidolonai.com/v1alpha1
kind: Agent
metadata:
  name: planning-agent
spec:
  # Implementation is the FQN of your agent template class.
  implementation: components.PlanningAgent
  description: "Custom agent that plans before responding"  # Optional: Override default configuration
```

> The FQN is the complete import path to your agent template class, which must be on the server's `PYTHONPATH`
