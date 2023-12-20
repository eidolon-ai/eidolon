---
title: AgentCPU
description: An overview of the AgentCPU within EidOS.
---

## Components
The AgentCPU constitutes the nucleus of a software agent within the Eidolon framework. Functioning akin to the central processing unit of a computer, the AgentCPU is tasked with orchestrating the behavior of the agent by handling tasks that span computation, memory management, conversation handling, and interaction with language models.

## Purpose and Use
The primary purpose of the AgentCPU is to serve as the central co-ordinator for various processing units that form the agent's cognitive and operational capabilities. It is designed to integrate seamlessly with Language Learning Models (LLMs) like
OpenAI's GPT models, facilitate interaction with the agent's memory systems, process input/output operations, and manage the logical functions assigned to the agent.

In practical use, the AgentCPU is deployed within an AgentMachine — a virtual environment that runs one or more instances of an AgentProgram. The AgentMachine, bolstered by the AgentOS as its runtime environment, offers the necessary services such
as process management, memory management, and I/O communication interfaces.


## Components and Operations
The AgentCPU consists of several key components, including:
- **I/O Unit:** This component is the interface for the ingress and egress of data, interpreting and converting incoming and outgoing messages to and from formats that the agent and the external world can understand.
- **MemoryUnit:** A memory management unit that archives and retrieves messages exchanged during agent interactions, playing a pivotal role in the agent's conversation history and context-aware responses.
- **LogicUnits:** Modules hosting the essential logic for task execution, enabling the agent to perform computations and other agent-defined actions.
- **LLMUnit:** A crucial unit responsible for interaction with LLMs, managing complexities of forming requests and interpreting sophisticated model responses.

These components together ensure that the agent can understand and fulfill its role within its operational context, adapting to conversational dynamics and contributing to task completion.

In the next sections, we will explore each of these components in detail, outlining their functions and capabilities.

## I/O Unit

The Input/Output Unit (IOUnit) is a core component of the AgentCPU, responsible for interfacing with external systems and the agent itself. It encapsulates the logic required to interpret incoming messages from users or other services and convert them into a structured format that can be processed by the agent. Conversely, it also formats the agent's responses for delivery to the external environment.

### Key Responsibilities

- **Message Processing**: The IOUnit takes incoming instances of `CPUMessageTypes`, which can include user-provided text, system-generated messages, or image URLs, and converts them into a list of `LLMMessage` objects suitable for further processing by the agent's language model.

- **Message Formatting**: For user messages, the IOUnit aggregates text components and images. Images are handled by writing the data to a temporary location and creating a corresponding URL.

- **File Handling**: When dealing with images, the IOUnit manages file operations, ensuring that images are properly stored and referenced using UUIDs, leveraging the file memory subsystem provided by AgentOS.

- **Response Transmission**: After processing by other components of the AgentCPU, the IOUnit's `process_response` method is involved in returning the final output back to the source of the original request.

### Implementation Details

- **Custom Message Types**: The IOUnit works with custom message classes such as `UserTextCPUMessage`, `SystemCPUMessage`, and `ImageCPUMessage`, relying on their inheritance from the base `CPUMessage` model. Each class has distinct characteristics for handling various message formats.

- **AgentOS Integration**: The IOUnit collaborates with AgentOS, particularly with the file memory module when handling temporary storage of files, such as images uploaded by users.

### Error Handling

The IOUnit includes error handling to manage unexpected message types, ensuring the robustness of message processing and enforcing the valid communication protocol expected by the AgentCPU.

By translating between raw input/output and structured representations used by agent's internal processes, the IOUnit plays a pivotal role in ensuring smooth communication and operation of the agent within its ecosystem.

## MemoryUnit

The `MemoryUnit` in the Eidolon SDK serves as an abstract base class that specifies the interface for memory storage operations within the AgentCPU framework. The primary responsibility of the MemoryUnit is to manage the recording and retrieval of
messages exchanged during agent interactions.

The `eidos/cpu/memory_unit.py` source code provides a blueprint for the essential functions a MemoryUnit implementation must provide:

