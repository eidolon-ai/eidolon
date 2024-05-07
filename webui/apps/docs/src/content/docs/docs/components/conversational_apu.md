---
title: AgentProcessingUnit (APU)
description: Component - AgentProcessingUnit (APU)


---
The ConversationalAPU (Agent Processing Unit) allows for multiple llm support including multimedia support and function 
calling (even if the llm does not support it). It does the by defining units that can patch in missing functionality for
the llm. For example, defining an image_unit will allow that image unit to describe an image for you llm, allowing even 
a small model to understand the image and respond to it.

## Basic Flow
The llm_unit will be called all the messages retrieved from memory (as controlled 
by the memory unit), all new messages, and the tools dynamically created from the logic_units. If the llm_unit executes 
any tools, it will be fed the response(s) and be executed again. When done the response is returned (or streamed).

## Specifications

| Key                | Description                                                                                                                                                                                                                          |
|--------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| io_unit            | `type`: Reference[IOUnit]<br/>`Default`: Reference[IOUnit]<br/>`Description:` Manages the ingress and egress of data, converting messages to and from formats understandable by both the agent and external entities.                |
| memory_unit        | `type`: Reference[MemoryUnit]<br/>`Default`: Reference[MemoryUnit]<br/>`Description:` Archives and retrieves messages exchanged during agent interactions, crucial for maintaining conversation history and context-aware responses. |
| logic_units        | `type`: List[Reference[LogicUnit]]<br/>`Default`: []<br/>`Description:` Hosts the essential logic for task execution, enabling the agent to perform computations and other actions.                                                  |
| llm_unit           | `type`: Reference[LLMUnit]<br/>`Default`: Reference[LLMUnit]<br/>`Description:` Interacts with Language Learning Models (LLMs), managing the complexities of forming requests and interpreting responses.                            |
| audio_unit         | `type`: Optional[Reference[AudioUnit]]<br/>`Default`: None<br/>`Description:` Processes audio inputs and outputs, integrated depending on the specific requirements of the deployment.                                               |
| image_unit         | `type`: Optional[Reference[ImageUnit]]<br/>`Default`: None<br/>`Description:` Handles image processing tasks, integrated based on the deployment needs.                                                                              |
| document_processor | `type`: Reference[DocumentProcessor]<br/>`Default`: Reference[DocumentProcessor]<br/>`Description:` Manages document-related tasks within the agent's operational scope.                                                             |
