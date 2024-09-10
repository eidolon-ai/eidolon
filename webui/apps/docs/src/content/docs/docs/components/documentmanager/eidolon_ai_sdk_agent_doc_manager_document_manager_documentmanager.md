---
title: eidolon_ai_sdk.agent.doc_manager.document_manager.DocumentManager
description: Description of eidolon_ai_sdk.agent.doc_manager.document_manager.DocumentManager component
---

**Description:** Manages a collection of documents and provides search functionality. Automatically embeds and syncs documents (
provided by loader) into similarity memory where they can be searched.

| Property                                   | Pattern | Type                         | Deprecated | Definition                                 | Title/Description                                                 |
| ------------------------------------------ | ------- | ---------------------------- | ---------- | ------------------------------------------ | ----------------------------------------------------------------- |
| - [implementation](#implementation )       | No      | const                        | No         | -                                          | eidolon_ai_sdk.agent.doc_manager.document_manager.DocumentManager |
| + [name](#name )                           | No      | string                       | No         | -                                          | Name                                                              |
| - [recheck_frequency](#recheck_frequency ) | No      | integer                      | No         | -                                          | Recheck Frequency                                                 |
| - [loader](#loader )                       | No      | Reference[DocumentLoader]    | No         | In [DocumentLoader](/docs/components/documentloader/overview)    | Overview of DocumentLoader components                             |
| - [doc_processor](#doc_processor )         | No      | Reference[DocumentProcessor] | No         | In [DocumentProcessor](/docs/components/documentprocessor/overview) | Overview of DocumentProcessor components                          |
| - [concurrency](#concurrency )             | No      | integer                      | No         | -                                          | Concurrency                                                       |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** eidolon_ai_sdk.agent.doc_manager.document_manager.DocumentManager

Specific value: `"eidolon_ai_sdk.agent.doc_manager.document_manager.DocumentManager"`

## <a name="name"></a>2. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** The name of the document manager (used to name database collections).

## <a name="recheck_frequency"></a>3. Property `recheck_frequency`

**Title:** Recheck Frequency

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `60`      |

**Description:** The number of seconds between checks.

## <a name="loader"></a>4. Property `loader`

|                |                                        |
| -------------- | -------------------------------------- |
| **Type**       | `Reference[DocumentLoader]`            |
| **Required**   | No                                     |
| **Default**    | `{"implementation": "DocumentLoader"}` |
| **Defined in** | [DocumentLoader](/docs/components/documentloader/overview)   |

**Description:** Overview of DocumentLoader components

## <a name="doc_processor"></a>5. Property `doc_processor`

|                |                                           |
| -------------- | ----------------------------------------- |
| **Type**       | `Reference[DocumentProcessor]`            |
| **Required**   | No                                        |
| **Default**    | `{"implementation": "DocumentProcessor"}` |
| **Defined in** | [DocumentProcessor](/docs/components/documentprocessor/overview)   |

**Description:** Overview of DocumentProcessor components

## <a name="concurrency"></a>6. Property `concurrency`

**Title:** Concurrency

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `8`       |

**Description:** The number of concurrent tasks to run.

----------------------------------------------------------------------------------------------------------------------------
