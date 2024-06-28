---
title: AnthropicLLMUnit
description: Description of AnthropicLLMUnit component
---

| Property                             | Pattern | Type                                                      | Deprecated | Definition | Title/Description |
| ------------------------------------ | ------- | --------------------------------------------------------- | ---------- | ---------- | ----------------- |
| - [implementation](#implementation ) | No      | const                                                     | No         | -          | AnthropicLLMUnit  |
| - [model](#model )                   | No      | [Reference[LLMModel]](/docs/components/llmmodel/overview) | No         | -          | LLMModel          |
| - [temperature](#temperature )       | No      | number                                                    | No         | -          | Temperature       |
| - [max_tokens](#max_tokens )         | No      | Combination                                               | No         | -          | Max Tokens        |
| - [client_args](#client_args )       | No      | object                                                    | No         | -          | Client Args       |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AnthropicLLMUnit

Specific value: `"AnthropicLLMUnit"`

## <a name="model"></a>2. Property `model`

**Title:** LLMModel

|              |                                                             |
| ------------ | ----------------------------------------------------------- |
| **Type**     | [`Reference[LLMModel]`](/docs/components/llmmodel/overview) |
| **Required** | No                                                          |
| **Default**  | `{"implementation": "claude-3-opus-20240229"}`              |

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

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                 |
| ------------------------------ |
| [item 0](#max_tokens_anyOf_i0) |
| [item 1](#max_tokens_anyOf_i1) |

### <a name="max_tokens_anyOf_i0"></a>4.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

### <a name="max_tokens_anyOf_i1"></a>4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

## <a name="client_args"></a>5. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

----------------------------------------------------------------------------------------------------------------------------
