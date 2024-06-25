---
title: SimilarityMemoryImpl
description: Description of SimilarityMemoryImpl component
---

| Property                             | Pattern | Type                                                            | Deprecated | Definition | Title/Description    |
| ------------------------------------ | ------- | --------------------------------------------------------------- | ---------- | ---------- | -------------------- |
| - [implementation](#implementation ) | No      | const                                                           | No         | -          | SimilarityMemoryImpl |
| - [embedder](#embedder )             | No      | [Reference[Embedding]](/docs/components/embedding/overview)     | No         | -          | Embedding            |
| - [vector_store](#vector_store )     | No      | [Reference[VectorStore]](/docs/components/vectorstore/overview) | No         | -          | VectorStore          |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** SimilarityMemoryImpl

Specific value: `"SimilarityMemoryImpl"`

## <a name="embedder"></a>2. Property `embedder`

**Title:** Embedding

|              |                                                               |
| ------------ | ------------------------------------------------------------- |
| **Type**     | [`Reference[Embedding]`](/docs/components/embedding/overview) |
| **Required** | No                                                            |
| **Default**  | `{"implementation": "Embedding"}`                             |

**Description:** Overview of Embedding components

## <a name="vector_store"></a>3. Property `vector_store`

**Title:** VectorStore

|              |                                                                   |
| ------------ | ----------------------------------------------------------------- |
| **Type**     | [`Reference[VectorStore]`](/docs/components/vectorstore/overview) |
| **Required** | No                                                                |
| **Default**  | `{"implementation": "VectorStore"}`                               |

**Description:** Overview of VectorStore components

----------------------------------------------------------------------------------------------------------------------------
