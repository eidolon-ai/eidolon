---
title: ToolCallLLMWrapper
description: Description of ToolCallLLMWrapper component
---

| Property                                       | Pattern | Type               | Deprecated | Definition | Title/Description   |
| ---------------------------------------------- | ------- | ------------------ | ---------- | ---------- | ------------------- |
| - [tool_message_prompt](#tool_message_prompt ) | No      | string             | No         | -          | Tool Message Prompt |
| - [llm_unit](#llm_unit )                       | No      | [Reference[LLMUnit]](/docs/components/llmunit/overview/) | No         | -          | LLMUnit Reference   |
| - [model](#model )                             | No      | Combination        | No         | -          | -                   |

## <a name="tool_message_prompt"></a>1. Property `tool_message_prompt`

**Title:** Tool Message Prompt

|              |                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Required** | No                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Default**  | `"You must follow these instructions:\nYou can select zero or more of the above tools based on the user query\nIf there are multiple tools required, make sure a list of tools are returned in a JSON array.\nIf there is no tool that match the user request or you have already answered the question, you will respond with empty json array for the tools.\nYou can also add any additional notes or explanations in the notes field."` |

## <a name="llm_unit"></a>2. Property `llm_unit`

**Title:** LLMUnit Reference

|              |                      |
| ------------ | -------------------- |
| **Type**     | `[Reference[LLMUnit]](/docs/components/llmunit/overview/)` |
| **Required** | No                   |
| **Default**  | `"LLMUnit"`          |

## <a name="model"></a>3. Property `model`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                        |
| ------------------------------------- |
| [LLMModel Reference](#model_anyOf_i0) |
| [item 1](#model_anyOf_i1)             |

### <a name="model_anyOf_i0"></a>3.1. Property `LLMModel Reference`

**Title:** LLMModel Reference

|              |                                          |
| ------------ | ---------------------------------------- |
| **Type**     | `[Reference[LLMModel]](/docs/components/llmmodel/overview/)`                    |
| **Required** | No                                       |
| **Default**  | `"eidolon_ai_sdk.cpu.llm_unit.LLMModel"` |

### <a name="model_anyOf_i1"></a>3.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

----------------------------------------------------------------------------------------------------------------------------
