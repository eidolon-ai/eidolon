---
title: DocumentManager
description: Description of DocumentManager component
---
# DocumentManager

- [1. Property `DocumentManager > name`](#name)
- [2. Property `DocumentManager > recheck_frequency`](#recheck_frequency)
- [3. Property `DocumentManager > loader`](#loader)
- [4. Property `DocumentManager > doc_processor`](#doc_processor)

**Title:** DocumentManager

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

**Description:** Manages a collection of documents and provides search functionality. Automatically embeds and syncs documents (
provided by loader) into similarity memory where they can be searched.

| Property                                   | Pattern | Type                         | Deprecated | Definition | Title/Description           |
| ------------------------------------------ | ------- | ---------------------------- | ---------- | ---------- | --------------------------- |
| + [name](#name )                           | No      | string                       | No         | -          | Name                        |
| - [recheck_frequency](#recheck_frequency ) | No      | integer                      | No         | -          | Recheck Frequency           |
| - [loader](#loader )                       | No      | [Reference[DocumentLoader]](/docs/components/documentloader/overview/)    | No         | -          | DocumentLoader Reference    |
| - [doc_processor](#doc_processor )         | No      | Reference[DocumentProcessor] | No         | -          | DocumentProcessor Reference |

## <a name="name"></a>1. Property `DocumentManager > name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** The name of the document manager (used to name database collections).

## <a name="recheck_frequency"></a>2. Property `DocumentManager > recheck_frequency`

**Title:** Recheck Frequency

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `60`      |

**Description:** The number of seconds between checks.

## <a name="loader"></a>3. Property `DocumentManager > loader`

**Title:** DocumentLoader Reference

|              |                             |
| ------------ | --------------------------- |
| **Type**     | `[Reference[DocumentLoader]](/docs/components/documentloader/overview/)` |
| **Required** | No                          |
| **Default**  | `"DocumentLoader"`          |

## <a name="doc_processor"></a>4. Property `DocumentManager > doc_processor`

**Title:** DocumentProcessor Reference

|              |                                |
| ------------ | ------------------------------ |
| **Type**     | `Reference[DocumentProcessor]` |
| **Required** | No                             |
| **Default**  | `"DocumentProcessor"`          |

----------------------------------------------------------------------------------------------------------------------------
