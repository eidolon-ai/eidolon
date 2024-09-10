---
title: SimilarityMemoryImpl
description: "Description of SimilarityMemoryImpl component"
---

| Property                             | Pattern | Type                   | Deprecated | Definition                           | Title/Description                  |
| ------------------------------------ | ------- | ---------------------- | ---------- | ------------------------------------ | ---------------------------------- |
| - [implementation](#implementation ) | No      | const                  | No         | -                                    | SimilarityMemoryImpl               |
| - [embedder](#embedder )             | No      | Reference[Embedding]   | No         | In [Embedding](/docs/components/embedding/overview)   | Overview of Embedding components   |
| - [vector_store](#vector_store )     | No      | Reference[VectorStore] | No         | In [VectorStore](/docs/components/vectorstore/overview) | Overview of VectorStore components |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** SimilarityMemoryImpl

Specific value: `"SimilarityMemoryImpl"`

## <a name="embedder"></a>2. Property `embedder`

|                |                                   |
| -------------- | --------------------------------- |
| **Type**       | `Reference[Embedding]`            |
| **Required**   | No                                |
| **Default**    | `{"implementation": "Embedding"}` |
| **Defined in** | [Embedding](/docs/components/embedding/overview)   |

**Description:** Overview of Embedding components

## <a name="vector_store"></a>3. Property `vector_store`

|                |                                     |
| -------------- | ----------------------------------- |
| **Type**       | `Reference[VectorStore]`            |
| **Required**   | No                                  |
| **Default**    | `{"implementation": "VectorStore"}` |
| **Defined in** | [VectorStore](/docs/components/vectorstore/overview)   |

**Description:** Overview of VectorStore components

----------------------------------------------------------------------------------------------------------------------------
