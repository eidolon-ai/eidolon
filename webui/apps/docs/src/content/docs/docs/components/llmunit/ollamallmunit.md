---
title: OllamaLLMUnit
description: Description of OllamaLLMUnit component
---

| Property                             | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------ | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#implementation ) | No      | const       | No         | -          | OllamaLLMUnit      |
| - [model](#model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#temperature )       | No      | number      | No         | -          | Temperature        |
| - [force_json](#force_json )         | No      | boolean     | No         | -          | Force Json         |
| - [max_tokens](#max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_options](#client_options ) | No      | object      | No         | -          | Client Options     |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OllamaLLMUnit

Specific value: `"OllamaLLMUnit"`

## <a name="model"></a>2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"llama3"`                                                                |

| Property                                   | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------ | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#model_additionalProperties )         | No      | object | No         | -          | -                 |

### <a name="model_implementation"></a>2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

## <a name="temperature"></a>3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

## <a name="force_json"></a>4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

## <a name="max_tokens"></a>5. Property `max_tokens`

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

### <a name="max_tokens_anyOf_i0"></a>5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

### <a name="max_tokens_anyOf_i1"></a>5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

## <a name="client_options"></a>6. Property `client_options`

**Title:** Client Options

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

----------------------------------------------------------------------------------------------------------------------------
