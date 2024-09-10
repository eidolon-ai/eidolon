---
title: OpenAIGPT
description: "Description of OpenAIGPT component"
---

| Property                                     | Pattern | Type                               | Deprecated | Definition                                       | Title/Description                              |
| -------------------------------------------- | ------- | ---------------------------------- | ---------- | ------------------------------------------------ | ---------------------------------------------- |
| - [implementation](#implementation )         | No      | const                              | No         | -                                                | OpenAIGPT                                      |
| - [model](#model )                           | No      | Reference[LLMModel]                | No         | In [LLMModel](/docs/components/llmmodel/overview)                | Overview of LLMModel components                |
| - [temperature](#temperature )               | No      | number                             | No         | -                                                | Temperature                                    |
| - [force_json](#force_json )                 | No      | boolean                            | No         | -                                                | Force Json                                     |
| - [max_tokens](#max_tokens )                 | No      | integer                            | No         | -                                                | Max Tokens                                     |
| - [connection_handler](#connection_handler ) | No      | Reference[OpenAIConnectionHandler] | No         | In [OpenAIConnectionHandler](/docs/components/openaiconnectionhandler/overview) | Overview of OpenAIConnectionHandler components |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OpenAIGPT

Specific value: `"OpenAIGPT"`

## <a name="model"></a>2. Property `model`

|                |                                     |
| -------------- | ----------------------------------- |
| **Type**       | `Reference[LLMModel]`               |
| **Required**   | No                                  |
| **Default**    | `{"implementation": "gpt-4-turbo"}` |
| **Defined in** | [LLMModel](/docs/components/llmmodel/overview)      |

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

## <a name="connection_handler"></a>6. Property `connection_handler`

|                |                                                 |
| -------------- | ----------------------------------------------- |
| **Type**       | `Reference[OpenAIConnectionHandler]`            |
| **Required**   | No                                              |
| **Default**    | `{"implementation": "OpenAIConnectionHandler"}` |
| **Defined in** | [OpenAIConnectionHandler](/docs/components/openaiconnectionhandler/overview)   |

**Description:** Overview of OpenAIConnectionHandler components

----------------------------------------------------------------------------------------------------------------------------
