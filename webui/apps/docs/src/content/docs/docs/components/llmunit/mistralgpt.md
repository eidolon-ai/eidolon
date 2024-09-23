---
title: MistralGPT
description: "Description of MistralGPT component"
---

| Property                             | Pattern | Type                | Deprecated | Definition                        | Title/Description               |
| ------------------------------------ | ------- | ------------------- | ---------- | --------------------------------- | ------------------------------- |
| - [implementation](#implementation ) | No      | const               | No         | -                                 | MistralGPT                      |
| - [model](#model )                   | No      | Reference[LLMModel] | No         | In [LLMModel](/docs/components/llmmodel/overview) | Overview of LLMModel components |
| - [temperature](#temperature )       | No      | number              | No         | -                                 | Temperature                     |
| - [force_json](#force_json )         | No      | boolean             | No         | -                                 | Force Json                      |
| - [max_tokens](#max_tokens )         | No      | integer             | No         | -                                 | Max Tokens                      |
| - [client_args](#client_args )       | No      | object              | No         | -                                 | Client Args                     |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** MistralGPT

Specific value: `"MistralGPT"`

## <a name="model"></a>2. Property `model`

|                |                                              |
| -------------- | -------------------------------------------- |
| **Type**       | `Reference[LLMModel]`                        |
| **Required**   | No                                           |
| **Default**    | `{"implementation": "mistral-large-latest"}` |
| **Defined in** | [LLMModel](/docs/components/llmmodel/overview)               |

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

## <a name="client_args"></a>6. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

----------------------------------------------------------------------------------------------------------------------------