- **storeMessages(CallContext, List[LLMMessage])**: This method is used to store a list of messages associated with a particular call context. It's an asynchronous method that gets passed the call context, which uniquely identifies an interaction
  sequence, along with the messages that need to be stored for that context.

- **storeBootMessages(CallContext, List[LLMMessage])**: This method is similar to `storeMessages` but is designated for storing messages that are part of the initial interaction sequence with the agent, commonly referred to as the "boot messages".
  This can include initial instructions or settings relevant to the start of a session.

- **storeAndFetch(CallContext, List[LLMMessage])**: Beyond just storing messages, this method also returns the full conversation history for the given call context. This is useful for providing a complete picture of an ongoing conversation
  immediately after new messages have been recorded.

To facilitate these functions, the MemoryUnit also requires concrete implementations of the following abstract methods:

- **writeBootMessages(CallContext, List[LLMMessage])**: An implementor of a MemoryUnit is expected to define how boot messages are stored persistently.

- **writeMessages(CallContext, List[LLMMessage])**: This method should define the strategy for storing standard messages during regular operations.

- **getConversationHistory(CallContext)**: This asynchronous method is called to retrieve the conversation history corresponding to a particular call context, providing a log of all interactions which have occurred within that session.

It is important for implementations to handle these operations efficiently to ensure they do not become bottlenecks in the performance of the agent system. Furthermore, specific implementation details such as data format standardization, error
handling, and data integrity checks are expected to be defined in the concrete classes that extend this base `MemoryUnit`. The functions define the contract that all specialized memory units must adhere to, ensuring modularity and a standardized
approach to memory handling within the AgentCPU architecture.

## LogicUnits

Within the Eidolon SDK, LogicUnits are responsible for encapsulating logic that can be executed by an agent. These are important for structuring the decision-making processes and computational logic that agents use to interact with their
environment, users, or other systems.

LogicUnits use the `llm_function` decorator to expose methods as executable actions that can be invoked by the agent's language model. Each method decorated with `@llm_function` represents a self-contained unit of logic or computation. Below are the
essential characteristics and functions of a LogicUnit within the Eidolon SDK:

### Characteristics of LogicUnits
- **Modularity:** LogicUnits define specific functionalities that are abstracted away from the rest of the system, promoting encapsulation and reuse.
- **Asynchronicity:** Methods in LogicUnits are asynchronous, which allows them to work seamlessly with other parts of the asynchronous Eidolon platform.
- **Decorators:** The `llm_function` decorator is used to signify which methods are accessible by the agent's language learning model (LLM) as callable actions.

### Functions of LogicUnits
- **Exposed Methods using llm_function:** Methods are exposed using `@llm_function` to indicate they should be callable by the agent’s LLM. These methods perform distinct actions, such as mathematical operations—addition, subtraction,
  multiplication, division—or search operations within a codebase.
- **Return Types:** These methods return various types, ranging from simple data types like floats to complex structures which may include search results, package listings, or source code content.
- **Documentation Strings:** Each method contains a documentation string (docstring) that describes its functionality, parameters, and return types. This aids in understanding the purpose and usage of the method within the SDK.

### Implementing a LogicUnit
The implementation details often involve:
1. Subclassing from `LogicUnit`.
2. Defining methods with computational logic inside the subclass. Each method should be designed to perform a standalone task.
3. Annotating these methods with `@llm_function` to enable them to be discovered and used by the agent's language model.
4. Writing docstrings for each method to explain its functionality and usage, ensuring clarity and maintainability.

In practice, a LogicUnit might define methods that can perform basic math operations or execute a code search within a directory of files. When invoked, the methods will perform their logic and return a result that the agent can use to proceed with
its interactions. Documentation for each method is crucial to maintain a clear understanding of the responsibilities and capabilities of the LogicUnit.

To summarize, LogicUnits form a fundamental component of the Eidolon SDK, providing clearly defined, modular units of logic that can be incorporated into an agent’s processes. This organized structure of logic encapsulation is key to building
versatile and intelligent agents by permitting task-specific computational procedures to be defined and executed within the agent framework.

## LLMUnit

