---
title: Embedding
description: Description of Embedding component
---

| Property                                     | Pattern | Type                               | Deprecated | Definition                                       | Title/Description                              |
| -------------------------------------------- | ------- | ---------------------------------- | ---------- | ------------------------------------------------ | ---------------------------------------------- |
| - [implementation](#implementation )         | No      | const                              | No         | -                                                | Embedding                                      |
| - [model](#model )                           | No      | string                             | No         | -                                                | Model                                          |
| - [connection_handler](#connection_handler ) | No      | Reference[OpenAIConnectionHandler] | No         | In [OpenAIConnectionHandler](/docs/components/openaiconnectionhandler/overview) | Overview of OpenAIConnectionHandler components |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** Embedding

Specific value: `"Embedding"`

## <a name="model"></a>2. Property `model`

**Title:** Model

|              |                            |
| ------------ | -------------------------- |
| **Type**     | `string`                   |
| **Required** | No                         |
| **Default**  | `"text-embedding-ada-002"` |

**Description:** The name of the model to use.

## <a name="connection_handler"></a>3. Property `connection_handler`

|                |                                                 |
| -------------- | ----------------------------------------------- |
| **Type**       | `Reference[OpenAIConnectionHandler]`            |
| **Required**   | No                                              |
| **Default**    | `{"implementation": "OpenAIConnectionHandler"}` |
| **Defined in** | [OpenAIConnectionHandler](/docs/components/openaiconnectionhandler/overview)   |

**Description:** Overview of OpenAIConnectionHandler components

----------------------------------------------------------------------------------------------------------------------------
