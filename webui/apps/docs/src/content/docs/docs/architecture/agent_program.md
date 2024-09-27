---
title: Structure of an Agent
description: An overview of the AgentProgram within Eidolon.
---

## What is an agent?

An LLM agent is:

*An AI system that goes beyond simple text production. It uses a large language model (LLM) as its central computational engine, allowing it to carry on conversations, do tasks, reason, and display a degree of autonomy.*

In fact a software agent, in general terms, is:

*A computer program that acts for a user or another program in a relationship of agency.*

Within the framework of the Eidolon platform, an Autonomous agent is a **loosely coupled program that performs a specific task**. An agent can act in concert with other agents, in a relationship of agency, to perform a more complex task. An agent might assume an overseer role for another agent, e.g. a QA agent or a manager agent, it could be a planning agent, or it could just be a skilled worker agent that performs a single task.

The construct of an agent is composed of the following elements:

- **Agent Code**: The executable part of the agent that contains the logic and behaviors necessary for performing the agent's functions.

- **Agent Specification**: A structured definition that defines the agent's abilities. The specification is defined in a YAML file and is used to configure the agent's behavior and communication schemata.

- **Agent Processing Unit (APU)**: The computational heart of an agent, analogous to a CPU in a computer. It coordinates all interaction with an LLM and other agents, enabling the seamless flow of data and instructions within the agent.

- **AgentOS**: The operating system for agents, providing the foundational runtime environment, including process management and memory management. It supports the various agent programs running within it.

Agents on the Eidolon platform are characterized by their ability to maintain and operate within various states, seamlessly transitioning between them to execute tasks and interact with users or other processes.

### Examples of Agents on Eidolon

The simplest form of an agent is epitomized by the **HelloWorld** agent:

```python
class HelloWorld:
    @register_program()
    async def execute(self, name: str) -> IdleStateRepresentation:
        return IdleStateRepresentation(welcome_message=f"Hello, World {name}!")
```

This agent takes a user-provided name and responds with a greeting—a basic demonstration of agent functionality and an entry point for understanding how Eidolon agents operate.

Notice the use of the `@register_program()` decorator, which is used to register the `execute` method as the agent's program. This decorator is used to register all agent programs, the starting point for any conversation.

Calls to methods decorated with `@register_program()` are assigned a new **process_id** and are executed in a new process. The process_id allows the agent to maintain state between calls to the program, and to execute multiple programs concurrently.

Transitioning to a more complex scenario, the **StateMachine** demonstrates an agent that manages different states, executing transitions and tasks based on input and processing rules:

```python
class StateMachine:
    @register_program()
    async def execute(self) -> AgentState[str]:
        # ...
  
    @register_action("a", "b")
    async def transform(self, requested_state: str) -> AgentState[Union[AState, BState, CState]]:
        # ...
```

This agent starts in state ‘A’ and provides mechanisms to transition to other specified states, offering an example of how stateful logic can be implemented within an agent.

Agent states are useful for managing the states of a **conversation** between two agents. As mentioned above, each call to a program is assigned a new process_id. This process_id is used to track the state of the conversation between the two agents.
A great use case for states is a manger agent. A worker agent can use a manager agent to answer questions and perform tasks. The manager agent can maintain state between calls to the worker agent, allowing it to manage the conversation and the worker agent's state.

Subsequent calls to an agent are made to an **action** defined on the agent. Action methods are decorated with `@register_action()`. All calls to actions are made with the process_id of the conversation, allowing the agent to maintain state between calls to the action.

Moving to the concept of a more self-reliant agent, the **AutonomousAgent** makes use of an `APU` to process inputs and engage in autonomous interactions:

```python
class AutonomousAgent(Agent):
    @register_program()
    @register_action("idle")
    async def converse(
        self, process_id, question: Annotated[str, Body(description="A question", embed=True)]
    ) -> AgentState[IdleStateRepresentation]:
        thread = await self.apu.main_thread(process_id)
        response = await thread.schedule_request(
            [UserTextAPUMessage(prompt=question)], IdleStateRepresentation.model_json_schema()
        )
        return AgentState(name="idle", data=IdleStateRepresentation(**response))
```

Here, the **AutonomousAgent** leverages the computational capabilities of an APU to answer questions. The `APU` is responsible for interactions with an LLM, allowing the agent to perform complex language processing tasks.
Notice how

As we ascend the complexity ladder, agents are built to handle more autonomy and computational tasks, ultimately enabling a wide span of potential applications within the Eidolon ecosystem. From the simplistic to the intricate, the agents authored

## Specification and Runtime Code
We've already seen how agents are defined in code, but let's see how they manifest themselves at configuration time in YAML. Here is the configuration for the **HelloWorld** agent:

```yaml
apiVersion: server.eidolonai.com/v1alpha1
kind: Agent
metadata:
  name: HelloWorld

implementation: "eidolon_examples.hello_world.HelloWorld.HelloWorld"
```

As you can see, this is the simplest form of an agent declaration. Notice the **kind** is set to **Agent**. This is the most basic type of agent, and it is used to define agents that implement all features on their own.
The **implementation** field points to the class that implements the agent. This class must be a subclass of `Agent` and must implement at least one program.

