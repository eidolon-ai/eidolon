---
title: RetrieverAgent
description: Description of RetrieverAgent component
---

**Description:** A RetrieverAgent is an agent that will take a query, rewrite it for better similarity vector search, and then perform the vector search on the document store.
The agent will dynamically load and embed files, so it is not performant for loading large bodies of files, but performs very well for small to medium-sized document stores (hundreds to thousands of documents) which are updating frequently.

| Property                                         | Pattern | Type                           | Deprecated | Definition | Title/Description             |
| ------------------------------------------------ | ------- | ------------------------------ | ---------- | ---------- | ----------------------------- |
| - [max_num_results](#max_num_results )           | No      | integer                        | No         | -          | Max Num Results               |
| - [question_transformer](#question_transformer ) | No      | Reference[QuestionTransformer] | No         | -          | QuestionTransformer Reference |
| - [document_retriever](#document_retriever )     | No      | Reference[DocumentRetriever]   | No         | -          | DocumentRetriever Reference   |
| - [document_reranker](#document_reranker )       | No      | Reference[DocumentReranker]    | No         | -          | DocumentReranker Reference    |
| - [result_summarizer](#result_summarizer )       | No      | Reference[ResultSummarizer]    | No         | -          | ResultSummarizer Reference    |
| + [name](#name )                                 | No      | string                         | No         | -          | Name                          |
| + [description](#description )                   | No      | string                         | No         | -          | Description                   |
| - [loader_root_location](#loader_root_location ) | No      | Combination                    | No         | -          | Loader Root Location          |
| - [loader_pattern](#loader_pattern )             | No      | Combination                    | No         | -          | Loader Pattern                |
| - [document_manager](#document_manager )         | No      | Combination                    | No         | -          | -                             |

## <a name="max_num_results"></a>1. Property `max_num_results`

**Title:** Max Num Results

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `10`      |

**Description:** The maximum number of results to consider.

## <a name="question_transformer"></a>2. Property `question_transformer`

**Title:** QuestionTransformer Reference

|              |                                  |
| ------------ | -------------------------------- |
| **Type**     | `Reference[QuestionTransformer]` |
| **Required** | No                               |
| **Default**  | `"QuestionTransformer"`          |

## <a name="document_retriever"></a>3. Property `document_retriever`

**Title:** DocumentRetriever Reference

|              |                                |
| ------------ | ------------------------------ |
| **Type**     | `Reference[DocumentRetriever]` |
| **Required** | No                             |
| **Default**  | `"DocumentRetriever"`          |

## <a name="document_reranker"></a>4. Property `document_reranker`

**Title:** DocumentReranker Reference

|              |                               |
| ------------ | ----------------------------- |
| **Type**     | `Reference[DocumentReranker]` |
| **Required** | No                            |
| **Default**  | `"DocumentReranker"`          |

## <a name="result_summarizer"></a>5. Property `result_summarizer`

**Title:** ResultSummarizer Reference

|              |                               |
| ------------ | ----------------------------- |
| **Type**     | `Reference[ResultSummarizer]` |
| **Required** | No                            |
| **Default**  | `"ResultSummarizer"`          |

## <a name="name"></a>6. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** The name of the document store to use.

## <a name="description"></a>7. Property `description`

**Title:** Description

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** A detailed description of the the retriever including all necessary information for the calling agent to decide to call this agent, i.e. file type or location or etc...

## <a name="loader_root_location"></a>8. Property `loader_root_location`

**Title:** Loader Root Location

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

**Description:** A URL specifying the root location of the loader.

| Any of(Option)                           |
| ---------------------------------------- |
| [item 0](#loader_root_location_anyOf_i0) |
| [item 1](#loader_root_location_anyOf_i1) |

### <a name="loader_root_location_anyOf_i0"></a>8.1. Property `item 0`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

### <a name="loader_root_location_anyOf_i1"></a>8.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

## <a name="loader_pattern"></a>9. Property `loader_pattern`

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

### <a name="loader_pattern_anyOf_i0"></a>9.1. Property `item 0`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

### <a name="loader_pattern_anyOf_i1"></a>9.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

## <a name="document_manager"></a>10. Property `document_manager`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                          |
| ------------------------------------------------------- |
| [DocumentManager Reference](#document_manager_anyOf_i0) |
| [item 1](#document_manager_anyOf_i1)                    |

### <a name="document_manager_anyOf_i0"></a>10.1. Property `DocumentManager Reference`

**Title:** DocumentManager Reference

|              |                                                                       |
| ------------ | --------------------------------------------------------------------- |
| **Type**     | `[Reference[DocumentManager]](/docs/components/documentmanager/overview/)`                                          |
| **Required** | No                                                                    |
| **Default**  | `"eidolon_ai_sdk.agent.doc_manager.document_manager.DocumentManager"` |

### <a name="document_manager_anyOf_i1"></a>10.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

----------------------------------------------------------------------------------------------------------------------------
