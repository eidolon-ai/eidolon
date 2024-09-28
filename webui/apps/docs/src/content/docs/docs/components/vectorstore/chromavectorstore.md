---
title: ChromaVectorStore
description: "Description of ChromaVectorStore component"
---
# ChromaVectorStore

- [1. [Optional] Property implementation](#implementation)
- [2. [Optional] Property root_document_directory](#root_document_directory)
- [3. [Optional] Property url](#url)

**Title:** ChromaVectorStore

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

Specific value: `"ChromaVectorStore"`

</blockquote>
</details>

<details>
<summary>
<strong> <a name="root_document_directory"></a>2. [Optional] Property root_document_directory</strong>  

</summary>
<blockquote>

**Title:** Root Document Directory

|              |                   |
| ------------ | ----------------- |
| **Type**     | `string`          |
| **Required** | No                |
| **Default**  | `"vector_memory"` |

**Description:** The root directory where the vector memory will store documents.

</blockquote>
</details>

<details>
<summary>
<strong> <a name="url"></a>3. [Optional] Property url</strong>  

</summary>
<blockquote>

**Title:** Url

|              |                                             |
| ------------ | ------------------------------------------- |
| **Type**     | `string`                                    |
| **Required** | No                                          |
| **Default**  | `"file://${EIDOLON_DATA_DIR}/doc_producer"` |

**Description:** The url of the chroma database. Use http(s)://$HOST:$PORT?header1=value1&header2=value2 to pass headers to the database.Use file://$PATH to use a local file database.

</blockquote>
</details>

----------------------------------------------------------------------------------------------------------------------------
