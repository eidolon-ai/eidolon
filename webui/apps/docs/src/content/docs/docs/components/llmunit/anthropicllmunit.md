---
title: AnthropicLLMUnit
description: Description of AnthropicLLMUnit component
---

| Property                             | Pattern | Type                | Deprecated | Definition                        | Title/Description               |
| ------------------------------------ | ------- | ------------------- | ---------- | --------------------------------- | ------------------------------- |
| - [implementation](#implementation ) | No      | const               | No         | -                                 | AnthropicLLMUnit                |
| - [model](#model )                   | No      | Reference[LLMModel] | No         | In [LLMModel](/docs/components/llmmodel/overview) | Overview of LLMModel components |
| - [temperature](#temperature )       | No      | number              | No         | -                                 | Temperature                     |
| - [max_tokens](#max_tokens )         | No      | integer             | No         | -                                 | Max Tokens                      |
| - [client_args](#client_args )       | No      | object              | No         | -                                 | Client Args                     |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AnthropicLLMUnit

Specific value: `"AnthropicLLMUnit"`

## <a name="model"></a>2. Property `model`

|                |                                                |
| -------------- | ---------------------------------------------- |
| **Type**       | `Reference[LLMModel]`                          |
| **Required**   | No                                             |
| **Default**    | `{"implementation": "claude-3-opus-20240229"}` |
| **Defined in** | [LLMModel](/docs/components/llmmodel/overview)                 |

**Description:** Overview of LLMModel components

## <a name="temperature"></a>3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

## <a name="max_tokens"></a>4. Property `max_tokens`

**Title:** Max Tokens

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `null`    |

## <a name="client_args"></a>5. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

----------------------------------------------------------------------------------------------------------------------------
