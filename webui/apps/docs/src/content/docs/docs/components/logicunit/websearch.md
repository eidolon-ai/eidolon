---
title: WebSearch
description: Description of WebSearch component
---
# WebSearch

- [1. Property `WebSearch > summarizer`](#summarizer)
- [2. Property `WebSearch > cse_id`](#cse_id)
- [3. Property `WebSearch > cse_token`](#cse_token)
- [4. Property `WebSearch > name`](#name)
- [5. Property `WebSearch > description`](#description)
- [6. Property `WebSearch > defaultDateRestrict`](#defaultDateRestrict)
  - [6.1. Property `WebSearch > defaultDateRestrict > anyOf > item 0`](#defaultDateRestrict_anyOf_i0)
  - [6.2. Property `WebSearch > defaultDateRestrict > anyOf > item 1`](#defaultDateRestrict_anyOf_i1)
- [7. Property `WebSearch > params`](#params)
  - [7.1. Property `WebSearch > params > anyOf > item 0`](#params_anyOf_i0)
  - [7.2. Property `WebSearch > params > anyOf > item 1`](#params_anyOf_i1)

**Title:** WebSearch

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

| Property                                       | Pattern | Type             | Deprecated | Definition | Title/Description   |
| ---------------------------------------------- | ------- | ---------------- | ---------- | ---------- | ------------------- |
| - [summarizer](#summarizer )                   | No      | enum (of string) | No         | -          | Summarizer          |
| - [cse_id](#cse_id )                           | No      | string           | No         | -          | Cse Id              |
| - [cse_token](#cse_token )                     | No      | string           | No         | -          | Cse Token           |
| - [name](#name )                               | No      | string           | No         | -          | Name                |
| - [description](#description )                 | No      | string           | No         | -          | Description         |
| - [defaultDateRestrict](#defaultDateRestrict ) | No      | Combination      | No         | -          | Defaultdaterestrict |
| - [params](#params )                           | No      | Combination      | No         | -          | Params              |

## <a name="summarizer"></a>1. Property `WebSearch > summarizer`

**Title:** Summarizer

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | No                 |
| **Default**  | `"BeautifulSoup"`  |

Must be one of:
* "BeautifulSoup"
* "noop"

## <a name="cse_id"></a>2. Property `WebSearch > cse_id`

**Title:** Cse Id

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

## <a name="cse_token"></a>3. Property `WebSearch > cse_token`

**Title:** Cse Token

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

## <a name="name"></a>4. Property `WebSearch > name`

**Title:** Name

|              |            |
| ------------ | ---------- |
| **Type**     | `string`   |
| **Required** | No         |
| **Default**  | `"search"` |

## <a name="description"></a>5. Property `WebSearch > description`

**Title:** Description

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

## <a name="defaultDateRestrict"></a>6. Property `WebSearch > defaultDateRestrict`

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

### <a name="defaultDateRestrict_anyOf_i0"></a>6.1. Property `WebSearch > defaultDateRestrict > anyOf > item 0`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

### <a name="defaultDateRestrict_anyOf_i1"></a>6.2. Property `WebSearch > defaultDateRestrict > anyOf > item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

## <a name="params"></a>7. Property `WebSearch > params`

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

### <a name="params_anyOf_i0"></a>7.1. Property `WebSearch > params > anyOf > item 0`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

### <a name="params_anyOf_i1"></a>7.2. Property `WebSearch > params > anyOf > item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

----------------------------------------------------------------------------------------------------------------------------
