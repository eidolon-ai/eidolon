---
title: ToolCallLLMWrapper
description: Description of the ToolCallLLMWrapper component
---

| Property                                       | Pattern | Type                | Deprecated | Definition | Title/Description   |
| ---------------------------------------------- | ------- | ------------------- | ---------- | ---------- | ------------------- |
| + [implementation](#implementation )           | No      | const               | No         | -          | Implementation      |
| - [tool_message_prompt](#tool_message_prompt ) | No      | string              | No         | -          | Tool Message Prompt |
| - [llm_unit](#llm_unit )                       | No      | [Reference[LLMUnit]](/docs/components/llmunit/overview)  | No         | -          | -                   |
| - [model](#model )                             | No      | [Reference[LLMModel]](/docs/components/llmmodel/overview) | No         | -          | -                   |

## <a name="implementation"></a>1. Property `implementation`

**Title:** Implementation

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | Yes     |

Specific value: `"ToolCallLLMWrapper"`

## <a name="tool_message_prompt"></a>2. Property `tool_message_prompt`

**Title:** Tool Message Prompt

|              |                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Required** | No                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Default**  | `"You must follow these instructions:\nYou can select zero or more of the above tools based on the user query\nIf there are multiple tools required, make sure a list of tools are returned in a JSON array.\nIf there is no tool that match the user request or you have already answered the question, you will respond with empty json array for the tools.\nYou can also add any additional notes or explanations in the notes field."` |

## <a name="llm_unit"></a>3. Property `llm_unit`

|              |                                 |
| ------------ | ------------------------------- |
| **Type**     | [`Reference[LLMUnit]`](/docs/components/llmunit/overview)            |
| **Required** | No                              |
| **Default**  | `{"implementation": "LLMUnit"}` |

## <a name="model"></a>4. Property `model`

|              |                       |
| ------------ | --------------------- |
| **Type**     | [`Reference[LLMModel]`](/docs/components/llmmodel/overview) |
| **Required** | No                    |
| **Default**  | `null`                |

----------------------------------------------------------------------------------------------------------------------------
