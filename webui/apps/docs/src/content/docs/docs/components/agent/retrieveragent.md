---
title: RetrieverAgentSpec
description: "Description of RetrieverAgentSpec component"
---

**Description:** A RetrieverAgent is an agent that will take a query, rewrite it for better similarity vector search, and then perform the vector search on the document store.
The agent will dynamically load and embed files, so it is not performant for loading large bodies of files, but performs very well for small to medium-sized document stores (hundreds to thousands of documents) which are updating frequently.

| Property                                         | Pattern | Type        | Deprecated | Definition | Title/Description                           |
| ------------------------------------------------ | ------- | ----------- | ---------- | ---------- | ------------------------------------------- |
| - [max_num_results](#max_num_results )           | No      | integer     | No         | -          | Max Num Results                             |
| - [question_transformer](#question_transformer ) | No      | object      | No         | -          | -                                           |
| - [document_retriever](#document_retriever )     | No      | object      | No         | -          | -                                           |
| - [document_reranker](#document_reranker )       | No      | object      | No         | -          | -                                           |
| - [result_summarizer](#result_summarizer )       | No      | object      | No         | -          | -                                           |
| + [name](#name )                                 | No      | string      | No         | -          | Name                                        |
| + [description](#description )                   | No      | string      | No         | -          | Description                                 |
| - [loader_root_location](#loader_root_location ) | No      | string      | No         | -          | Loader Root Location                        |
| - [loader_pattern](#loader_pattern )             | No      | Combination | No         | -          | Loader Pattern                              |
| - [document_manager](#document_manager )         | No      | object      | No         | -          | -                                           |
| - [apu](#apu )                                   | No      | object      | No         | -          | The APU to use for question transformation. |
| - [implementation](#implementation )             | No      | const       | No         | -          | -                                           |

## <a name="max_num_results"></a>1. Property `max_num_results`

**Title:** Max Num Results

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `10`      |

**Description:** The maximum number of results to consider.

## <a name="question_transformer"></a>2. Property `question_transformer`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

| Property                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#question_transformer_implementation ) | No      | string | No         | -          | -                 |
| - [](#question_transformer_additionalProperties )         | No      | object | No         | -          | -                 |

### <a name="question_transformer_implementation"></a>2.1. Property `implementation`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

## <a name="document_retriever"></a>3. Property `document_retriever`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

| Property                                                | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#document_retriever_implementation ) | No      | string | No         | -          | -                 |
| - [](#document_retriever_additionalProperties )         | No      | object | No         | -          | -                 |

### <a name="document_retriever_implementation"></a>3.1. Property `implementation`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

## <a name="document_reranker"></a>4. Property `document_reranker`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

| Property                                               | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------ | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#document_reranker_implementation ) | No      | string | No         | -          | -                 |
| - [](#document_reranker_additionalProperties )         | No      | object | No         | -          | -                 |

### <a name="document_reranker_implementation"></a>4.1. Property `implementation`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

## <a name="result_summarizer"></a>5. Property `result_summarizer`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

| Property                                               | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------ | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#result_summarizer_implementation ) | No      | string | No         | -          | -                 |
| - [](#result_summarizer_additionalProperties )         | No      | object | No         | -          | -                 |

### <a name="result_summarizer_implementation"></a>5.1. Property `implementation`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

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

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

**Description:** A URL specifying the root location of the loader.

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
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Property                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| ----------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#document_manager_implementation ) | No      | string | No         | -          | -                 |
| - [](#document_manager_additionalProperties )         | No      | object | No         | -          | -                 |

### <a name="document_manager_implementation"></a>10.1. Property `implementation`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

## <a name="apu"></a>11. Property `apu`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

**Description:** The APU to use for question transformation.

| Property                                 | Pattern | Type   | Deprecated | Definition | Title/Description |
| ---------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_implementation ) | No      | string | No         | -          | -                 |
| - [](#apu_additionalProperties )         | No      | object | No         | -          | -                 |

### <a name="apu_implementation"></a>11.1. Property `implementation`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

## <a name="implementation"></a>12. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

Specific value: `"RetrieverAgent"`

----------------------------------------------------------------------------------------------------------------------------
