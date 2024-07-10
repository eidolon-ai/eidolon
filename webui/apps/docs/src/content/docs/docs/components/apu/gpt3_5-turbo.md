---
title: GPT3.5-turbo
description: Description of GPT3.5-turbo component
---

| Property                                             | Pattern | Type                         | Deprecated | Definition                                 | Title/Description                                                                                                                                                                   |
| ---------------------------------------------------- | ------- | ---------------------------- | ---------- | ------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| - [implementation](#implementation )                 | No      | const                        | No         | -                                          | GPT3.5-turbo                                                                                                                                                                        |
| - [max_num_function_calls](#max_num_function_calls ) | No      | integer                      | No         | -                                          | Max Num Function Calls                                                                                                                                                              |
| - [io_unit](#io_unit )                               | No      | Reference[IOUnit]            | No         | In [IOUnit](/docs/components/iounit/overview)            | <br />This is the IO unit for the APU. It is responsible for converting the prompts from the User to the LLM<br /><br />This can be overridden to provide custom IO handling.<br /> |
| - [memory_unit](#memory_unit )                       | No      | Reference[MemoryUnit]        | No         | In [MemoryUnit](/docs/components/memoryunit/overview)        | Overview of MemoryUnit components                                                                                                                                                   |
| - [llm_unit](#llm_unit )                             | No      | Reference[LLMUnit]           | No         | In [LLMUnit](/docs/components/llmunit/overview)           | Overview of LLMUnit components                                                                                                                                                      |
| - [logic_units](#logic_units )                       | No      | array                        | No         | -                                          | Logic Units                                                                                                                                                                         |
| - [audio_unit](#audio_unit )                         | No      | Combination                  | No         | -                                          | -                                                                                                                                                                                   |
| - [image_unit](#image_unit )                         | No      | Combination                  | No         | -                                          | -                                                                                                                                                                                   |
| - [record_conversation](#record_conversation )       | No      | boolean                      | No         | -                                          | Record Conversation                                                                                                                                                                 |
| - [allow_tool_errors](#allow_tool_errors )           | No      | boolean                      | No         | -                                          | Allow Tool Errors                                                                                                                                                                   |
| - [document_processor](#document_processor )         | No      | Reference[DocumentProcessor] | No         | In [DocumentProcessor](/docs/components/documentprocessor/overview) | Overview of DocumentProcessor components                                                                                                                                            |
| - [retriever](#retriever )                           | No      | Reference[Retriever]         | No         | In [Retriever](/docs/components/retriever/overview)         | Overview of Retriever components                                                                                                                                                    |
| - [retriever_apu](#retriever_apu )                   | No      | Combination                  | No         | -                                          | -                                                                                                                                                                                   |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** GPT3.5-turbo

Specific value: `"GPT3.5-turbo"`

## <a name="max_num_function_calls"></a>2. Property `max_num_function_calls`

**Title:** Max Num Function Calls

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `10`      |

**Description:** The maximum number of function calls to make in a single request.

## <a name="io_unit"></a>3. Property `io_unit`

|                |                                |
| -------------- | ------------------------------ |
| **Type**       | `Reference[IOUnit]`            |
| **Required**   | No                             |
| **Default**    | `{"implementation": "IOUnit"}` |
| **Defined in** | [IOUnit](/docs/components/iounit/overview)   |

**Description:** 
This is the IO unit for the APU. It is responsible for converting the prompts from the User to the LLM

This can be overridden to provide custom IO handling.

## <a name="memory_unit"></a>4. Property `memory_unit`

|                |                                    |
| -------------- | ---------------------------------- |
| **Type**       | `Reference[MemoryUnit]`            |
| **Required**   | No                                 |
| **Default**    | `{"implementation": "MemoryUnit"}` |
| **Defined in** | [MemoryUnit](/docs/components/memoryunit/overview)   |

**Description:** Overview of MemoryUnit components

## <a name="llm_unit"></a>5. Property `llm_unit`

|                |                                                             |
| -------------- | ----------------------------------------------------------- |
| **Type**       | `Reference[LLMUnit]`                                        |
| **Required**   | No                                                          |
| **Default**    | `{"implementation": "OpenAIGPT", "model": "gpt-3.5-turbo"}` |
| **Defined in** | [LLMUnit](/docs/components/llmunit/overview)                               |

**Description:** Overview of LLMUnit components

## <a name="logic_units"></a>6. Property `logic_units`

**Title:** Logic Units

|              |         |
| ------------ | ------- |
| **Type**     | `array` |
| **Required** | No      |
| **Default**  | `[]`    |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be     | Description                      |
| ----------------------------------- | -------------------------------- |
| [overview.json](#logic_units_items) | Overview of LogicUnit components |

### <a name="autogenerated_heading_2"></a>6.1. overview.json

|                |                                 |
| -------------- | ------------------------------- |
| **Type**       | `Reference[LogicUnit]`          |
| **Required**   | No                              |
| **Defined in** | [LogicUnit](/docs/components/logicunit/overview) |

**Description:** Overview of LogicUnit components

## <a name="audio_unit"></a>7. Property `audio_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"OpenAiSpeech"`                                                          |

| Any of(Option)                        |
| ------------------------------------- |
| [overview.json](#audio_unit_anyOf_i0) |
| [item 1](#audio_unit_anyOf_i1)        |

### <a name="audio_unit_anyOf_i0"></a>7.1. Property `overview.json`

|                |                                 |
| -------------- | ------------------------------- |
| **Type**       | `Reference[AudioUnit]`          |
| **Required**   | No                              |
| **Defined in** | [AudioUnit](/docs/components/audiounit/overview) |

**Description:** Overview of AudioUnit components

### <a name="audio_unit_anyOf_i1"></a>7.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

## <a name="image_unit"></a>8. Property `image_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"OpenAIImageUnit"`                                                       |

| Any of(Option)                              |
| ------------------------------------------- |
| [ImageUnit Reference](#image_unit_anyOf_i0) |
| [item 1](#image_unit_anyOf_i1)              |

### <a name="image_unit_anyOf_i0"></a>8.1. Property `ImageUnit Reference`

**Title:** ImageUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

| Property                                                 | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#image_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#image_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

#### <a name="image_unit_anyOf_i0_implementation"></a>8.1.1. Property `implementation`

**Title:** Implementation

|              |                                             |
| ------------ | ------------------------------------------- |
| **Type**     | `string`                                    |
| **Required** | No                                          |
| **Default**  | `"eidolon_ai_sdk.apu.image_unit.ImageUnit"` |

### <a name="image_unit_anyOf_i1"></a>8.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

## <a name="record_conversation"></a>9. Property `record_conversation`

**Title:** Record Conversation

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

## <a name="allow_tool_errors"></a>10. Property `allow_tool_errors`

**Title:** Allow Tool Errors

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

## <a name="document_processor"></a>11. Property `document_processor`

|                |                                           |
| -------------- | ----------------------------------------- |
| **Type**       | `Reference[DocumentProcessor]`            |
| **Required**   | No                                        |
| **Default**    | `{"implementation": "DocumentProcessor"}` |
| **Defined in** | [DocumentProcessor](/docs/components/documentprocessor/overview)   |

**Description:** Overview of DocumentProcessor components

## <a name="retriever"></a>12. Property `retriever`

|                |                                   |
| -------------- | --------------------------------- |
| **Type**       | `Reference[Retriever]`            |
| **Required**   | No                                |
| **Default**    | `{"implementation": "Retriever"}` |
| **Defined in** | [Retriever](/docs/components/retriever/overview)   |

**Description:** Overview of Retriever components

## <a name="retriever_apu"></a>13. Property `retriever_apu`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                           |
| ---------------------------------------- |
| [overview.json](#retriever_apu_anyOf_i0) |
| [item 1](#retriever_apu_anyOf_i1)        |

### <a name="retriever_apu_anyOf_i0"></a>13.1. Property `overview.json`

|                |                           |
| -------------- | ------------------------- |
| **Type**       | `Reference[APU]`          |
| **Required**   | No                        |
| **Defined in** | [APU](/docs/components/apu/overview) |

**Description:** 
The APU is the main interface for the Agent to interact with the LLM.
The APU provides a set of capabilities that encapsulate LLM functionality and creates a clear separation between business logic and the underlying LLM implementation.

To learn more, check out our blog article APU: [What is it and how does it work?](https://www.eidolonai.com/what_is_apu/).

### <a name="retriever_apu_anyOf_i1"></a>13.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

----------------------------------------------------------------------------------------------------------------------------
