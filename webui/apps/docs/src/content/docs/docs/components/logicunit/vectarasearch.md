---
title: VectaraSearch
description: "Description of VectaraSearch component"
---
# VectaraSearch

- [1. [Optional] Property implementation](#implementation)
- [2. [Required] Property corpus_key](#corpus_key)
- [3. [Optional] Property description](#description)
- [4. [Optional] Property vectara_url](#vectara_url)

**Title:** VectaraSearch

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

Specific value: `"VectaraSearch"`

</blockquote>
</details>

<details>
<summary>
<strong> <a name="corpus_key"></a>2. [Required] Property corpus_key</strong>  

</summary>
<blockquote>

**Title:** Corpus Key

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** The corpus key to search in.

</blockquote>
</details>

<details>
<summary>
<strong> <a name="description"></a>3. [Optional] Property description</strong>  

</summary>
<blockquote>

**Title:** Description

|              |                                               |
| ------------ | --------------------------------------------- |
| **Type**     | `string`                                      |
| **Required** | No                                            |
| **Default**  | `"Search documents related to {corpus_key}."` |

**Description:** Description of the tool presented to LLM. Will be formatted with corpus_key.

</blockquote>
</details>

<details>
<summary>
<strong> <a name="vectara_url"></a>4. [Optional] Property vectara_url</strong>  

</summary>
<blockquote>

**Title:** Vectara Url

|              |                             |
| ------------ | --------------------------- |
| **Type**     | `string`                    |
| **Required** | No                          |
| **Default**  | `"https://api.vectara.io/"` |

</blockquote>
</details>

----------------------------------------------------------------------------------------------------------------------------
