---
title: DocumentProcessor
description: "Description of DocumentProcessor component"
---

| Property                             | Pattern | Type                           | Deprecated | Definition                                   | Title/Description                          |
| ------------------------------------ | ------- | ------------------------------ | ---------- | -------------------------------------------- | ------------------------------------------ |
| - [implementation](#implementation ) | No      | const                          | No         | -                                            | DocumentProcessor                          |
| - [parser](#parser )                 | No      | Reference[DocumentParser]      | No         | In [DocumentParser](/docs/components/documentparser/overview)      | Overview of DocumentParser components      |
| - [splitter](#splitter )             | No      | Reference[DocumentTransformer] | No         | In [DocumentTransformer](/docs/components/documenttransformer/overview) | Overview of DocumentTransformer components |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** DocumentProcessor

Specific value: `"DocumentProcessor"`

## <a name="parser"></a>2. Property `parser`

|                |                                        |
| -------------- | -------------------------------------- |
| **Type**       | `Reference[DocumentParser]`            |
| **Required**   | No                                     |
| **Default**    | `{"implementation": "DocumentParser"}` |
| **Defined in** | [DocumentParser](/docs/components/documentparser/overview)   |

**Description:** Overview of DocumentParser components

## <a name="splitter"></a>3. Property `splitter`

|                |                                             |
| -------------- | ------------------------------------------- |
| **Type**       | `Reference[DocumentTransformer]`            |
| **Required**   | No                                          |
| **Default**    | `{"implementation": "DocumentTransformer"}` |
| **Defined in** | [DocumentTransformer](/docs/components/documenttransformer/overview)   |

**Description:** Overview of DocumentTransformer components

----------------------------------------------------------------------------------------------------------------------------
