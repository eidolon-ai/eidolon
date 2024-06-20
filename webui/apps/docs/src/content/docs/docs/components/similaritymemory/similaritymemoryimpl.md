---
title: SimilarityMemoryImpl
description: Description of SimilarityMemoryImpl component
---

| Property                             | Pattern | Type   | Deprecated | Definition | Title/Description    |
| ------------------------------------ | ------- | ------ | ---------- | ---------- | -------------------- |
| - [implementation](#implementation ) | No      | const  | No         | -          | SimilarityMemoryImpl |
| - [embedder](#embedder )             | No      | object | No         | -          | Embedding            |
| - [vector_store](#vector_store )     | No      | object | No         | -          | VectorStore          |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** SimilarityMemoryImpl

Specific value: `"SimilarityMemoryImpl"`

## <a name="embedder"></a>2. Property `embedder`

**Title:** Embedding

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{"implementation": "OpenAIEmbedding"}`                                   |

**Description:** Overview of Embedding components

| Property                                      | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#embedder_implementation ) | No      | string | No         | -          | -                 |

### <a name="embedder_implementation"></a>2.1. Property `implementation`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

## <a name="vector_store"></a>3. Property `vector_store`

**Title:** VectorStore

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{"implementation": "ChromaVectorStore"}`                                 |

**Description:** Overview of VectorStore components

| Property                                          | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#vector_store_implementation ) | No      | string | No         | -          | -                 |

### <a name="vector_store_implementation"></a>3.1. Property `implementation`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

----------------------------------------------------------------------------------------------------------------------------
