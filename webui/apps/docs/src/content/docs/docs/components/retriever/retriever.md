---
title: Retriever
description: "Description of Retriever component"
---
# Retriever

- [1. [Optional] Property implementation](#implementation)
- [2. [Optional] Property max_num_results](#max_num_results)
- [3. [Optional] Property question_transformer](#question_transformer)
- [4. [Optional] Property document_retriever](#document_retriever)
- [5. [Optional] Property document_reranker](#document_reranker)
- [6. [Optional] Property result_summarizer](#result_summarizer)

**Title:** Retriever

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

Specific value: `"Retriever"`

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

----------------------------------------------------------------------------------------------------------------------------
