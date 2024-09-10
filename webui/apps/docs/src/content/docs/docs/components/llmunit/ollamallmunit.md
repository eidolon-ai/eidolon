---
title: OllamaLLMUnit
description: "Description of OllamaLLMUnit component"
---

| Property                             | Pattern | Type                | Deprecated | Definition                        | Title/Description               |
| ------------------------------------ | ------- | ------------------- | ---------- | --------------------------------- | ------------------------------- |
| - [implementation](#implementation ) | No      | const               | No         | -                                 | OllamaLLMUnit                   |
| - [model](#model )                   | No      | Reference[LLMModel] | No         | In [LLMModel](/docs/components/llmmodel/overview) | Overview of LLMModel components |
| - [temperature](#temperature )       | No      | number              | No         | -                                 | Temperature                     |
| - [force_json](#force_json )         | No      | boolean             | No         | -                                 | Force Json                      |
| - [max_tokens](#max_tokens )         | No      | integer             | No         | -                                 | Max Tokens                      |
| - [client_options](#client_options ) | No      | object              | No         | -                                 | Client Options                  |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OllamaLLMUnit

Specific value: `"OllamaLLMUnit"`

## <a name="model"></a>2. Property `model`

|                |                                |
| -------------- | ------------------------------ |
| **Type**       | `Reference[LLMModel]`          |
| **Required**   | No                             |
| **Default**    | `{"implementation": "llama3"}` |
| **Defined in** | [LLMModel](/docs/components/llmmodel/overview) |

**Description:** Overview of LLMModel components

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

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `null`    |

## <a name="client_options"></a>6. Property `client_options`

**Title:** Client Options

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

----------------------------------------------------------------------------------------------------------------------------
