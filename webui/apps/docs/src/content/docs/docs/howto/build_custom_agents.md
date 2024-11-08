---
title: How to Build Custom Agent Templates
description: Reference - Building Custom Agent Templates
---
# 🚨Work In Progress 🛠️

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

## 1. Defining an Agent Template Configuration

To create a new agent template, extend the `AgentBulder` class with your template's configuration. This is just a 
pydantic BaseModel, so we can define the configuration as you are used to with 
[pydantic](https://docs.pydantic.dev/latest/).

```python
from eidolon_ai_sdk.system.agent_builder import AgentBuilder

class MyValidatingAgent(AgentBuilder):
    system_prompt: str = "You are a helpful assistant"
    validation_uri: str
```

The AgentBuilder will also add an apu to your custom agent so that we can use make our LLM calls without needing to keep 
track of state or llm specific behavior like tool definitions, json mode, or multimedia support.

## 2. Adding an action to your agent

Now that we have defined our agent template's configuration, we can add an action to our agent. Since this is a simple 
chatbot, we will just add a single action `converse`.

```python
from eidolon_ai_sdk.apu.apu import APU, Thread
from eidolon_ai_sdk.apu.agent_io import UserTextAPUMessage

@MyValidatingAgent.action(description="Generate a title for the conversation", allowed_states=["initialized", "idle"])
async def converse(process_id: str, user_message: Annotated[str, Body()], spec: MyValidatingAgent):
    apu: APU = spec.apu_instance()
    thread: Thread = await apu.get_thread(process_id)
    async for event in thread.stream_request(prompts=[UserTextAPUMessage(prompt=user_message)]):
        if event.message:
            print(event.message)
```
