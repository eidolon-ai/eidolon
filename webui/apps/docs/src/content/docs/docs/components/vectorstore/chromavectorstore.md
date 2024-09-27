---
title: ChromaVectorStore
description: "Description of ChromaVectorStore component"
---

| Property                                               | Pattern | Type   | Deprecated | Definition | Title/Description       |
| ------------------------------------------------------ | ------- | ------ | ---------- | ---------- | ----------------------- |
| - [implementation](#implementation )                   | No      | const  | No         | -          | -                       |
| - [root_document_directory](#root_document_directory ) | No      | string | No         | -          | Root Document Directory |
| - [url](#url )                                         | No      | string | No         | -          | Url                     |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

Specific value: `"ChromaVectorStore"`

## <a name="root_document_directory"></a>2. Property `root_document_directory`

**Title:** Root Document Directory

|              |                   |
| ------------ | ----------------- |
| **Type**     | `string`          |
| **Required** | No                |
| **Default**  | `"vector_memory"` |

**Description:** The root directory where the vector memory will store documents.

## <a name="url"></a>3. Property `url`

**Title:** Url

|              |                                             |
| ------------ | ------------------------------------------- |
| **Type**     | `string`                                    |
| **Required** | No                                          |
| **Default**  | `"file://${EIDOLON_DATA_DIR}/doc_producer"` |

**Description:** The url of the chroma database. Use http(s)://$HOST:$PORT?header1=value1&header2=value2 to pass headers to the database.Use file://$PATH to use a local file database.

----------------------------------------------------------------------------------------------------------------------------
