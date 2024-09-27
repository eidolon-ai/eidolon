---
title: MistralMedium
description: "Description of MistralMedium component"
---

| Property                                             | Pattern | Type                          | Deprecated | Definition | Title/Description      |
| ---------------------------------------------------- | ------- | ----------------------------- | ---------- | ---------- | ---------------------- |
| - [implementation](#implementation )                 | No      | const                         | No         | -          | -                      |
| - [max_num_function_calls](#max_num_function_calls ) | No      | integer                       | No         | -          | Max Num Function Calls |
| - [io_unit](#io_unit )                               | No      | [Reference[IOUnit]](/docs/components/iounit/overview)             | No         | -          | -                      |
| - [memory_unit](#memory_unit )                       | No      | [Reference[MemoryUnit]](/docs/components/memoryunit/overview)         | No         | -          | -                      |
| - [longterm_memory_unit](#longterm_memory_unit )     | No      | [Reference[LongTermMemoryUnit]](/docs/components/longtermmemoryunit/overview) | No         | -          | -                      |
| - [llm_unit](#llm_unit )                             | No      | [Reference[LLMUnit]](/docs/components/llmunit/overview)            | No         | -          | -                      |
| - [logic_units](#logic_units )                       | No      | array of [Reference[LogicUnit]](/docs/components/logicunit/overview) | No         | -          | Logic Units            |
| - [audio_unit](#audio_unit )                         | No      | [Reference[AudioUnit]](/docs/components/audiounit/overview)          | No         | -          | -                      |
| - [image_unit](#image_unit )                         | No      | [Reference[ImageUnit]](/docs/components/imageunit/overview)          | No         | -          | -                      |
| - [record_conversation](#record_conversation )       | No      | boolean                       | No         | -          | Record Conversation    |
| - [allow_tool_errors](#allow_tool_errors )           | No      | boolean                       | No         | -          | Allow Tool Errors      |
| - [document_processor](#document_processor )         | No      | [Reference[DocumentProcessor]](/docs/components/documentprocessor/overview)  | No         | -          | -                      |
| - [retriever](#retriever )                           | No      | [Reference[Retriever]](/docs/components/retriever/overview)          | No         | -          | -                      |
| - [retriever_apu](#retriever_apu )                   | No      | [Reference[APU]](/docs/components/apu/overview)                | No         | -          | -                      |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

Specific value: `"MistralMedium"`

## <a name="max_num_function_calls"></a>2. Property `max_num_function_calls`

**Title:** Max Num Function Calls

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `10`      |

**Description:** The maximum number of function calls to make in a single request.

## <a name="io_unit"></a>3. Property `io_unit`

|              |                                |
| ------------ | ------------------------------ |
| **Type**     | [`Reference[IOUnit]`](/docs/components/iounit/overview)            |
| **Required** | No                             |
| **Default**  | `{"implementation": "IOUnit"}` |

## <a name="memory_unit"></a>4. Property `memory_unit`

|              |                                    |
| ------------ | ---------------------------------- |
| **Type**     | [`Reference[MemoryUnit]`](/docs/components/memoryunit/overview)            |
| **Required** | No                                 |
| **Default**  | `{"implementation": "MemoryUnit"}` |

## <a name="longterm_memory_unit"></a>5. Property `longterm_memory_unit`

|              |                                 |
| ------------ | ------------------------------- |
| **Type**     | [`Reference[LongTermMemoryUnit]`](/docs/components/longtermmemoryunit/overview) |
| **Required** | No                              |
| **Default**  | `null`                          |

## <a name="llm_unit"></a>6. Property `llm_unit`

|              |                                                                      |
| ------------ | -------------------------------------------------------------------- |
| **Type**     | [`Reference[LLMUnit]`](/docs/components/llmunit/overview)                                                 |
| **Required** | No                                                                   |
| **Default**  | `{"implementation": "MistralGPT", "model": "mistral-medium-latest"}` |

## <a name="logic_units"></a>7. Property `logic_units`

**Title:** Logic Units

|              |                                 |
| ------------ | ------------------------------- |
| **Type**     | `array of [Reference[LogicUnit]](/docs/components/logicunit/overview)` |
| **Required** | No                              |
| **Default**  | `[]`                            |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be         | Description |
| --------------------------------------- | ----------- |
| [logic_units items](#logic_units_items) | -           |

### <a name="autogenerated_heading_2"></a>7.1. logic_units items

|              |                                                                 |
| ------------ | --------------------------------------------------------------- |
| **Type**     | [`Reference[LogicUnit]`](/docs/components/logicunit/overview)                                          |
| **Required** | No                                                              |
| **Default**  | `{"implementation": "eidolon_ai_sdk.apu.logic_unit.LogicUnit"}` |

## <a name="audio_unit"></a>8. Property `audio_unit`

|              |                        |
| ------------ | ---------------------- |
| **Type**     | [`Reference[AudioUnit]`](/docs/components/audiounit/overview) |
| **Required** | No                     |
| **Default**  | `null`                 |

## <a name="image_unit"></a>9. Property `image_unit`

|              |                        |
| ------------ | ---------------------- |
| **Type**     | [`Reference[ImageUnit]`](/docs/components/imageunit/overview) |
| **Required** | No                     |
| **Default**  | `null`                 |

## <a name="record_conversation"></a>10. Property `record_conversation`

**Title:** Record Conversation

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

## <a name="allow_tool_errors"></a>11. Property `allow_tool_errors`

**Title:** Allow Tool Errors

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

## <a name="document_processor"></a>12. Property `document_processor`

|              |                                           |
| ------------ | ----------------------------------------- |
| **Type**     | [`Reference[DocumentProcessor]`](/docs/components/documentprocessor/overview)            |
| **Required** | No                                        |
| **Default**  | `{"implementation": "DocumentProcessor"}` |

## <a name="retriever"></a>13. Property `retriever`

|              |                                   |
| ------------ | --------------------------------- |
| **Type**     | [`Reference[Retriever]`](/docs/components/retriever/overview)            |
| **Required** | No                                |
| **Default**  | `{"implementation": "Retriever"}` |

## <a name="retriever_apu"></a>14. Property `retriever_apu`

|              |                  |
| ------------ | ---------------- |
| **Type**     | [`Reference[APU]`](/docs/components/apu/overview) |
| **Required** | No               |
| **Default**  | `null`           |

----------------------------------------------------------------------------------------------------------------------------
