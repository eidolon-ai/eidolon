---
title: WebSearch
description: Description of WebSearch component
---

| Property                                       | Pattern | Type             | Deprecated | Definition | Title/Description   |
| ---------------------------------------------- | ------- | ---------------- | ---------- | ---------- | ------------------- |
| - [summarizer](#summarizer )                   | No      | enum (of string) | No         | -          | Summarizer          |
| - [cse_id](#cse_id )                           | No      | string           | No         | -          | Cse Id              |
| - [cse_token](#cse_token )                     | No      | string           | No         | -          | Cse Token           |
| - [name](#name )                               | No      | string           | No         | -          | Name                |
| - [description](#description )                 | No      | string           | No         | -          | Description         |
| - [defaultDateRestrict](#defaultDateRestrict ) | No      | Combination      | No         | -          | Defaultdaterestrict |
| - [params](#params )                           | No      | Combination      | No         | -          | Params              |

## <a name="summarizer"></a>1. Property `summarizer`

**Title:** Summarizer

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | No                 |
| **Default**  | `"BeautifulSoup"`  |

Must be one of:
* "BeautifulSoup"
* "noop"

## <a name="cse_id"></a>2. Property `cse_id`

**Title:** Cse Id

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

## <a name="cse_token"></a>3. Property `cse_token`

**Title:** Cse Token

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

## <a name="name"></a>4. Property `name`

**Title:** Name

|              |            |
| ------------ | ---------- |
| **Type**     | `string`   |
| **Required** | No         |
| **Default**  | `"search"` |

## <a name="description"></a>5. Property `description`

**Title:** Description

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

## <a name="defaultDateRestrict"></a>6. Property `defaultDateRestrict`

**Title:** Defaultdaterestrict

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                          |
| --------------------------------------- |
| [item 0](#defaultDateRestrict_anyOf_i0) |
| [item 1](#defaultDateRestrict_anyOf_i1) |

### <a name="defaultDateRestrict_anyOf_i0"></a>6.1. Property `item 0`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

### <a name="defaultDateRestrict_anyOf_i1"></a>6.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

## <a name="params"></a>7. Property `params`

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

### <a name="params_anyOf_i0"></a>7.1. Property `item 0`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

### <a name="params_anyOf_i1"></a>7.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

----------------------------------------------------------------------------------------------------------------------------
