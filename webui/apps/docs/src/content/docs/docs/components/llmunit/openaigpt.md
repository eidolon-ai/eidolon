---
title: OpenAIGPT
description: "Description of OpenAIGPT component"
---

| Property                                                 | Pattern | Type                               | Deprecated | Definition                                  | Title/Description                              |
| -------------------------------------------------------- | ------- | ---------------------------------- | ---------- | ------------------------------------------- | ---------------------------------------------- |
| + [implementation](#implementation )                     | No      | const                              | No         | -                                           | OpenAIGPT                                      |
| - [model](#model )                                       | No      | Reference[LLMModel]                | No         | In [LLMModel](/docs/components/llmmodel/overview)                | Overview of LLMModel components                |
| - [temperature](#temperature )                           | No      | number                             | No         | -                                           | Temperature                                    |
| - [force_json](#force_json )                             | No      | boolean                            | No         | -                                           | Force Json                                     |
| - [max_tokens](#max_tokens )                             | No      | integer                            | No         | -                                           | Max Tokens                                     |
| - [supports_system_messages](#supports_system_messages ) | No      | boolean                            | No         | -                                           | Supports System Messages                       |
| - [can_stream](#can_stream )                             | No      | boolean                            | No         | -                                           | Can Stream                                     |
| - [connection_handler](#connection_handler )             | No      | Reference[OpenAIConnectionHandler] | No         | In [OpenAIConnectionHandler](/docs/components/openaiconnectionhandler/overview) | Overview of OpenAIConnectionHandler components |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | Yes     |

**Description:** OpenAIGPT

Specific value: `"OpenAIGPT"`

## <a name="model"></a>2. Property `model`

|                |                                     |
| -------------- | ----------------------------------- |
| **Type**       | `Reference[LLMModel]`               |
| **Required**   | No                                  |
| **Default**    | `{"implementation": "gpt-4-turbo"}` |
| **Defined in** | [LLMModel](/docs/components/llmmodel/overview)           |

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

## <a name="supports_system_messages"></a>6. Property `supports_system_messages`

**Title:** Supports System Messages

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

## <a name="can_stream"></a>7. Property `can_stream`

**Title:** Can Stream

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

## <a name="connection_handler"></a>8. Property `connection_handler`

|                |                                                 |
| -------------- | ----------------------------------------------- |
| **Type**       | `Reference[OpenAIConnectionHandler]`            |
| **Required**   | No                                              |
| **Default**    | `{"implementation": "OpenAIConnectionHandler"}` |
| **Defined in** | [OpenAIConnectionHandler](/docs/components/openaiconnectionhandler/overview)        |

**Description:** Overview of OpenAIConnectionHandler components

----------------------------------------------------------------------------------------------------------------------------
