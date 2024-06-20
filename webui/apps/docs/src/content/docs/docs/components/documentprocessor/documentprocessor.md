---
title: DocumentProcessor
description: Description of DocumentProcessor component
---

| Property                             | Pattern | Type   | Deprecated | Definition                                   | Title/Description                          |
| ------------------------------------ | ------- | ------ | ---------- | -------------------------------------------- | ------------------------------------------ |
| - [implementation](#implementation ) | No      | const  | No         | -                                            | DocumentProcessor                          |
| - [parser](#parser )                 | No      | object | No         | In [DocumentParser](/docs/components/documentparser/overview)      | Overview of DocumentParser components      |
| - [splitter](#splitter )             | No      | object | No         | In [DocumentTransformer](/docs/components/documenttransformer/overview) | Overview of DocumentTransformer components |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** DocumentProcessor

Specific value: `"DocumentProcessor"`

## <a name="parser"></a>2. Property `parser`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{"implementation": "AutoParser"}`                                        |
| **Defined in**            | [DocumentParser](/docs/components/documentparser/overview)                                      |

**Description:** Overview of DocumentParser components

| Any of(Option)                      |
| ----------------------------------- |
| [AutoParser.json](#parser_anyOf_i0) |

### <a name="parser_anyOf_i0"></a>2.1. Property `AutoParser.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./AutoParser.json                                                    |

| Property                                             | Pattern | Type  | Deprecated | Definition | Title/Description |
| ---------------------------------------------------- | ------- | ----- | ---------- | ---------- | ----------------- |
| - [implementation](#parser_anyOf_i0_implementation ) | No      | const | No         | -          | AutoParser        |

#### <a name="parser_anyOf_i0_implementation"></a>2.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AutoParser

Specific value: `"AutoParser"`

## <a name="splitter"></a>3. Property `splitter`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{"implementation": "AutoTransformer"}`                                   |
| **Defined in**            | [DocumentTransformer](/docs/components/documenttransformer/overview)                                 |

**Description:** Overview of DocumentTransformer components

| Any of(Option)                             |
| ------------------------------------------ |
| [AutoTransformer.json](#splitter_anyOf_i0) |

### <a name="splitter_anyOf_i0"></a>3.1. Property `AutoTransformer.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./AutoTransformer.json                                               |

| Property                                               | Pattern | Type  | Deprecated | Definition | Title/Description |
| ------------------------------------------------------ | ------- | ----- | ---------- | ---------- | ----------------- |
| - [implementation](#splitter_anyOf_i0_implementation ) | No      | const | No         | -          | AutoTransformer   |

#### <a name="splitter_anyOf_i0_implementation"></a>3.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AutoTransformer

Specific value: `"AutoTransformer"`

----------------------------------------------------------------------------------------------------------------------------
