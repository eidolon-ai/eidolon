---
title: DocumentManager
description: "Description of DocumentManager component"
---
| Property                                   | Pattern | Type                         | Deprecated | Definition | Title/Description |
| ------------------------------------------ | ------- | ---------------------------- | ---------- | ---------- | ----------------- |
| - [implementation](#implementation )       | No      | const                        | No         | -          | -                 |
| + [name](#name )                           | No      | string                       | No         | -          | Name              |
| - [recheck_frequency](#recheck_frequency ) | No      | integer                      | No         | -          | Recheck Frequency |
| - [loader](#loader )                       | No      | [Reference[DocumentLoader]](/docs/components/documentloader/overview)    | No         | -          | -                 |
| - [concurrency](#concurrency )             | No      | integer                      | No         | -          | Concurrency       |
| - [doc_processor](#doc_processor )         | No      | [Reference[DocumentProcessor]](/docs/components/documentprocessor/overview) | No         | -          | -                 |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

Specific value: `"DocumentManager"`

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

|              |                                        |
| ------------ | -------------------------------------- |
| **Type**     | [`Reference[DocumentLoader]`](/docs/components/documentloader/overview)            |
| **Required** | No                                     |
| **Default**  | `{"implementation": "DocumentLoader"}` |

## <a name="concurrency"></a>5. Property `concurrency`

**Title:** Concurrency

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `8`       |

**Description:** The number of concurrent tasks to run.

## <a name="doc_processor"></a>6. Property `doc_processor`

|              |                                           |
| ------------ | ----------------------------------------- |
| **Type**     | [`Reference[DocumentProcessor]`](/docs/components/documentprocessor/overview)            |
| **Required** | No                                        |
| **Default**  | `{"implementation": "DocumentProcessor"}` |

----------------------------------------------------------------------------------------------------------------------------
