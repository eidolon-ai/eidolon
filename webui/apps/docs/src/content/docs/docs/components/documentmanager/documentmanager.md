---
title: DocumentManager
description: Description of DocumentManager component
---

**Description:** Manages a collection of documents and provides search functionality. Automatically embeds and syncs documents (
provided by loader) into similarity memory where they can be searched.

| Property                                   | Pattern | Type    | Deprecated | Definition | Title/Description |
| ------------------------------------------ | ------- | ------- | ---------- | ---------- | ----------------- |
| - [implementation](#implementation )       | No      | const   | No         | -          | DocumentManager   |
| + [name](#name )                           | No      | string  | No         | -          | Name              |
| - [recheck_frequency](#recheck_frequency ) | No      | integer | No         | -          | Recheck Frequency |
| - [loader](#loader )                       | No      | object  | No         | -          | DocumentLoader    |
| - [doc_processor](#doc_processor )         | No      | object  | No         | -          | DocumentProcessor |
| - [concurrency](#concurrency )             | No      | integer | No         | -          | Concurrency       |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** DocumentManager

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

**Title:** DocumentLoader

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{"implementation": "FilesystemLoader"}`                                  |

**Description:** Overview of DocumentLoader components

| Property                                    | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#loader_implementation ) | No      | string | No         | -          | -                 |

### <a name="loader_implementation"></a>4.1. Property `implementation`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

## <a name="doc_processor"></a>5. Property `doc_processor`

**Title:** DocumentProcessor

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{"implementation": "DocumentProcessor"}`                                 |

**Description:** Overview of DocumentProcessor components

| Property                                           | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#doc_processor_implementation ) | No      | string | No         | -          | -                 |

### <a name="doc_processor_implementation"></a>5.1. Property `implementation`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

## <a name="concurrency"></a>6. Property `concurrency`

**Title:** Concurrency

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `8`       |

**Description:** The number of concurrent tasks to run.

----------------------------------------------------------------------------------------------------------------------------
