---
title: SimilarityMemoryImpl
description: "Description of SimilarityMemoryImpl component"
---
# SimilarityMemoryImpl

- [1. [Optional] Property implementation](#implementation)
- [2. [Optional] Property embedder](#embedder)
- [3. [Optional] Property vector_store](#vector_store)

**Title:** SimilarityMemoryImpl

|                           |                                                         |
| ------------------------- | ------------------------------------------------------- |
| **Type**                  | `object`                                                |
| **Required**              | No                                                      |
| **Additional properties** | [[Not allowed]](# "Additional Properties not allowed.") |

<details>
<summary>
<strong> <a name="implementation"></a>1. [Optional] Property implementation</strong>  

</summary>
<blockquote>

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

Specific value: `"SimilarityMemoryImpl"`

</blockquote>
</details>

<details>
<summary>
<strong> <a name="embedder"></a>2. [Optional] Property embedder</strong>  

</summary>
<blockquote>

|              |                                   |
| ------------ | --------------------------------- |
| **Type**     | [`Reference[Embedding]`](/docs/components/embedding/overview)            |
| **Required** | No                                |
| **Default**  | `{"implementation": "Embedding"}` |

</blockquote>
</details>

<details>
<summary>
<strong> <a name="vector_store"></a>3. [Optional] Property vector_store</strong>  

</summary>
<blockquote>

|              |                                     |
| ------------ | ----------------------------------- |
| **Type**     | [`Reference[VectorStore]`](/docs/components/vectorstore/overview)            |
| **Required** | No                                  |
| **Default**  | `{"implementation": "VectorStore"}` |

</blockquote>
</details>

----------------------------------------------------------------------------------------------------------------------------
