---
title: NLTKTextSplitter
description: "Description of NLTKTextSplitter component"
---

| Property                                 | Pattern | Type    | Deprecated | Definition | Title/Description |
| ---------------------------------------- | ------- | ------- | ---------- | ---------- | ----------------- |
| - [implementation](#implementation )     | No      | const   | No         | -          | NLTKTextSplitter  |
| - [chunk_size](#chunk_size )             | No      | integer | No         | -          | Chunk Size        |
| - [chunk_overlap](#chunk_overlap )       | No      | integer | No         | -          | Chunk Overlap     |
| - [keep_separator](#keep_separator )     | No      | boolean | No         | -          | Keep Separator    |
| - [strip_whitespace](#strip_whitespace ) | No      | boolean | No         | -          | Strip Whitespace  |
| - [separator](#separator )               | No      | string  | No         | -          | Separator         |
| - [language](#language )                 | No      | string  | No         | -          | Language          |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** NLTKTextSplitter

Specific value: `"NLTKTextSplitter"`

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
| **Default**  | `200`     |

**Description:** Overlap in characters between chunks

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

## <a name="separator"></a>6. Property `separator`

**Title:** Separator

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `"\n\n"` |

**Description:** Separator to split on

## <a name="language"></a>7. Property `language`

**Title:** Language

|              |             |
| ------------ | ----------- |
| **Type**     | `string`    |
| **Required** | No          |
| **Default**  | `"english"` |

**Description:** Language to use for tokenization

----------------------------------------------------------------------------------------------------------------------------
