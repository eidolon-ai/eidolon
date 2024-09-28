---
title: RetrieverAgent
description: "Description of RetrieverAgent component"
---

# RetrieverAgent

- [1. [Optional] Property implementation](#implementation)
- [2. [Optional] Property max_num_results](#max_num_results)
- [3. [Optional] Property question_transformer](#question_transformer)
- [4. [Optional] Property document_retriever](#document_retriever)
- [5. [Optional] Property document_reranker](#document_reranker)
- [6. [Optional] Property result_summarizer](#result_summarizer)
- [7. [Required] Property name](#name)
- [8. [Required] Property description](#description)
- [9. [Optional] Property loader_root_location](#loader_root_location)
- [10. [Optional] Property loader_pattern](#loader_pattern)
  - [10.1. Property `item 0`](#loader_pattern_anyOf_i0)
  - [10.2. Property `item 1`](#loader_pattern_anyOf_i1)
- [11. [Optional] Property document_manager](#document_manager)
- [12. [Optional] Property apu](#apu)

<details>
<summary>
<strong> <a name="implementation"></a>1. [Optional] Property implementation</strong>  

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
<strong> <a name="max_num_results"></a>2. [Optional] Property max_num_results</strong>  

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
<strong> <a name="question_transformer"></a>3. [Optional] Property question_transformer</strong>  

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
<strong> <a name="document_retriever"></a>4. [Optional] Property document_retriever</strong>  

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
<strong> <a name="document_reranker"></a>5. [Optional] Property document_reranker</strong>  

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
<strong> <a name="result_summarizer"></a>6. [Optional] Property result_summarizer</strong>  

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
<strong> <a name="name"></a>7. [Required] Property name</strong>  

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
<strong> <a name="description"></a>8. [Required] Property description</strong>  

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
<strong> <a name="loader_root_location"></a>9. [Optional] Property loader_root_location</strong>  

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
<strong> <a name="loader_pattern"></a>10. [Optional] Property loader_pattern</strong>  

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

### <a name="loader_pattern_anyOf_i0"></a>10.1. Property `item 0`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

</blockquote>
<blockquote>

### <a name="loader_pattern_anyOf_i1"></a>10.2. Property `item 1`

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
<strong> <a name="document_manager"></a>11. [Optional] Property document_manager</strong>  

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
<strong> <a name="apu"></a>12. [Optional] Property apu</strong>  

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
