---
title: RetrieverAgent
description: Description of the RetrieverAgent component
---

**Description:** A RetrieverAgent is an agent that will take a query, rewrite it for better similarity vector search, and then perform the vector search on the document store.
The agent will dynamically load and embed files, so it is not performant for loading large bodies of files, but performs very well for small to medium-sized document stores (hundreds to thousands of documents) which are updating frequently.

| Property                                         | Pattern | Type                           | Deprecated | Definition | Title/Description                           |
| ------------------------------------------------ | ------- | ------------------------------ | ---------- | ---------- | ------------------------------------------- |
| + [implementation](#implementation )             | No      | const                          | No         | -          | Implementation                              |
| - [max_num_results](#max_num_results )           | No      | integer                        | No         | -          | Max Num Results                             |
| - [question_transformer](#question_transformer ) | No      | [Reference[QuestionTransformer]](/docs/components/questiontransformer/overview) | No         | -          | -                                           |
| - [document_retriever](#document_retriever )     | No      | [Reference[DocumentRetriever]](/docs/components/documentretriever/overview)   | No         | -          | -                                           |
| - [document_reranker](#document_reranker )       | No      | [Reference[DocumentReranker]](/docs/components/documentreranker/overview)    | No         | -          | -                                           |
| - [result_summarizer](#result_summarizer )       | No      | [Reference[ResultSummarizer]](/docs/components/resultsummarizer/overview)    | No         | -          | -                                           |
| + [name](#name )                                 | No      | string                         | No         | -          | Name                                        |
| + [description](#description )                   | No      | string                         | No         | -          | Description                                 |
| - [loader_root_location](#loader_root_location ) | No      | string                         | No         | -          | Loader Root Location                        |
| - [loader_pattern](#loader_pattern )             | No      | Combination                    | No         | -          | Loader Pattern                              |
| - [document_manager](#document_manager )         | No      | [Reference[DocumentManager]](/docs/components/documentmanager/overview)     | No         | -          | -                                           |
| - [apu](#apu )                                   | No      | [Reference[APU]](/docs/components/apu/overview)                 | No         | -          | The APU to use for question transformation. |
| - [sync_wait_time](#sync_wait_time )             | No      | integer                        | No         | -          | Sync Wait Time                              |

## <a name="implementation"></a>1. Property `implementation`

**Title:** Implementation

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | Yes     |

Specific value: `"RetrieverAgent"`

## <a name="max_num_results"></a>2. Property `max_num_results`

**Title:** Max Num Results

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `10`      |

**Description:** The maximum number of results to consider.

## <a name="question_transformer"></a>3. Property `question_transformer`

|              |                                             |
| ------------ | ------------------------------------------- |
| **Type**     | [`Reference[QuestionTransformer]`](/docs/components/questiontransformer/overview)            |
| **Required** | No                                          |
| **Default**  | `{"implementation": "QuestionTransformer"}` |

## <a name="document_retriever"></a>4. Property `document_retriever`

|              |                                           |
| ------------ | ----------------------------------------- |
| **Type**     | [`Reference[DocumentRetriever]`](/docs/components/documentretriever/overview)            |
| **Required** | No                                        |
| **Default**  | `{"implementation": "DocumentRetriever"}` |

## <a name="document_reranker"></a>5. Property `document_reranker`

|              |                                          |
| ------------ | ---------------------------------------- |
| **Type**     | [`Reference[DocumentReranker]`](/docs/components/documentreranker/overview)            |
| **Required** | No                                       |
| **Default**  | `{"implementation": "DocumentReranker"}` |

## <a name="result_summarizer"></a>6. Property `result_summarizer`

|              |                                          |
| ------------ | ---------------------------------------- |
| **Type**     | [`Reference[ResultSummarizer]`](/docs/components/resultsummarizer/overview)            |
| **Required** | No                                       |
| **Default**  | `{"implementation": "ResultSummarizer"}` |

## <a name="name"></a>7. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** The name of the document store to use.

## <a name="description"></a>8. Property `description`

**Title:** Description

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** A detailed description of the the retriever including all necessary information for the calling agent to decide to call this agent, i.e. file type or location or etc...

## <a name="loader_root_location"></a>9. Property `loader_root_location`

**Title:** Loader Root Location

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

**Description:** A URL specifying the root location of the loader.

## <a name="loader_pattern"></a>10. Property `loader_pattern`

**Title:** Loader Pattern

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"**/*"`                                                                  |

**Description:** The search pattern to use when loading files.

| Any of(Option)                     |
| ---------------------------------- |
| [item 0](#loader_pattern_anyOf_i0) |
| [item 1](#loader_pattern_anyOf_i1) |

### <a name="loader_pattern_anyOf_i0"></a>10.1. Property `item 0`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

### <a name="loader_pattern_anyOf_i1"></a>10.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

## <a name="document_manager"></a>11. Property `document_manager`

|              |                              |
| ------------ | ---------------------------- |
| **Type**     | [`Reference[DocumentManager]`](/docs/components/documentmanager/overview) |
| **Required** | No                           |
| **Default**  | `null`                       |

## <a name="apu"></a>12. Property `apu`

|              |                             |
| ------------ | --------------------------- |
| **Type**     | [`Reference[APU]`](/docs/components/apu/overview)            |
| **Required** | No                          |
| **Default**  | `{"implementation": "APU"}` |

**Description:** The APU to use for question transformation.

## <a name="sync_wait_time"></a>13. Property `sync_wait_time`

**Title:** Sync Wait Time

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `-1`      |

**Description:** The amount of time (seconds) to wait while documents sync before returning results.

----------------------------------------------------------------------------------------------------------------------------
