---
title: Retriever
description: Description of Retriever component
---

| Property                                         | Pattern | Type                                                                            | Deprecated | Definition | Title/Description   |
| ------------------------------------------------ | ------- | ------------------------------------------------------------------------------- | ---------- | ---------- | ------------------- |
| - [implementation](#implementation )             | No      | const                                                                           | No         | -          | Retriever           |
| - [max_num_results](#max_num_results )           | No      | integer                                                                         | No         | -          | Max Num Results     |
| - [question_transformer](#question_transformer ) | No      | [Reference[QuestionTransformer]](/docs/components/questiontransformer/overview) | No         | -          | QuestionTransformer |
| - [document_retriever](#document_retriever )     | No      | [Reference[DocumentRetriever]](/docs/components/documentretriever/overview)     | No         | -          | DocumentRetriever   |
| - [document_reranker](#document_reranker )       | No      | [Reference[DocumentReranker]](/docs/components/documentreranker/overview)       | No         | -          | DocumentReranker    |
| - [result_summarizer](#result_summarizer )       | No      | [Reference[ResultSummarizer]](/docs/components/resultsummarizer/overview)       | No         | -          | ResultSummarizer    |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** Retriever

Specific value: `"Retriever"`

## <a name="max_num_results"></a>2. Property `max_num_results`

**Title:** Max Num Results

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `10`      |

**Description:** The maximum number of results to consider.

## <a name="question_transformer"></a>3. Property `question_transformer`

**Title:** QuestionTransformer

|              |                                                                                   |
| ------------ | --------------------------------------------------------------------------------- |
| **Type**     | [`Reference[QuestionTransformer]`](/docs/components/questiontransformer/overview) |
| **Required** | No                                                                                |
| **Default**  | `{"implementation": "QuestionTransformer"}`                                       |

**Description:** Overview of QuestionTransformer components

## <a name="document_retriever"></a>4. Property `document_retriever`

**Title:** DocumentRetriever

|              |                                                                               |
| ------------ | ----------------------------------------------------------------------------- |
| **Type**     | [`Reference[DocumentRetriever]`](/docs/components/documentretriever/overview) |
| **Required** | No                                                                            |
| **Default**  | `{"implementation": "DocumentRetriever"}`                                     |

**Description:** Overview of DocumentRetriever components

## <a name="document_reranker"></a>5. Property `document_reranker`

**Title:** DocumentReranker

|              |                                                                             |
| ------------ | --------------------------------------------------------------------------- |
| **Type**     | [`Reference[DocumentReranker]`](/docs/components/documentreranker/overview) |
| **Required** | No                                                                          |
| **Default**  | `{"implementation": "DocumentReranker"}`                                    |

**Description:** Overview of DocumentReranker components

## <a name="result_summarizer"></a>6. Property `result_summarizer`

**Title:** ResultSummarizer

|              |                                                                             |
| ------------ | --------------------------------------------------------------------------- |
| **Type**     | [`Reference[ResultSummarizer]`](/docs/components/resultsummarizer/overview) |
| **Required** | No                                                                          |
| **Default**  | `{"implementation": "ResultSummarizer"}`                                    |

**Description:** Overview of ResultSummarizer components

----------------------------------------------------------------------------------------------------------------------------
