---
title: ToolCallLLMWrapper
description: Description of ToolCallLLMWrapper component
---

| Property                                       | Pattern | Type                                                    | Deprecated | Definition | Title/Description   |
| ---------------------------------------------- | ------- | ------------------------------------------------------- | ---------- | ---------- | ------------------- |
| - [implementation](#implementation )           | No      | const                                                   | No         | -          | ToolCallLLMWrapper  |
| - [tool_message_prompt](#tool_message_prompt ) | No      | string                                                  | No         | -          | Tool Message Prompt |
| - [llm_unit](#llm_unit )                       | No      | [Reference[LLMUnit]](/docs/components/llmunit/overview) | No         | -          | LLMUnit             |
| - [model](#model )                             | No      | Combination                                             | No         | -          | -                   |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ToolCallLLMWrapper

Specific value: `"ToolCallLLMWrapper"`

## <a name="tool_message_prompt"></a>2. Property `tool_message_prompt`

**Title:** Tool Message Prompt

|              |                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Required** | No                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Default**  | `"You must follow these instructions:\nYou can select zero or more of the above tools based on the user query\nIf there are multiple tools required, make sure a list of tools are returned in a JSON array.\nIf there is no tool that match the user request or you have already answered the question, you will respond with empty json array for the tools.\nYou can also add any additional notes or explanations in the notes field."` |

## <a name="llm_unit"></a>3. Property `llm_unit`

**Title:** LLMUnit

|              |                                                           |
| ------------ | --------------------------------------------------------- |
| **Type**     | [`Reference[LLMUnit]`](/docs/components/llmunit/overview) |
| **Required** | No                                                        |
| **Default**  | `{"implementation": "LLMUnit"}`                           |

**Description:** Overview of LLMUnit components

## <a name="model"></a>4. Property `model`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)              |
| --------------------------- |
| [LLMModel](#model_anyOf_i0) |
| [item 1](#model_anyOf_i1)   |

### <a name="model_anyOf_i0"></a>4.1. Property `LLMModel`

**Title:** LLMModel

|              |                                                             |
| ------------ | ----------------------------------------------------------- |
| **Type**     | [`Reference[LLMModel]`](/docs/components/llmmodel/overview) |
| **Required** | No                                                          |

**Description:** Overview of LLMModel components

### <a name="model_anyOf_i1"></a>4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

----------------------------------------------------------------------------------------------------------------------------
