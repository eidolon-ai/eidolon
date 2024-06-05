---
title: SimilarityMemoryImpl
description: Description of SimilarityMemoryImpl component
---

| Property                             | Pattern | Type   | Deprecated | Definition | Title/Description     |
| ------------------------------------ | ------- | ------ | ---------- | ---------- | --------------------- |
| - [implementation](#implementation ) | No      | const  | No         | -          | SimilarityMemoryImpl  |
| - [embedder](#embedder )             | No      | object | No         | -          | Embedding Reference   |
| - [vector_store](#vector_store )     | No      | object | No         | -          | VectorStore Reference |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** SimilarityMemoryImpl

Specific value: `"SimilarityMemoryImpl"`

## <a name="embedder"></a>2. Property `embedder`

**Title:** Embedding Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"Embedding"`                                                             |

| Property                                      | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#embedder_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#embedder_additionalProperties )         | No      | object | No         | -          | -                 |

### <a name="embedder_implementation"></a>2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

## <a name="vector_store"></a>3. Property `vector_store`

**Title:** VectorStore Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"VectorStore"`                                                           |

| Property                                          | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#vector_store_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#vector_store_additionalProperties )         | No      | object | No         | -          | -                 |

### <a name="vector_store_implementation"></a>3.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

----------------------------------------------------------------------------------------------------------------------------
