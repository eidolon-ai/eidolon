---
title: SimilarityMemoryImpl
description: Description of the SimilarityMemoryImpl component
---

| Property                             | Pattern | Type                   | Deprecated | Definition | Title/Description |
| ------------------------------------ | ------- | ---------------------- | ---------- | ---------- | ----------------- |
| + [implementation](#implementation ) | No      | const                  | No         | -          | Implementation    |
| - [embedder](#embedder )             | No      | [Reference[Embedding]](/docs/components/embedding/overview)   | No         | -          | -                 |
| - [vector_store](#vector_store )     | No      | [Reference[VectorStore]](/docs/components/vectorstore/overview) | No         | -          | -                 |

## <a name="implementation"></a>1. Property `implementation`

**Title:** Implementation

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | Yes     |

Specific value: `"SimilarityMemoryImpl"`

## <a name="embedder"></a>2. Property `embedder`

|              |                                   |
| ------------ | --------------------------------- |
| **Type**     | [`Reference[Embedding]`](/docs/components/embedding/overview)            |
| **Required** | No                                |
| **Default**  | `{"implementation": "Embedding"}` |

## <a name="vector_store"></a>3. Property `vector_store`

|              |                                     |
| ------------ | ----------------------------------- |
| **Type**     | [`Reference[VectorStore]`](/docs/components/vectorstore/overview)            |
| **Required** | No                                  |
| **Default**  | `{"implementation": "VectorStore"}` |

----------------------------------------------------------------------------------------------------------------------------
