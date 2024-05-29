---
title: AnthropicLLMUnit
description: Description of AnthropicLLMUnit component
---
# AnthropicLLMUnit

- [1. Property `AnthropicLLMUnit > model`](#model)
- [2. Property `AnthropicLLMUnit > temperature`](#temperature)
- [3. Property `AnthropicLLMUnit > max_tokens`](#max_tokens)
  - [3.1. Property `AnthropicLLMUnit > max_tokens > anyOf > item 0`](#max_tokens_anyOf_i0)
  - [3.2. Property `AnthropicLLMUnit > max_tokens > anyOf > item 1`](#max_tokens_anyOf_i1)
- [4. Property `AnthropicLLMUnit > client_args`](#client_args)

**Title:** AnthropicLLMUnit

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

| Property                       | Pattern | Type                | Deprecated | Definition | Title/Description  |
| ------------------------------ | ------- | ------------------- | ---------- | ---------- | ------------------ |
| - [model](#model )             | No      | [Reference[LLMModel]](/docs/components/llmmodel/overview/) | No         | -          | LLMModel Reference |
| - [temperature](#temperature ) | No      | number              | No         | -          | Temperature        |
| - [max_tokens](#max_tokens )   | No      | Combination         | No         | -          | Max Tokens         |
| - [client_args](#client_args ) | No      | object              | No         | -          | Client Args        |

## <a name="model"></a>1. Property `AnthropicLLMUnit > model`

**Title:** LLMModel Reference

|              |                            |
| ------------ | -------------------------- |
| **Type**     | `[Reference[LLMModel]](/docs/components/llmmodel/overview/)`      |
| **Required** | No                         |
| **Default**  | `"claude-3-opus-20240229"` |

## <a name="temperature"></a>2. Property `AnthropicLLMUnit > temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

## <a name="max_tokens"></a>3. Property `AnthropicLLMUnit > max_tokens`

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

### <a name="max_tokens_anyOf_i0"></a>3.1. Property `AnthropicLLMUnit > max_tokens > anyOf > item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

### <a name="max_tokens_anyOf_i1"></a>3.2. Property `AnthropicLLMUnit > max_tokens > anyOf > item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

## <a name="client_args"></a>4. Property `AnthropicLLMUnit > client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

----------------------------------------------------------------------------------------------------------------------------
