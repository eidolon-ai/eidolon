---
title: ToolCallLLMWrapper
description: "Description of ToolCallLLMWrapper component"
---
# ToolCallLLMWrapper

- [1. [Optional] Property implementation](#implementation)
- [2. [Optional] Property tool_message_prompt](#tool_message_prompt)
- [3. [Optional] Property llm_unit](#llm_unit)
- [4. [Optional] Property model](#model)

**Title:** ToolCallLLMWrapper

|                           |                                                         |
| ------------------------- | ------------------------------------------------------- |
| **Type**                  | `object`                                                |
| **Required**              | No                                                      |
| **Additional properties** | [[Not allowed]](# "Additional Properties not allowed.") |

<details>
<summary>
<strong> <a name="implementation"></a>1. [Optional] Property implementation</strong>  

</summary>
<blockquote>

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

Specific value: `"ToolCallLLMWrapper"`

</blockquote>
</details>

<details>
<summary>
<strong> <a name="tool_message_prompt"></a>2. [Optional] Property tool_message_prompt</strong>  

</summary>
<blockquote>

**Title:** Tool Message Prompt

|              |                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Required** | No                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Default**  | `"You must follow these instructions:\nYou can select zero or more of the above tools based on the user query\nIf there are multiple tools required, make sure a list of tools are returned in a JSON array.\nIf there is no tool that match the user request or you have already answered the question, you will respond with empty json array for the tools.\nYou can also add any additional notes or explanations in the notes field."` |

</blockquote>
</details>

<details>
<summary>
<strong> <a name="llm_unit"></a>3. [Optional] Property llm_unit</strong>  

</summary>
<blockquote>

|              |                                                             |
| ------------ | ----------------------------------------------------------- |
| **Type**     | [`Reference[LLMUnit]`](/docs/components/llmunit/overview)                                        |
| **Required** | No                                                          |
| **Default**  | `{"implementation": "eidolon_ai_sdk.apu.llm_unit.LLMUnit"}` |

</blockquote>
</details>

<details>
<summary>
<strong> <a name="model"></a>4. [Optional] Property model</strong>  

</summary>
<blockquote>

|              |                       |
| ------------ | --------------------- |
| **Type**     | [`Reference[LLMModel]`](/docs/components/llmmodel/overview) |
| **Required** | No                    |
| **Default**  | `null`                |

</blockquote>
</details>

----------------------------------------------------------------------------------------------------------------------------
