---
title: SpacyTextSplitter
description: "Description of SpacyTextSplitter component"
---
# SpacyTextSplitter

- [1. [Optional] Property implementation](#implementation)
- [2. [Optional] Property chunk_size](#chunk_size)
- [3. [Optional] Property chunk_overlap](#chunk_overlap)
- [4. [Optional] Property keep_separator](#keep_separator)
- [5. [Optional] Property strip_whitespace](#strip_whitespace)
- [6. [Optional] Property separator](#separator)
- [7. [Optional] Property pipeline](#pipeline)
- [8. [Optional] Property max_length](#max_length)

**Title:** SpacyTextSplitter

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

Specific value: `"SpacyTextSplitter"`

</blockquote>
</details>

<details>
<summary>
<strong> <a name="chunk_size"></a>2. [Optional] Property chunk_size</strong>  

</summary>
<blockquote>

**Title:** Chunk Size

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `4000`    |

**Description:** Maximum size of chunks to return

</blockquote>
</details>

<details>
<summary>
<strong> <a name="chunk_overlap"></a>3. [Optional] Property chunk_overlap</strong>  

</summary>
<blockquote>

**Title:** Chunk Overlap

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `200`     |

**Description:** Overlap in characters between chunks

</blockquote>
</details>

<details>
<summary>
<strong> <a name="keep_separator"></a>4. [Optional] Property keep_separator</strong>  

</summary>
<blockquote>

**Title:** Keep Separator

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `false`   |

**Description:** Whether to keep the separator in the chunks

</blockquote>
</details>

<details>
<summary>
<strong> <a name="strip_whitespace"></a>5. [Optional] Property strip_whitespace</strong>  

</summary>
<blockquote>

**Title:** Strip Whitespace

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

**Description:** If `True`, strips whitespace from the start and end of every document

</blockquote>
</details>

<details>
<summary>
<strong> <a name="separator"></a>6. [Optional] Property separator</strong>  

</summary>
<blockquote>

**Title:** Separator

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `"\n\n"` |

**Description:** Separator to split on

</blockquote>
</details>

<details>
<summary>
<strong> <a name="pipeline"></a>7. [Optional] Property pipeline</strong>  

</summary>
<blockquote>

**Title:** Pipeline

|              |                    |
| ------------ | ------------------ |
| **Type**     | `string`           |
| **Required** | No                 |
| **Default**  | `"en_core_web_sm"` |

**Description:** Spacy pipeline to use

</blockquote>
</details>

<details>
<summary>
<strong> <a name="max_length"></a>8. [Optional] Property max_length</strong>  

</summary>
<blockquote>

**Title:** Max Length

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `1000000` |

**Description:** Maximum length of characters to process

</blockquote>
</details>

----------------------------------------------------------------------------------------------------------------------------
