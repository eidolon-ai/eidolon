---
title: Fundamentals of Agent Architecture
description: An overview of the core concepts within EidOS.
---

Understanding the eidolon framework requires familiarity with the foundational elements of agent architecture. This section explores the key concepts, structures, and modularity mechanisms that underpin the framework, providing an architectural
blueprint for building software agents.

## AgentMachine

The **AgentMachine** serves as the operational environment where **AgentPrograms** are executed. It also defines the **AgentMemory** which serves as the underlying persistent storage accessible to anything running on the machine (agents, cpu, etc). It provides the necessary infrastructure such as process management, memory allocation, and input/output handling required for agents to perform their
tasks. In essence, the AgentMachine is akin to an operating system specifically tailored for agents, allowing them to run in isolation or collaboratively within a distributed network.

## AgentPrograms

At the core of the AgentMachine's task execution lies the **AgentProgram**, which encompasses two essential components:

- **The Runtime Code**: The executable part of the agent that contains the logic and behaviors necessary for performing the agent's functions.
- **The Specification**: A structured definition that outlines the agent's capacities, communication schemata, and interaction protocols. It acts as a blueprint, providing the necessary information to the AgentMachine for effective execution and
  collaboration with other agents.

## AgentCPU

The **AgentCPU** is the organizational nucleus of an individual AgentProgram, analogous to the central processing unit in traditional computing architecture. It coordinates all internal processing units, enabling the seamless flow of data and
instructions within the agent. The AgentCPU is composed of several key units:

- **I/O Unit**: It interfaces with the external environment, allowing the agent to send and receive messages. The I/O Unit is responsible for encoding and decoding data, ensuring that the agent can communicate with other systems and agents
  effectively.
- **LogicUnits**: These units consist of function calls or tools that provide the computational logic for executing tasks. They form the operational layer that processes inputs and generates appropriate outputs based on the agent's programming.
- **MemoryUnit**: This unit encompasses the mechanisms for storing and retrieving information critical to the agent's state and operation. It enables the agent to maintain continuity and context over its lifecycle.
- **LLMUnit**: Dedicated to facilitating interactions with large language models, the LLMUnit streamlines the communication between the agent and complex language processing services, transforming standardized requests into actionable responses.

The architecture's modularity allows developers to customize each unit, creating tailored solutions for specific tasks or operational requirements.

## Modular Design and Pluggability

One of the eidolon framework's central tenets is its modular design and the pluggability of its components. Developers can easily swap out or upgrade individual units within the AgentCPU, such as replacing a basic MemoryUnit with one that has more
sophisticated retrieval algorithms or integrating a new LogicUnit specialized for particular calculations or data processing tasks.

This modularity facilitates extensibility, allowing the agent architecture to scale and adapt as the complexity of tasks and the overall system requirements evolve. It also promotes reusability, where standardized units can be shared across multiple
AgentPrograms, enhancing development efficiency and system coherence.

## Communication and Interoperability

Agents within the eidolon framework are designed to work both independently and as part of larger, collective operations. To support this, the architecture emphasizes communication and interoperability. Agents are equipped with the capability to
exchange data and messages in a standardized format, delineated by their specifications, making it possible for them to cooperate on complex tasks or distribute workloads.

As part of this communication strategy, the AgentMachine manages the necessary networking and messaging protocols, ensuring that agents can discover each other and coordinate their actions reliably within the network.

[previous](Introduction.md) / [next](AgentProgram.md)
