---
title: How to Build Custom Agent Templates
description: Reference - Building Custom Agent Templates
---
Eidolon defines several useful built-in [AgentTemplates](/docs/components/agents/overview) out of the box, but for domain 
specific problems, you may need to create your own.

## Why
Most projects will end up needing custom agents with domain specific logic. It is crucial for an agentic framework to be 
flexible enough to "hand over the keys" when developers just need to write their own code. Trying to incorporate this 
into an agentic framework just means creating another programing language. Nothing gained, but a lot lost. 

## How
You can create new agent templates by creating a class and decorating the methods you would like to expose
as actions. You also specify the states these actions are allowed on, and return the state the agent should transition to
after the action is complete.

```python
class CodeAgent:
    @register_action("initialized", "idle")
    async def execute(self, name: Annotated[str, Body(description="Your name", embed=True)]) -> AgentState[str]:
        """
        I greet people with a smile!
        """
        return AgentState(name="idle", data=f"Hello {name}!👋😀")
# 🚨 If you do not return an AgentState object, the agent will move to the 'terminated' state.
# ie: `return "Foo"` => `return AgentState(name="terminated", data="Foo")`
```

To use this agent template, you simply refer to it in your agent's yaml file by its fully qualified name.

```yaml
apiVersion: server.eidolonai.com/v1alpha1
kind: Agent
metadata:
  name: hello_world

spec: "components.getting_started.CodeAgent"
# 🚨 components must be available in your pythonpath
```

But wait 💭, that didn't use an LLM at all... what gives?! This is because there are no fixed patterns in Eidolon that 
you are forced to use. This also enables you to use Eidolon in tandem with any other LLM frameworks and libraries.

What is the point of this then? By defining an agent in this way, you get deployment, and more importantly inter-agent 
communication for free. So even though this "agent" is not using an LLM, other agents (and external services) can still 
communicate with it.

### LLM Based Agent Template

Ok, so now let's actually create an agent that uses an LLM. You could use langchain or even raw calls out 
to OpenAI if you want, but to fully leverage Eidolon's capabilities, you should use an [**Agent Processing Unit**](/docs/components/apu/overview/)
(APU).

The APU is Eidolon's abstraction around LLM interactions. It provides an LLM-agnostic, multi-media interface. The APU 
gives developers built-in tooling to manage memory, inter-agent-communication, logic units, metrics, and prompt engineering. 


Everything you love about Eidolon is baked into the **APU**.

```python
class QASpec(BaseModel):
  apu: AnnotatedReference[AgentProcessingUnit]


class QA(Specable[QASpec]):
  @register_program()
  async def run_tests(self, process_id) -> str:
    apu = self.spec.apu.initialize()
    thread = await apu.main_thread(process_id)
    return await thread.run_request(prompts=[
      SystemAPUMessage(prompt="You are a QA assistant responsible for validating agents and tools"),
      UserTextAPUMessage(prompt=f"Exhaustively test all of your tools and agents and report any issues"),
    ])
```

🔎 What is this `Specable` thing? Eidolon uses <a href="https://docs.pydantic.dev/latest/concepts/models/" target=_blank>Pydantic models</a> to define the spec of different resources. [Learn more about 
how references work.](/docs/howto/using_references)

### Streaming Response
LLMs can be slow, and sometimes you want to stream responses back to the user. Eidolon supports this by allowing you to 
yield events from your action. The APU can be called with stream_request to yield these events.

```python
class QASpec(BaseModel):
  apu: AnnotatedReference[AgentProcessingUnit]


class QA(Specable[QASpec]):
  def __init__(self, **kwargs):
    Specable.__init__(self, **kwargs)
    self.apu = self.spec.apu.initialize()

  @register_program()
  async def run_tests(self, process_id) -> str:
    thread = await self.apu.main_thread(process_id)
    yield StringOutputEvent(content="Beginning tests...\n")
    async for event in thread.stream_request(prompts=[
      SystemAPUMessage(prompt="You are a QA assistant responsible for validating agents and tools"),
      UserTextAPUMessage(prompt=f"Exhaustively test all of your tools and agents and report any issues"),
    ]):
      yield event
    yield StringOutputEvent(content="\nDone!")
    # While streaming yield a state event to indicate the next state.
    # Similarly to the return value, if you do not yield a state event, the agent will move to the 'terminated' state.
    yield AgentState(name="idle", data="Tests complete")
```

