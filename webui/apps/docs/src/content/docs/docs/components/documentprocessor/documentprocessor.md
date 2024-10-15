---
title: DocumentProcessor
description: Description of the DocumentProcessor component
---

| Property                             | Pattern | Type                           | Deprecated | Definition | Title/Description |
| ------------------------------------ | ------- | ------------------------------ | ---------- | ---------- | ----------------- |
| + [implementation](#implementation ) | No      | const                          | No         | -          | Implementation    |
| - [parser](#parser )                 | No      | [Reference[DocumentParser]](/docs/components/documentparser/overview)      | No         | -          | -                 |
| - [splitter](#splitter )             | No      | [Reference[DocumentTransformer]](/docs/components/documenttransformer/overview) | No         | -          | -                 |

## <a name="implementation"></a>1. Property `implementation`

**Title:** Implementation

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | Yes     |

Specific value: `"DocumentProcessor"`

## <a name="parser"></a>2. Property `parser`

|              |                                        |
| ------------ | -------------------------------------- |
| **Type**     | [`Reference[DocumentParser]`](/docs/components/documentparser/overview)            |
| **Required** | No                                     |
| **Default**  | `{"implementation": "DocumentParser"}` |

## <a name="splitter"></a>3. Property `splitter`

|              |                                             |
| ------------ | ------------------------------------------- |
| **Type**     | [`Reference[DocumentTransformer]`](/docs/components/documenttransformer/overview)            |
| **Required** | No                                          |
| **Default**  | `{"implementation": "DocumentTransformer"}` |

----------------------------------------------------------------------------------------------------------------------------
