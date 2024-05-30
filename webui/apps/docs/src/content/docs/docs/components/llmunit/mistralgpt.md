---
title: MistralGPT
description: Description of MistralGPT component
---

| Property                       | Pattern | Type                | Deprecated | Definition | Title/Description  |
| ------------------------------ | ------- | ------------------- | ---------- | ---------- | ------------------ |
| - [model](#model )             | No      | [Reference[LLMModel]](/docs/components/llmmodel/overview/) | No         | -          | LLMModel Reference |
| - [temperature](#temperature ) | No      | number              | No         | -          | Temperature        |
| - [force_json](#force_json )   | No      | boolean             | No         | -          | Force Json         |
| - [max_tokens](#max_tokens )   | No      | Combination         | No         | -          | Max Tokens         |
| - [client_args](#client_args ) | No      | object              | No         | -          | Client Args        |

## <a name="model"></a>1. Property `model`

**Title:** LLMModel Reference

|              |                          |
| ------------ | ------------------------ |
| **Type**     | `[Reference[LLMModel]](/docs/components/llmmodel/overview/)`    |
| **Required** | No                       |
| **Default**  | `"mistral-large-latest"` |

## <a name="temperature"></a>2. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

## <a name="force_json"></a>3. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

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
