---
title: Retriever
description: "Description of Retriever component"
---

| Property                                         | Pattern | Type                           | Deprecated | Definition                              | Title/Description                          |
| ------------------------------------------------ | ------- | ------------------------------ | ---------- | --------------------------------------- | ------------------------------------------ |
| + [implementation](#implementation )             | No      | const                          | No         | -                                       | Retriever                                  |
| - [max_num_results](#max_num_results )           | No      | integer                        | No         | -                                       | Max Num Results                            |
| - [question_transformer](#question_transformer ) | No      | Reference[QuestionTransformer] | No         | In [QuestionTransformer](/docs/components/questiontransformer/overview) | Overview of QuestionTransformer components |
| - [document_retriever](#document_retriever )     | No      | Reference[DocumentRetriever]   | No         | In [DocumentRetriever](/docs/components/documentretriever/overview)   | Overview of DocumentRetriever components   |
| - [document_reranker](#document_reranker )       | No      | Reference[DocumentReranker]    | No         | In [DocumentReranker](/docs/components/documentreranker/overview)    | Overview of DocumentReranker components    |
| - [result_summarizer](#result_summarizer )       | No      | Reference[ResultSummarizer]    | No         | In [ResultSummarizer](/docs/components/resultsummarizer/overview)    | Overview of ResultSummarizer components    |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | Yes     |

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

|                |                                             |
| -------------- | ------------------------------------------- |
| **Type**       | `Reference[QuestionTransformer]`            |
| **Required**   | No                                          |
| **Default**    | `{"implementation": "QuestionTransformer"}` |
| **Defined in** | [QuestionTransformer](/docs/components/questiontransformer/overview)        |

**Description:** Overview of QuestionTransformer components

## <a name="document_retriever"></a>4. Property `document_retriever`

|                |                                           |
| -------------- | ----------------------------------------- |
| **Type**       | `Reference[DocumentRetriever]`            |
| **Required**   | No                                        |
| **Default**    | `{"implementation": "DocumentRetriever"}` |
| **Defined in** | [DocumentRetriever](/docs/components/documentretriever/overview)        |

**Description:** Overview of DocumentRetriever components

## <a name="document_reranker"></a>5. Property `document_reranker`

|                |                                          |
| -------------- | ---------------------------------------- |
| **Type**       | `Reference[DocumentReranker]`            |
| **Required**   | No                                       |
| **Default**    | `{"implementation": "DocumentReranker"}` |
| **Defined in** | [DocumentReranker](/docs/components/documentreranker/overview)        |

**Description:** Overview of DocumentReranker components

## <a name="result_summarizer"></a>6. Property `result_summarizer`

|                |                                          |
| -------------- | ---------------------------------------- |
| **Type**       | `Reference[ResultSummarizer]`            |
| **Required**   | No                                       |
| **Default**    | `{"implementation": "ResultSummarizer"}` |
| **Defined in** | [ResultSummarizer](/docs/components/resultsummarizer/overview)        |

**Description:** Overview of ResultSummarizer components

----------------------------------------------------------------------------------------------------------------------------
