---
title: SentenceTransformersTokenTextSplitter
description: Description of the SentenceTransformersTokenTextSplitter component
---

| Property                                 | Pattern | Type    | Deprecated | Definition | Title/Description |
| ---------------------------------------- | ------- | ------- | ---------- | ---------- | ----------------- |
| + [implementation](#implementation )     | No      | const   | No         | -          | -                 |
| - [chunk_size](#chunk_size )             | No      | integer | No         | -          | Chunk Size        |
| - [chunk_overlap](#chunk_overlap )       | No      | integer | No         | -          | Chunk Overlap     |
| - [keep_separator](#keep_separator )     | No      | boolean | No         | -          | Keep Separator    |
| - [strip_whitespace](#strip_whitespace ) | No      | boolean | No         | -          | Strip Whitespace  |
| - [model](#model )                       | No      | string  | No         | -          | Model             |
| - [tokens_per_chunk](#tokens_per_chunk ) | No      | integer | No         | -          | Tokens Per Chunk  |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | Yes     |

Specific value: `"SentenceTransformersTokenTextSplitter"`

## <a name="chunk_size"></a>2. Property `chunk_size`

**Title:** Chunk Size

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `4000`    |

**Description:** Maximum size of chunks to return

## <a name="chunk_overlap"></a>3. Property `chunk_overlap`

**Title:** Chunk Overlap

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `50`      |

## <a name="keep_separator"></a>4. Property `keep_separator`

**Title:** Keep Separator

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `false`   |

**Description:** Whether to keep the separator in the chunks

## <a name="strip_whitespace"></a>5. Property `strip_whitespace`

**Title:** Strip Whitespace

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

**Description:** If `True`, strips whitespace from the start and end of every document

## <a name="model"></a>6. Property `model`

**Title:** Model

|              |                                             |
| ------------ | ------------------------------------------- |
| **Type**     | `string`                                    |
| **Required** | No                                          |
| **Default**  | `"sentence-transformers/all-mpnet-base-v2"` |

**Description:** Model name

## <a name="tokens_per_chunk"></a>7. Property `tokens_per_chunk`

**Title:** Tokens Per Chunk

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `null`    |

**Description:** Number of tokens per chunk

----------------------------------------------------------------------------------------------------------------------------
