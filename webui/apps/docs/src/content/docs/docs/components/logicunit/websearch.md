---
title: WebSearch
description: Description of the WebSearch component
---

| Property                                       | Pattern | Type             | Deprecated | Definition | Title/Description   |
| ---------------------------------------------- | ------- | ---------------- | ---------- | ---------- | ------------------- |
| + [implementation](#implementation )           | No      | const            | No         | -          | Implementation      |
| - [summarizer](#summarizer )                   | No      | enum (of string) | No         | -          | Summarizer          |
| - [cse_id](#cse_id )                           | No      | string           | No         | -          | Cse Id              |
| - [cse_token](#cse_token )                     | No      | string           | No         | -          | Cse Token           |
| - [name](#name )                               | No      | string           | No         | -          | Name                |
| - [description](#description )                 | No      | string           | No         | -          | Description         |
| - [defaultDateRestrict](#defaultDateRestrict ) | No      | string           | No         | -          | Defaultdaterestrict |
| - [params](#params )                           | No      | Combination      | No         | -          | Params              |

## <a name="implementation"></a>1. Property `implementation`

**Title:** Implementation

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | Yes     |

Specific value: `"WebSearch"`

## <a name="summarizer"></a>2. Property `summarizer`

**Title:** Summarizer

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | No                 |
| **Default**  | `"BeautifulSoup"`  |

Must be one of:
* "BeautifulSoup"
* "noop"

## <a name="cse_id"></a>3. Property `cse_id`

**Title:** Cse Id

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Google Custom Search Engine Id.

## <a name="cse_token"></a>4. Property `cse_token`

**Title:** Cse Token

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Google Project dev token, must have search permissions.

## <a name="name"></a>5. Property `name`

**Title:** Name

|              |            |
| ------------ | ---------- |
| **Type**     | `string`   |
| **Required** | No         |
| **Default**  | `"search"` |

## <a name="description"></a>6. Property `description`

**Title:** Description

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

## <a name="defaultDateRestrict"></a>7. Property `defaultDateRestrict`

**Title:** Defaultdaterestrict

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

## <a name="params"></a>8. Property `params`

**Title:** Params

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

| Any of(Option)             |
| -------------------------- |
| [item 0](#params_anyOf_i0) |
| [item 1](#params_anyOf_i1) |

### <a name="params_anyOf_i0"></a>8.1. Property `item 0`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

### <a name="params_anyOf_i1"></a>8.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

----------------------------------------------------------------------------------------------------------------------------
