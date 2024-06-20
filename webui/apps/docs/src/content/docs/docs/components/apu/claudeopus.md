---
title: ClaudeOpus
description: Description of ClaudeOpus component
---

| Property                                             | Pattern | Type                                                                        | Deprecated | Definition | Title/Description      |
| ---------------------------------------------------- | ------- | --------------------------------------------------------------------------- | ---------- | ---------- | ---------------------- |
| - [implementation](#implementation )                 | No      | const                                                                       | No         | -          | ClaudeOpus             |
| - [max_num_function_calls](#max_num_function_calls ) | No      | integer                                                                     | No         | -          | Max Num Function Calls |
| - [io_unit](#io_unit )                               | No      | [Reference[IOUnit]](/docs/components/iounit/overview)                       | No         | -          | IOUnit                 |
| - [memory_unit](#memory_unit )                       | No      | [Reference[MemoryUnit]](/docs/components/memoryunit/overview)               | No         | -          | MemoryUnit             |
| - [llm_unit](#llm_unit )                             | No      | [Reference[LLMUnit]](/docs/components/llmunit/overview)                     | No         | -          | LLMUnit                |
| - [logic_units](#logic_units )                       | No      | array of [Reference[LogicUnit]](/docs/components/logicunit/overview)        | No         | -          | Logic Units            |
| - [audio_unit](#audio_unit )                         | No      | Combination                                                                 | No         | -          | -                      |
| - [image_unit](#image_unit )                         | No      | Combination                                                                 | No         | -          | -                      |
| - [record_conversation](#record_conversation )       | No      | boolean                                                                     | No         | -          | Record Conversation    |
| - [allow_tool_errors](#allow_tool_errors )           | No      | boolean                                                                     | No         | -          | Allow Tool Errors      |
| - [document_processor](#document_processor )         | No      | [Reference[DocumentProcessor]](/docs/components/documentprocessor/overview) | No         | -          | DocumentProcessor      |
| - [retriever](#retriever )                           | No      | [Reference[Retriever]](/docs/components/retriever/overview)                 | No         | -          | Retriever              |
| - [retriever_apu](#retriever_apu )                   | No      | Combination                                                                 | No         | -          | -                      |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ClaudeOpus

Specific value: `"ClaudeOpus"`

## <a name="max_num_function_calls"></a>2. Property `max_num_function_calls`

**Title:** Max Num Function Calls

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `10`      |

**Description:** The maximum number of function calls to make in a single request.

## <a name="io_unit"></a>3. Property `io_unit`

**Title:** IOUnit

|              |                                                         |
| ------------ | ------------------------------------------------------- |
| **Type**     | `[Reference[IOUnit]](/docs/components/iounit/overview)` |
| **Required** | No                                                      |
| **Default**  | `{"implementation": "IOUnit"}`                          |

**Description:** 
This is the IO unit for the APU. It is responsible for converting the prompts from the User to the LLM

This can be overridden to provide custom IO handling.

## <a name="memory_unit"></a>4. Property `memory_unit`

**Title:** MemoryUnit

|              |                                                                 |
| ------------ | --------------------------------------------------------------- |
| **Type**     | `[Reference[MemoryUnit]](/docs/components/memoryunit/overview)` |
| **Required** | No                                                              |
| **Default**  | `{"implementation": "RawMemoryUnit"}`                           |

**Description:** Overview of MemoryUnit components

## <a name="llm_unit"></a>5. Property `llm_unit`

**Title:** LLMUnit

|              |                                                                             |
| ------------ | --------------------------------------------------------------------------- |
| **Type**     | `[Reference[LLMUnit]](/docs/components/llmunit/overview)`                   |
| **Required** | No                                                                          |
| **Default**  | `{"implementation": "AnthropicLLMUnit", "model": "claude-3-opus-20240229"}` |

**Description:** Overview of LLMUnit components

## <a name="logic_units"></a>6. Property `logic_units`

**Title:** Logic Units

|              |                                                                        |
| ------------ | ---------------------------------------------------------------------- |
| **Type**     | `array of [Reference[LogicUnit]](/docs/components/logicunit/overview)` |
| **Required** | No                                                                     |
| **Default**  | `[]`                                                                   |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be | Description                      |
| ------------------------------- | -------------------------------- |
| [LogicUnit](#logic_units_items) | Overview of LogicUnit components |

### <a name="autogenerated_heading_2"></a>6.1. LogicUnit

**Title:** LogicUnit

|              |                                                               |
| ------------ | ------------------------------------------------------------- |
| **Type**     | `[Reference[LogicUnit]](/docs/components/logicunit/overview)` |
| **Required** | No                                                            |

**Description:** Overview of LogicUnit components

## <a name="audio_unit"></a>7. Property `audio_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                    |
| --------------------------------- |
| [AudioUnit](#audio_unit_anyOf_i0) |
| [item 1](#audio_unit_anyOf_i1)    |

### <a name="audio_unit_anyOf_i0"></a>7.1. Property `AudioUnit`

**Title:** AudioUnit

|              |                                                               |
| ------------ | ------------------------------------------------------------- |
| **Type**     | `[Reference[AudioUnit]](/docs/components/audiounit/overview)` |
| **Required** | No                                                            |

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
| **Default**               | `null`                                                                    |

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

|              |               |
| ------------ | ------------- |
| **Type**     | `string`      |
| **Required** | No            |
| **Default**  | `"ImageUnit"` |

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

**Title:** DocumentProcessor

|              |                                                                               |
| ------------ | ----------------------------------------------------------------------------- |
| **Type**     | `[Reference[DocumentProcessor]](/docs/components/documentprocessor/overview)` |
| **Required** | No                                                                            |
| **Default**  | `{"implementation": "DocumentProcessor"}`                                     |

**Description:** Overview of DocumentProcessor components

## <a name="retriever"></a>12. Property `retriever`

**Title:** Retriever

|              |                                                               |
| ------------ | ------------------------------------------------------------- |
| **Type**     | `[Reference[Retriever]](/docs/components/retriever/overview)` |
| **Required** | No                                                            |
| **Default**  | `{"implementation": "Retriever"}`                             |

**Description:** Overview of Retriever components

## <a name="retriever_apu"></a>13. Property `retriever_apu`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                    |
| --------------------------------- |
| [APU](#retriever_apu_anyOf_i0)    |
| [item 1](#retriever_apu_anyOf_i1) |

### <a name="retriever_apu_anyOf_i0"></a>13.1. Property `APU`

**Title:** APU

|              |                                                   |
| ------------ | ------------------------------------------------- |
| **Type**     | [`Reference[APU]`](/docs/components/apu/overview) |
| **Required** | No                                                |

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
