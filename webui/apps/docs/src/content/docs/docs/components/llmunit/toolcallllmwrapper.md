---
title: ToolCallLLMWrapper
description: "Description of ToolCallLLMWrapper component"
---

| Property                                       | Pattern | Type   | Deprecated | Definition | Title/Description   |
| ---------------------------------------------- | ------- | ------ | ---------- | ---------- | ------------------- |
| - [implementation](#implementation )           | No      | const  | No         | -          | -                   |
| - [tool_message_prompt](#tool_message_prompt ) | No      | string | No         | -          | Tool Message Prompt |
| - [llm_unit](#llm_unit )                       | No      | object | No         | -          | -                   |
| - [model](#model )                             | No      | object | No         | -          | -                   |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

Specific value: `"ToolCallLLMWrapper"`

## <a name="tool_message_prompt"></a>2. Property `tool_message_prompt`

**Title:** Tool Message Prompt

|              |                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Required** | No                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Default**  | `"You must follow these instructions:\nYou can select zero or more of the above tools based on the user query\nIf there are multiple tools required, make sure a list of tools are returned in a JSON array.\nIf there is no tool that match the user request or you have already answered the question, you will respond with empty json array for the tools.\nYou can also add any additional notes or explanations in the notes field."` |

## <a name="llm_unit"></a>3. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

| Property                                      | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#llm_unit_implementation ) | No      | string | No         | -          | -                 |
| - [](#llm_unit_additionalProperties )         | No      | object | No         | -          | -                 |

### <a name="llm_unit_implementation"></a>3.1. Property `implementation`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

## <a name="model"></a>4. Property `model`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Property                                   | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------ | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#model_implementation ) | No      | string | No         | -          | -                 |
| - [](#model_additionalProperties )         | No      | object | No         | -          | -                 |

### <a name="model_implementation"></a>4.1. Property `implementation`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

----------------------------------------------------------------------------------------------------------------------------
