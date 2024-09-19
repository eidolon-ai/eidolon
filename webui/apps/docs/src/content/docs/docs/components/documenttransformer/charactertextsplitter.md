---
title: CharacterTextSplitter
description: "Description of CharacterTextSplitter component"
---

| Property                                     | Pattern | Type    | Deprecated | Definition | Title/Description     |
| -------------------------------------------- | ------- | ------- | ---------- | ---------- | --------------------- |
| + [implementation](#implementation )         | No      | const   | No         | -          | CharacterTextSplitter |
| - [chunk_size](#chunk_size )                 | No      | integer | No         | -          | Chunk Size            |
| - [chunk_overlap](#chunk_overlap )           | No      | integer | No         | -          | Chunk Overlap         |
| - [keep_separator](#keep_separator )         | No      | boolean | No         | -          | Keep Separator        |
| - [strip_whitespace](#strip_whitespace )     | No      | boolean | No         | -          | Strip Whitespace      |
| - [separator](#separator )                   | No      | string  | No         | -          | Separator             |
| - [is_separator_regex](#is_separator_regex ) | No      | boolean | No         | -          | Is Separator Regex    |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | Yes     |

**Description:** CharacterTextSplitter

Specific value: `"CharacterTextSplitter"`

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

## <a name="is_separator_regex"></a>7. Property `is_separator_regex`

**Title:** Is Separator Regex

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `false`   |

**Description:** Whether the separator is a regex

----------------------------------------------------------------------------------------------------------------------------
