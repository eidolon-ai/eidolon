---
title: VectaraSearch
description: "Description of VectaraSearch component"
---

| Property                             | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------ | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#implementation ) | No      | const  | No         | -          | -                 |
| + [corpus_key](#corpus_key )         | No      | string | No         | -          | Corpus Key        |
| - [description](#description )       | No      | string | No         | -          | Description       |
| - [vectara_url](#vectara_url )       | No      | string | No         | -          | Vectara Url       |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

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

----------------------------------------------------------------------------------------------------------------------------
