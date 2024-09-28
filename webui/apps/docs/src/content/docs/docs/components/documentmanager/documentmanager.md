---
title: DocumentManager
description: "Description of DocumentManager component"
---
# DocumentManager

- [1. [Optional] Property implementation](#implementation)
- [2. [Required] Property name](#name)
- [3. [Optional] Property recheck_frequency](#recheck_frequency)
- [4. [Optional] Property loader](#loader)
- [5. [Optional] Property concurrency](#concurrency)
- [6. [Optional] Property doc_processor](#doc_processor)

**Title:** DocumentManager

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

Specific value: `"DocumentManager"`

</blockquote>
</details>

<details>
<summary>
<strong> <a name="name"></a>2. [Required] Property name</strong>  

</summary>
<blockquote>

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** The name of the document manager (used to name database collections).

</blockquote>
</details>

<details>
<summary>
<strong> <a name="recheck_frequency"></a>3. [Optional] Property recheck_frequency</strong>  

</summary>
<blockquote>

**Title:** Recheck Frequency

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `60`      |

**Description:** The number of seconds between checks.

</blockquote>
</details>

<details>
<summary>
<strong> <a name="loader"></a>4. [Optional] Property loader</strong>  

</summary>
<blockquote>

|              |                                        |
| ------------ | -------------------------------------- |
| **Type**     | [`Reference[DocumentLoader]`](/docs/components/documentloader/overview)            |
| **Required** | No                                     |
| **Default**  | `{"implementation": "DocumentLoader"}` |

</blockquote>
</details>

<details>
<summary>
<strong> <a name="concurrency"></a>5. [Optional] Property concurrency</strong>  

</summary>
<blockquote>

**Title:** Concurrency

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `8`       |

**Description:** The number of concurrent tasks to run.

</blockquote>
</details>

<details>
<summary>
<strong> <a name="doc_processor"></a>6. [Optional] Property doc_processor</strong>  

</summary>
<blockquote>

|              |                                           |
| ------------ | ----------------------------------------- |
| **Type**     | [`Reference[DocumentProcessor]`](/docs/components/documentprocessor/overview)            |
| **Required** | No                                        |
| **Default**  | `{"implementation": "DocumentProcessor"}` |

</blockquote>
</details>

----------------------------------------------------------------------------------------------------------------------------
