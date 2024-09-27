---
title: TokenTextSplitter
description: "Description of TokenTextSplitter component"
---

| Property                                     | Pattern | Type        | Deprecated | Definition | Title/Description  |
| -------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#implementation )         | No      | const       | No         | -          | -                  |
| - [chunk_size](#chunk_size )                 | No      | integer     | No         | -          | Chunk Size         |
| - [chunk_overlap](#chunk_overlap )           | No      | integer     | No         | -          | Chunk Overlap      |
| - [keep_separator](#keep_separator )         | No      | boolean     | No         | -          | Keep Separator     |
| - [strip_whitespace](#strip_whitespace )     | No      | boolean     | No         | -          | Strip Whitespace   |
| - [encoding_name](#encoding_name )           | No      | string      | No         | -          | Encoding Name      |
| - [model](#model )                           | No      | string      | No         | -          | Model              |
| - [allowed_special](#allowed_special )       | No      | Combination | No         | -          | Allowed Special    |
| - [disallowed_special](#disallowed_special ) | No      | Combination | No         | -          | Disallowed Special |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

Specific value: `"TokenTextSplitter"`

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

## <a name="encoding_name"></a>6. Property `encoding_name`

**Title:** Encoding Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `"gpt2"` |

**Description:** Encoding name

## <a name="model"></a>7. Property `model`

**Title:** Model

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

**Description:** Model name

## <a name="allowed_special"></a>8. Property `allowed_special`

**Title:** Allowed Special

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `[]`                                                                      |

**Description:** Allowed special tokens

| Any of(Option)                      |
| ----------------------------------- |
| [item 0](#allowed_special_anyOf_i0) |
| [item 1](#allowed_special_anyOf_i1) |

### <a name="allowed_special_anyOf_i0"></a>8.1. Property `item 0`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

Must be one of:
* "all"
Specific value: `"all"`

### <a name="allowed_special_anyOf_i1"></a>8.2. Property `item 1`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of string` |
| **Required** | No                |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                 | Description |
| ----------------------------------------------- | ----------- |
| [item 1 items](#allowed_special_anyOf_i1_items) | -           |

#### <a name="autogenerated_heading_2"></a>8.2.1. item 1 items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

## <a name="disallowed_special"></a>9. Property `disallowed_special`

**Title:** Disallowed Special

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"all"`                                                                   |

**Description:** Disallowed special tokens

| Any of(Option)                         |
| -------------------------------------- |
| [item 0](#disallowed_special_anyOf_i0) |
| [item 1](#disallowed_special_anyOf_i1) |

### <a name="disallowed_special_anyOf_i0"></a>9.1. Property `item 0`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

Must be one of:
* "all"
Specific value: `"all"`

### <a name="disallowed_special_anyOf_i1"></a>9.2. Property `item 1`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of string` |
| **Required** | No                |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                    | Description |
| -------------------------------------------------- | ----------- |
| [item 1 items](#disallowed_special_anyOf_i1_items) | -           |

#### <a name="autogenerated_heading_3"></a>9.2.1. item 1 items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

----------------------------------------------------------------------------------------------------------------------------
