---
title: RetrieverAgent
description: Description of RetrieverAgent component
---

**Description:** A RetrieverAgent is an agent that will take a query, rewrite it for better similarity vector search, and then perform the vector search on the document store.
The agent will dynamically load and embed files, so it is not performant for loading large bodies of files, but performs very well for small to medium-sized document stores (hundreds to thousands of documents) which are updating frequently.

| Property                                         | Pattern | Type        | Deprecated | Definition | Title/Description             |
| ------------------------------------------------ | ------- | ----------- | ---------- | ---------- | ----------------------------- |
| - [implementation](#implementation )             | No      | const       | No         | -          | RetrieverAgent                |
| - [max_num_results](#max_num_results )           | No      | integer     | No         | -          | Max Num Results               |
| - [question_transformer](#question_transformer ) | No      | object      | No         | -          | QuestionTransformer Reference |
| - [document_retriever](#document_retriever )     | No      | object      | No         | -          | DocumentRetriever Reference   |
| - [document_reranker](#document_reranker )       | No      | object      | No         | -          | DocumentReranker Reference    |
| - [result_summarizer](#result_summarizer )       | No      | object      | No         | -          | ResultSummarizer Reference    |
| + [name](#name )                                 | No      | string      | No         | -          | Name                          |
| + [description](#description )                   | No      | string      | No         | -          | Description                   |
| - [loader_root_location](#loader_root_location ) | No      | Combination | No         | -          | Loader Root Location          |
| - [loader_pattern](#loader_pattern )             | No      | Combination | No         | -          | Loader Pattern                |
| - [document_manager](#document_manager )         | No      | Combination | No         | -          | -                             |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** RetrieverAgent

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

**Title:** QuestionTransformer Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"QuestionTransformer"`                                                   |

| Property                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#question_transformer_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#question_transformer_additionalProperties )         | No      | object | No         | -          | -                 |

### <a name="question_transformer_implementation"></a>3.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

## <a name="document_retriever"></a>4. Property `document_retriever`

**Title:** DocumentRetriever Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"DocumentRetriever"`                                                     |

| Property                                                | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#document_retriever_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#document_retriever_additionalProperties )         | No      | object | No         | -          | -                 |

### <a name="document_retriever_implementation"></a>4.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

## <a name="document_reranker"></a>5. Property `document_reranker`

**Title:** DocumentReranker Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"DocumentReranker"`                                                      |

| Property                                               | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------ | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#document_reranker_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#document_reranker_additionalProperties )         | No      | object | No         | -          | -                 |

### <a name="document_reranker_implementation"></a>5.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

## <a name="result_summarizer"></a>6. Property `result_summarizer`

**Title:** ResultSummarizer Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"ResultSummarizer"`                                                      |

| Property                                               | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------ | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#result_summarizer_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#result_summarizer_additionalProperties )         | No      | object | No         | -          | -                 |

### <a name="result_summarizer_implementation"></a>6.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

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

### <a name="loader_root_location_anyOf_i0"></a>9.1. Property `item 0`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

### <a name="loader_root_location_anyOf_i1"></a>9.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

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

### <a name="document_manager_anyOf_i0"></a>11.1. Property `DocumentManager Reference`

**Title:** DocumentManager Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.agent.doc_manager.document_manager.DocumentManager"`     |

| Property                                                       | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#document_manager_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#document_manager_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

#### <a name="document_manager_anyOf_i0_implementation"></a>11.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

### <a name="document_manager_anyOf_i1"></a>11.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

----------------------------------------------------------------------------------------------------------------------------
