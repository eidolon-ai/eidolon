---
title: ToolCallLLMWrapper
description: "Description of ToolCallLLMWrapper component"
---

| Property                                       | Pattern | Type                | Deprecated | Definition                   | Title/Description               |
| ---------------------------------------------- | ------- | ------------------- | ---------- | ---------------------------- | ------------------------------- |
| + [implementation](#implementation )           | No      | const               | No         | -                            | ToolCallLLMWrapper              |
| - [tool_message_prompt](#tool_message_prompt ) | No      | string              | No         | -                            | Tool Message Prompt             |
| - [llm_unit](#llm_unit )                       | No      | Reference[LLMUnit]  | No         | In [LLMUnit](/docs/components/llmunit/overview)  | Overview of LLMUnit components  |
| - [model](#model )                             | No      | Reference[LLMModel] | No         | In [LLMModel](/docs/components/llmmodel/overview) | Overview of LLMModel components |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | Yes     |

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

|                |                                 |
| -------------- | ------------------------------- |
| **Type**       | `Reference[LLMUnit]`            |
| **Required**   | No                              |
| **Default**    | `{"implementation": "LLMUnit"}` |
| **Defined in** | [LLMUnit](/docs/components/llmunit/overview)        |

**Description:** Overview of LLMUnit components

## <a name="model"></a>4. Property `model`

|                |                           |
| -------------- | ------------------------- |
| **Type**       | `Reference[LLMModel]`     |
| **Required**   | No                        |
| **Default**    | `null`                    |
| **Defined in** | [LLMModel](/docs/components/llmmodel/overview) |

**Description:** Overview of LLMModel components

----------------------------------------------------------------------------------------------------------------------------
