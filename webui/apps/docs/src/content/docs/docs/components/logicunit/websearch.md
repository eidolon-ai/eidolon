---
title: WebSearchConfig
description: "Description of WebSearchConfig component"
---
# WebSearchConfig

- [1. [Optional] Property implementation](#implementation)
- [2. [Optional] Property summarizer](#summarizer)
- [3. [Optional] Property cse_id](#cse_id)
- [4. [Optional] Property cse_token](#cse_token)
- [5. [Optional] Property name](#name)
- [6. [Optional] Property description](#description)
- [7. [Optional] Property defaultDateRestrict](#defaultDateRestrict)
- [8. [Optional] Property params](#params)
  - [8.1. Property `item 0`](#params_anyOf_i0)
  - [8.2. Property `item 1`](#params_anyOf_i1)

**Title:** WebSearchConfig

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

Specific value: `"WebSearch"`

</blockquote>
</details>

<details>
<summary>
<strong> <a name="summarizer"></a>2. [Optional] Property summarizer</strong>  

</summary>
<blockquote>

**Title:** Summarizer

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | No                 |
| **Default**  | `"BeautifulSoup"`  |

Must be one of:
* "BeautifulSoup"
* "noop"

</blockquote>
</details>

<details>
<summary>
<strong> <a name="cse_id"></a>3. [Optional] Property cse_id</strong>  

</summary>
<blockquote>

**Title:** Cse Id

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Google Custom Search Engine Id.

</blockquote>
</details>

<details>
<summary>
<strong> <a name="cse_token"></a>4. [Optional] Property cse_token</strong>  

</summary>
<blockquote>

**Title:** Cse Token

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Google Project dev token, must have search permissions.

</blockquote>
</details>

<details>
<summary>
<strong> <a name="name"></a>5. [Optional] Property name</strong>  

</summary>
<blockquote>

**Title:** Name

|              |            |
| ------------ | ---------- |
| **Type**     | `string`   |
| **Required** | No         |
| **Default**  | `"search"` |

</blockquote>
</details>

<details>
<summary>
<strong> <a name="description"></a>6. [Optional] Property description</strong>  

</summary>
<blockquote>

**Title:** Description

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

</blockquote>
</details>

<details>
<summary>
<strong> <a name="defaultDateRestrict"></a>7. [Optional] Property defaultDateRestrict</strong>  

</summary>
<blockquote>

**Title:** Defaultdaterestrict

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

</blockquote>
</details>

<details>
<summary>
<strong> <a name="params"></a>8. [Optional] Property params</strong>  

</summary>
<blockquote>

**Title:** Params

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

<blockquote>

| Any of(Option)             |
| -------------------------- |
| [item 0](#params_anyOf_i0) |
| [item 1](#params_anyOf_i1) |

<blockquote>

### <a name="params_anyOf_i0"></a>8.1. Property `item 0`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

</blockquote>
<blockquote>

### <a name="params_anyOf_i1"></a>8.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

</blockquote>

</blockquote>

</blockquote>
</details>

----------------------------------------------------------------------------------------------------------------------------
