---
title: VectaraSearch
description: Description of the VectaraSearch component
---

**Description:** A logic unit for searching in Vectara. Requires the VECTARA_API_KEY environment variable to be set for authentication.

| Property                                                   | Pattern | Type        | Deprecated | Definition | Title/Description         |
| ---------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------------- |
| + [implementation](#implementation )                       | No      | const       | No         | -          | Implementation            |
| + [corpus_key](#corpus_key )                               | No      | string      | No         | -          | Corpus Key                |
| - [description](#description )                             | No      | string      | No         | -          | Description               |
| - [vectara_url](#vectara_url )                             | No      | string      | No         | -          | Vectara Url               |
| - [read_document_enabled](#read_document_enabled )         | No      | boolean     | No         | -          | Read Document Enabled     |
| - [read_document_description](#read_document_description ) | No      | Combination | No         | -          | Read Document Description |

## <a name="implementation"></a>1. Property `implementation`

**Title:** Implementation

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | Yes     |

Specific value: `"VectaraSearch"`

## <a name="corpus_key"></a>2. Property `corpus_key`

**Title:** Corpus Key

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** The corpus key to search in.

## <a name="description"></a>3. Property `description`

**Title:** Description

|              |                                               |
| ------------ | --------------------------------------------- |
| **Type**     | `string`                                      |
| **Required** | No                                            |
| **Default**  | `"Search documents related to {corpus_key}."` |

**Description:** Description of the tool presented to LLM. Will be formatted with corpus_key.

## <a name="vectara_url"></a>4. Property `vectara_url`

**Title:** Vectara Url

|              |                             |
| ------------ | --------------------------- |
| **Type**     | `string`                    |
| **Required** | No                          |
| **Default**  | `"https://api.vectara.io/"` |

## <a name="read_document_enabled"></a>5. Property `read_document_enabled`

**Title:** Read Document Enabled

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `false`   |

**Description:** Enable read_document tool.

## <a name="read_document_description"></a>6. Property `read_document_description`

**Title:** Read Document Description

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"Read a document from {corpus_key}."`                                    |

**Description:** Description of the tool presented to LLM. Will be formatted with corpus_key.

| Any of(Option)                                |
| --------------------------------------------- |
| [item 0](#read_document_description_anyOf_i0) |
| [item 1](#read_document_description_anyOf_i1) |

### <a name="read_document_description_anyOf_i0"></a>6.1. Property `item 0`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

### <a name="read_document_description_anyOf_i1"></a>6.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

----------------------------------------------------------------------------------------------------------------------------