The `LLMUnit` is a critical conceptual component of the Eidolon SDK, tasked with the management and interaction with Language Learning Models (LLMs) like OpenAI's GPT models. Here, "LLM" refers to any complex model capable of understanding and
generating human-like text. The LLMUnit is designed to be an intermediary between these sophisticated AI models, the software agent, and the tasks it needs to perform.

The LLMUnit class is an abstract base class, which means it provides a template for creating concrete subclasses that implement specific behavior. In the Eidolon SDK, the LLMUnit extends the `ProcessingUnit` class, making it part of the broader
processing framework within the agent system.

The core functionality of an LLMUnit involves its ability to execute requests using an LLM and parsing the responses from the LLM to be usable within the agent system. This involves exchanging messages in a way that an LLM can work with, dealing
with intricacies such as token limitations and formats.

Here is a deeper dive into the key abstract method within `eidos/cpu/llm_unit.py`:

- **execute_llm(CallContext, List[LLMMessage], List[LLMCallFunction], Union[Literal["str"], Dict])**: This method signature reflects its core purpose. It takes a `CallContext` which provides the context for the request, such as the current state of
  a conversation. It takes a list of `LLMMessage` objects, which represents the collected input for the LLM, and a list of `LLMCallFunction` objects which describe tools that may influence how the LLM processes the messages. The output format is
  specified, which determines how the response from the LLM should be structured, whether as a string or a more structured dict response. The return type is an `AssistantMessage`, which encapsulates the response from the LLM for use by the agent
  system.

The LLMUnit is also associated with `LLM_MAX_TOKENS`, a dictionary that maps model names to the maximum number of tokens they support—this informs how the unit will manage token budgets when generating responses from the LLM.

The subclasses of LLMUnit must implement the `execute_llm` method to be functional. This method is critical to the agent’s ability to perform complex language tasks, as it calls to the actual LLM with prepared input and processes the results into a
form that the agent can use to continue its operations.

### Key Points
- The unit handles communication between the agent and external LLMs, managing the complexities of issuing requests and interpreting responses.
- It must respect token limitations, which vary by the model used.
- As an abstract class, LLMUnit requires concrete implementations to define the specifics of communication with a given LLM.

To leverage an LLMUnit within an agent, integration with an actual LLM provider like OpenAI—through API calls or other interfaces—is necessary. Practical implementations would handle task-specific interactions, such as issuing prompts to generate
text, answering questions, or any natural language generation task aligned with the agent's functions.

In summary, the LLMUnit is a vital abstraction that enables the Eidolon SDK’s agents to tap into the capabilities of modern LLMs, thus opening pathways to rich interactive experiences and intelligent automated processes. The design of LLMUnit as a
ProcessingUnit subclass ensures that it seamlessly fits into the larger operational framework of the AgentCPU, contributing to the system's overall strength in language-based tasks.

## Additional CPU Components

Within the Eidolon SDK, the `eidos/cpu` package includes a variety of additional CPU components vital to the operation of advanced software agent systems. These components fulfill specific roles within the agent architecture, enhancing the
flexibility of agent capabilities.

##### OpenAIAssistantsCPU
The `OpenAIAssistantsCPU` is a specialized component designed to interact directly with OpenAI's suite of models. It contains functionalities like processing files for use, creating assistants based on the GPT model specified, and handling the
bootstrapping of messages.

This unit is notable for its comprehensive handling of an agent's interaction with OpenAI services, including creating and maintaining conversations, processing uploads (like images), and orchestrating the execution of tools through the assistant.
It's designed to manage not only the generation of responses based on inputs but also to operate secondary logic when the LLM requires further actions—essentially acting as a bridge between the general-purpose agent CPU and the specific requirements
of OpenAI's APIs【3†source】.

These additional CPU components underscore the SDK's commitment to offering a robust and extendable framework for agent development. Each component—be it conversational logic, summarization, or integration with third-party services like
OpenAI—serves to enhance the agent's operation, making it more adaptable, intelligent, and responsive to the demands of complex interactive tasks. The separation of these concerns into dedicated units also aligns with the SDK's modular design
philosophy, allowing developers to plug in the needed functionalities while maintaining a clean and maintainable codebase.