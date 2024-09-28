---
title: RetrieverAgent
description: Description of the RetrieverAgent component
---

**Title:** RetrieverAgent

|                           |                                                         |
| ------------------------- | ------------------------------------------------------- |
| **Type**                  | `object`                                                |
| **Required**              | No                                                      |
| **Additional properties** | [[Not allowed]](# "Additional Properties not allowed.") |

<details>
<summary>
<strong> [Optional] Property implementation</strong>  

</summary>
<blockquote>

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

Specific value: `"RetrieverAgent"`

</blockquote>
</details>

<details>
<summary>
<strong> [Optional] Property max_num_results</strong>  

</summary>
<blockquote>

**Title:** Max Num Results

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `10`      |

**Description:** The maximum number of results to consider.

</blockquote>
</details>

<details>
<summary>
<strong> [Optional] Property question_transformer</strong>  

</summary>
<blockquote>

|              |                                             |
| ------------ | ------------------------------------------- |
| **Type**     | [`Reference[QuestionTransformer]`](/docs/components/questiontransformer/overview)            |
| **Required** | No                                          |
| **Default**  | `{"implementation": "QuestionTransformer"}` |

</blockquote>
</details>

<details>
<summary>
<strong> [Optional] Property document_retriever</strong>  

</summary>
<blockquote>

|              |                                           |
| ------------ | ----------------------------------------- |
| **Type**     | [`Reference[DocumentRetriever]`](/docs/components/documentretriever/overview)            |
| **Required** | No                                        |
| **Default**  | `{"implementation": "DocumentRetriever"}` |

</blockquote>
</details>

<details>
<summary>
<strong> [Optional] Property document_reranker</strong>  

</summary>
<blockquote>

|              |                                          |
| ------------ | ---------------------------------------- |
| **Type**     | [`Reference[DocumentReranker]`](/docs/components/documentreranker/overview)            |
| **Required** | No                                       |
| **Default**  | `{"implementation": "DocumentReranker"}` |

</blockquote>
</details>

<details>
<summary>
<strong> [Optional] Property result_summarizer</strong>  

</summary>
<blockquote>

|              |                                          |
| ------------ | ---------------------------------------- |
| **Type**     | [`Reference[ResultSummarizer]`](/docs/components/resultsummarizer/overview)            |
| **Required** | No                                       |
| **Default**  | `{"implementation": "ResultSummarizer"}` |

</blockquote>
</details>

<details>
<summary>
<strong> [Required] Property name</strong>  

</summary>
<blockquote>

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** The name of the document store to use.

</blockquote>
</details>

<details>
<summary>
<strong> [Required] Property description</strong>  

</summary>
<blockquote>

**Title:** Description

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** A detailed description of the the retriever including all necessary information for the calling agent to decide to call this agent, i.e. file type or location or etc...

</blockquote>
</details>

<details>
<summary>
<strong> [Optional] Property loader_root_location</strong>  

</summary>
<blockquote>

**Title:** Loader Root Location

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

**Description:** A URL specifying the root location of the loader.

</blockquote>
</details>

<details>
<summary>
<strong> [Optional] Property loader_pattern</strong>  

</summary>
<blockquote>

**Title:** Loader Pattern

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"**/*"`                                                                  |

**Description:** The search pattern to use when loading files.

<blockquote>

| Any of(Option)                     |
| ---------------------------------- |
| [item 0](#loader_pattern_anyOf_i0) |
| [item 1](#loader_pattern_anyOf_i1) |

<blockquote>

## <a name="loader_pattern_anyOf_i0"></a>1. Property `item 0`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

</blockquote>
<blockquote>

## <a name="loader_pattern_anyOf_i1"></a>2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

</blockquote>

</blockquote>

</blockquote>
</details>

<details>
<summary>
<strong> [Optional] Property document_manager</strong>  

</summary>
<blockquote>

|              |                              |
| ------------ | ---------------------------- |
| **Type**     | [`Reference[DocumentManager]`](/docs/components/documentmanager/overview) |
| **Required** | No                           |
| **Default**  | `null`                       |

</blockquote>
</details>

<details>
<summary>
<strong> [Optional] Property apu</strong>  

</summary>
<blockquote>

|              |                             |
| ------------ | --------------------------- |
| **Type**     | [`Reference[APU]`](/docs/components/apu/overview)            |
| **Required** | No                          |
| **Default**  | `{"implementation": "APU"}` |

**Description:** The APU to use for question transformation.

</blockquote>
</details>

----------------------------------------------------------------------------------------------------------------------------
