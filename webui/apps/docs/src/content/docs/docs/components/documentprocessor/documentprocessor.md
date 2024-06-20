---
title: DocumentProcessor
description: Description of DocumentProcessor component
---

| Property                             | Pattern | Type                                                                            | Deprecated | Definition | Title/Description   |
| ------------------------------------ | ------- | ------------------------------------------------------------------------------- | ---------- | ---------- | ------------------- |
| - [implementation](#implementation ) | No      | const                                                                           | No         | -          | DocumentProcessor   |
| - [parser](#parser )                 | No      | [Reference[DocumentParser]](/docs/components/documentparser/overview)           | No         | -          | DocumentParser      |
| - [splitter](#splitter )             | No      | [Reference[DocumentTransformer]](/docs/components/documenttransformer/overview) | No         | -          | DocumentTransformer |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** DocumentProcessor

Specific value: `"DocumentProcessor"`

## <a name="parser"></a>2. Property `parser`

**Title:** DocumentParser

|              |                                                                         |
| ------------ | ----------------------------------------------------------------------- |
| **Type**     | `[Reference[DocumentParser]](/docs/components/documentparser/overview)` |
| **Required** | No                                                                      |
| **Default**  | `{"implementation": "AutoParser"}`                                      |

**Description:** Overview of DocumentParser components

## <a name="splitter"></a>3. Property `splitter`

**Title:** DocumentTransformer

|              |                                                                                   |
| ------------ | --------------------------------------------------------------------------------- |
| **Type**     | `[Reference[DocumentTransformer]](/docs/components/documenttransformer/overview)` |
| **Required** | No                                                                                |
| **Default**  | `{"implementation": "AutoTransformer"}`                                           |

**Description:** Overview of DocumentTransformer components

----------------------------------------------------------------------------------------------------------------------------
