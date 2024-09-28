---
title: SentenceTransformersTokenTextSplitter
description: "Description of SentenceTransformersTokenTextSplitter component"
---
# SentenceTransformersTokenTextSplitter

- [1. [Optional] Property implementation](#implementation)
- [2. [Optional] Property chunk_size](#chunk_size)
- [3. [Optional] Property chunk_overlap](#chunk_overlap)
- [4. [Optional] Property keep_separator](#keep_separator)
- [5. [Optional] Property strip_whitespace](#strip_whitespace)
- [6. [Optional] Property model](#model)
- [7. [Optional] Property tokens_per_chunk](#tokens_per_chunk)

**Title:** SentenceTransformersTokenTextSplitter

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

Specific value: `"SentenceTransformersTokenTextSplitter"`

</blockquote>
</details>

<details>
<summary>
<strong> <a name="chunk_size"></a>2. [Optional] Property chunk_size</strong>  

</summary>
<blockquote>

**Title:** Chunk Size

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `4000`    |

**Description:** Maximum size of chunks to return

</blockquote>
</details>

<details>
<summary>
<strong> <a name="chunk_overlap"></a>3. [Optional] Property chunk_overlap</strong>  

</summary>
<blockquote>

**Title:** Chunk Overlap

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `50`      |

</blockquote>
</details>

<details>
<summary>
<strong> <a name="keep_separator"></a>4. [Optional] Property keep_separator</strong>  

</summary>
<blockquote>

**Title:** Keep Separator

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `false`   |

**Description:** Whether to keep the separator in the chunks

</blockquote>
</details>

<details>
<summary>
<strong> <a name="strip_whitespace"></a>5. [Optional] Property strip_whitespace</strong>  

</summary>
<blockquote>

**Title:** Strip Whitespace

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

**Description:** If `True`, strips whitespace from the start and end of every document

</blockquote>
</details>

<details>
<summary>
<strong> <a name="model"></a>6. [Optional] Property model</strong>  

</summary>
<blockquote>

**Title:** Model

|              |                                             |
| ------------ | ------------------------------------------- |
| **Type**     | `string`                                    |
| **Required** | No                                          |
| **Default**  | `"sentence-transformers/all-mpnet-base-v2"` |

**Description:** Model name

</blockquote>
</details>

<details>
<summary>
<strong> <a name="tokens_per_chunk"></a>7. [Optional] Property tokens_per_chunk</strong>  

</summary>
<blockquote>

**Title:** Tokens Per Chunk

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `null`    |

**Description:** Number of tokens per chunk

</blockquote>
</details>

----------------------------------------------------------------------------------------------------------------------------
