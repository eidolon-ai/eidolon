---
title: DocumentProcessor
description: Description of DocumentProcessor component
---

| Property                             | Pattern | Type   | Deprecated | Definition | Title/Description   |
| ------------------------------------ | ------- | ------ | ---------- | ---------- | ------------------- |
| - [implementation](#implementation ) | No      | const  | No         | -          | DocumentProcessor   |
| - [parser](#parser )                 | No      | object | No         | -          | DocumentParser      |
| - [splitter](#splitter )             | No      | object | No         | -          | DocumentTransformer |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** DocumentProcessor

Specific value: `"DocumentProcessor"`

## <a name="parser"></a>2. Property `parser`

**Title:** DocumentParser

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{"implementation": "AutoParser"}`                                        |

**Description:** Overview of DocumentParser components

| Property                                    | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#parser_implementation ) | No      | string | No         | -          | -                 |

### <a name="parser_implementation"></a>2.1. Property `implementation`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

## <a name="splitter"></a>3. Property `splitter`

**Title:** DocumentTransformer

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{"implementation": "AutoTransformer"}`                                   |

**Description:** Overview of DocumentTransformer components

| Property                                      | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#splitter_implementation ) | No      | string | No         | -          | -                 |

### <a name="splitter_implementation"></a>3.1. Property `implementation`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

----------------------------------------------------------------------------------------------------------------------------
