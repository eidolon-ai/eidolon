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
| - [document_reranker](#document_reranker )       | No      | Reference[DocumentReranker]    | No         | -          | DocumentReranker Reference    |
| + [name](#name )                                 | No      | string                         | No         | -          | Name                          |
| + [description](#description )                   | No      | string                         | No         | -          | Description                   |
| - [loader_root_location](#loader_root_location ) | No      | string                         | No         | -          | Loader Root Location          |
| - [loader_pattern](#loader_pattern )             | No      | string                         | No         | -          | Loader Pattern                |
| + [document_manager](#document_manager )         | No      | [Reference[DocumentManager]](/docs/components/documentmanager/overview/)     | No         | -          | DocumentManager Reference     |

## <a name="max_num_results"></a>1. Property `max_num_results`

**Title:** Max Num Results

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `10`      |

**Description:** The maximum number of results to send to cpu.

## <a name="question_transformer"></a>2. Property `question_transformer`

**Title:** QuestionTransformer Reference

|              |                                  |
| ------------ | -------------------------------- |
| **Type**     | `Reference[QuestionTransformer]` |
| **Required** | No                               |
| **Default**  | `"QuestionTransformer"`          |

## <a name="document_reranker"></a>3. Property `document_reranker`

**Title:** DocumentReranker Reference

|              |                               |
| ------------ | ----------------------------- |
| **Type**     | `Reference[DocumentReranker]` |
| **Required** | No                            |
| **Default**  | `"DocumentReranker"`          |

## <a name="name"></a>4. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** The name of the document store to use.

## <a name="description"></a>5. Property `description`

**Title:** Description

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** A detailed description of the the retriever including all necessary information for the calling agent to decide to call this agent, i.e. file type or location or etc...

## <a name="loader_root_location"></a>6. Property `loader_root_location`

**Title:** Loader Root Location

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

**Description:** A URL specifying the root location of the loader.

## <a name="loader_pattern"></a>7. Property `loader_pattern`

**Title:** Loader Pattern

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `"**/*"` |

**Description:** The search pattern to use when loading files.

## <a name="document_manager"></a>8. Property `document_manager`

**Title:** DocumentManager Reference

|              |                                                                       |
| ------------ | --------------------------------------------------------------------- |
| **Type**     | `[Reference[DocumentManager]](/docs/components/documentmanager/overview/)`                                          |
| **Required** | Yes                                                                   |
| **Default**  | `"eidolon_ai_sdk.agent.doc_manager.document_manager.DocumentManager"` |

----------------------------------------------------------------------------------------------------------------------------
