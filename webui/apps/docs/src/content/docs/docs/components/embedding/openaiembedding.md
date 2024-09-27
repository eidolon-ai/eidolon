---
title: OpenAIEmbedding
description: "Description of OpenAIEmbedding component"
---
# Schema Docs

- [1. Property `implementation`](#implementation)
- [2. Property `model`](#model)
- [3. Property `connection_handler`](#connection_handler)
  - [3.1. Property `implementation`](#connection_handler_implementation)

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

| Property                                     | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#implementation )         | No      | const  | No         | -          | -                 |
| - [model](#model )                           | No      | string | No         | -          | Model             |
| - [connection_handler](#connection_handler ) | No      | object | No         | -          | -                 |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

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

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

| Property                                                | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#connection_handler_implementation ) | No      | string | No         | -          | -                 |
| - [](#connection_handler_additionalProperties )         | No      | object | No         | -          | -                 |

### <a name="connection_handler_implementation"></a>3.1. Property `implementation`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

----------------------------------------------------------------------------------------------------------------------------
