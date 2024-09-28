---
title: OpenAIEmbedding
description: Description of the OpenAIEmbedding component
---

| Property                                     | Pattern | Type                               | Deprecated | Definition | Title/Description |
| -------------------------------------------- | ------- | ---------------------------------- | ---------- | ---------- | ----------------- |
| + [implementation](#implementation )         | No      | const                              | No         | -          | -                 |
| - [model](#model )                           | No      | string                             | No         | -          | Model             |
| - [connection_handler](#connection_handler ) | No      | [Reference[OpenAIConnectionHandler]](/docs/components/openaiconnectionhandler/overview) | No         | -          | -                 |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | Yes     |

Specific value: `"OpenAIEmbedding"`

## <a name="model"></a>2. Property `model`

**Title:** Model

|              |                            |
| ------------ | -------------------------- |
| **Type**     | `string`                   |
| **Required** | No                         |
| **Default**  | `"text-embedding-ada-002"` |

**Description:** The name of the model to use.

## <a name="connection_handler"></a>3. Property `connection_handler`

|              |                                                 |
| ------------ | ----------------------------------------------- |
| **Type**     | [`Reference[OpenAIConnectionHandler]`](/docs/components/openaiconnectionhandler/overview)            |
| **Required** | No                                              |
| **Default**  | `{"implementation": "OpenAIConnectionHandler"}` |

----------------------------------------------------------------------------------------------------------------------------