The **HelloWorld** agent is a good example of an agent that does not require any additional configuration. It is a self-contained agent that does not require any additional resources to operate.
However, most agents require some form of configuration to operate. This is where the agent specification comes into play. The specification is a YAML file that defines the configuration parameters for an agent.
For example, lets look at a simple agent that takes a question and returns a response:

```yaml
apiVersion: server.eidolonai.com/v1alpha1
kind: SimpleAgent

metadata:
  name: ExampleSimple

spec:
  description: "This is an example of a simple agent which can be used to create a conversational agent."
  system_prompt: "You are a machine which follows instructions and returns a summary of your actions."
  actions:
    - user_prompt: "{{instruction}}"
      input_schema:
        instruction:
        type: string
      output_schema: 'str'
      allow_file_upload: True
```

Notice the **kind** is set to **SimpleAgent**. This is a special type of agent that is used for single question agents that use an LLM to answer questions. The **spec** field contains the specification for the agent. The specification is a YAML file that defines the configuration parameters for an agent.

In this example, the specification defines the following parameters:
- **description**: A description of the agent. This is used to describe the agent to users or other agents that may use this agent.
- **system_prompt**: The system prompt given to the LLM when a conversation (process) is started.
- **user_prompt**: The user prompt given to the LLM when a conversation (process) is started. This may be parameterized with options from the input schema.
- **input_schema**: The schema for the input to the agent. This is used to create the OpenAPI schema for the agent defining how a user or another agent should interact with this agent.
- **output_schema**: The schema for the output of the agent. This can either be an object or a string. If it is an object, the output is assumed to be a json object. If it is a string, the output is assumed to be a plain string.
- **files**: The file handling mode for the agent. This can be either 'single', 'single-optional', 'multiple', or 'disable'. This defines how the agent handles files. If it is 'single', the agent will accept a single file as input. If it is 'single-optional', the agent will accept a single file as input, but it is optional. If it is 'multiple', the agent will accept multiple files as input. If it is 'disable', the agent will not accept files as input.

Even though **SimpleAgent** is a built-in agent type, there isn't any magic going on here. The **SimpleAgent** is just a subclass of `Agent` that defines a few configuration options in its specification.

```python
class SimpleAgentSpec(AgentSpec):
    description: Optional[str] = None
    system_prompt: str = (
        "You are a helpful assistant. Always use the provided tools, if appropriate, to complete the task."
    )
    agent_refs: List[str] = []
    actions: List[ActionDefinition] = [ActionDefinition()]
    apu: AnnotatedReference[APU] = None
    apus: List[NamedAPU] = []
    title_generation_mode: Literal["none", "on_request"] = "on_request"

class SimpleAgent(Specable[SimpleAgentSpec]):
    def __init__(self, spec):
        super().__init__(spec=spec)
        if self.spec.apu:
            self.apu = self.spec.apu.instantiate()
            self.apu.title = self.apu.__class__.__name__
            self._register_refs_logic_unit(self.apu, self.spec.agent_refs)
        else:
            self.apus = []
            for apu_spec in self.spec.apus:
                apu = apu_spec.apu.instantiate()
                apu.title = apu_spec.title or apu.__class__.__name__
                if apu_spec.default:
                    apu.default = True
                    self.apu = apu
                self._register_refs_logic_unit(apu, self.spec.agent_refs)
                self.apus.append(apu)
        ...
```

Any agent class can be made configurable by subclassing `Specable` and defining a specification class. The specification class is a pydantic model that defines the configuration parameters for the agent. The `Specable` class provides a `spec` property that returns the specification for the agent.
The **AgentOS** uses the specification to configure the agent. The specification is used to create the OpenAPI schema for the agent, and it is used to configure the agent's behavior at runtime.
The AgentOS maps the specification for an agent to REST endpoints that can be used to interact with the agent taking care to validate and convert the input and output to the appropriate types and call the appropriate methods on the agent.

## Conclusion
The "Structure of an Agent" section effectively introduces the various components that make up an agent within the Eidolon platform by discussing the roles and functionalities of each part. We learn about the Agent Code, which contains the logic and
behaviors necessary for the agent's operational functions, as well as the Agent Specification, which outlines the agent's abilities in a structured YAML file. The APU, acting as the computational heart, and AgentOS, serving as the foundational
runtime environment, highlight the technical aspects of how agents perform tasks and manage their states.

Several examples illustrate the range of complexity possible within the agent framework, from simple greeting responses with HelloWorld agents to state machines managing different states and transitions. Furthermore, the section delves into the
specifics of agent specifications by presenting YAML configurations and explaining the significance of each parameter.

As a conclusion to this section, we can say that an agent in the Eidolon platform is an intricate and modular construct, capable of varying degrees of autonomy and complexity. Agents are designed to interact seamlessly with users, other agents, and
the LLM, underpinned by a well-defined structure that facilitates the development and operation of versatile, task-specific programs within a larger, cohesive system. Whether dealing with simple question-answer interactions or complex, stateful
conversations, each agent is built with the core principles of modularity, flexibility, and scalability in mind, ensuring their adaptability to a wide array of applications within the platform.
