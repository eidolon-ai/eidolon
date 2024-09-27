---
title: DocumentReranker
description: "Description of DocumentReranker component"
---
# Schema Docs

- [1. Property `implementation`](#implementation)
- [2. Property `k`](#k)

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

| Property                             | Pattern | Type    | Deprecated | Definition | Title/Description |
| ------------------------------------ | ------- | ------- | ---------- | ---------- | ----------------- |
| - [implementation](#implementation ) | No      | const   | No         | -          | -                 |
| - [k](#k )                           | No      | integer | No         | -          | K                 |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

Specific value: `"DocumentReranker"`

## <a name="k"></a>2. Property `k`

**Title:** K

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `60`      |

**Description:** The rerank factor.

----------------------------------------------------------------------------------------------------------------------------
