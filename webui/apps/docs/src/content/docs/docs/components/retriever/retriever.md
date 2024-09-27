---
title: Retriever
description: "Description of Retriever component"
---
# Schema Docs

- [1. Property `implementation`](#implementation)
- [2. Property `max_num_results`](#max_num_results)
- [3. Property `question_transformer`](#question_transformer)
  - [3.1. Property `implementation`](#question_transformer_implementation)
- [4. Property `document_retriever`](#document_retriever)
  - [4.1. Property `implementation`](#document_retriever_implementation)
- [5. Property `document_reranker`](#document_reranker)
  - [5.1. Property `implementation`](#document_reranker_implementation)
- [6. Property `result_summarizer`](#result_summarizer)
  - [6.1. Property `implementation`](#result_summarizer_implementation)

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

| Property                                         | Pattern | Type    | Deprecated | Definition | Title/Description |
| ------------------------------------------------ | ------- | ------- | ---------- | ---------- | ----------------- |
| - [implementation](#implementation )             | No      | const   | No         | -          | -                 |
| - [max_num_results](#max_num_results )           | No      | integer | No         | -          | Max Num Results   |
| - [question_transformer](#question_transformer ) | No      | object  | No         | -          | -                 |
| - [document_retriever](#document_retriever )     | No      | object  | No         | -          | -                 |
| - [document_reranker](#document_reranker )       | No      | object  | No         | -          | -                 |
| - [result_summarizer](#result_summarizer )       | No      | object  | No         | -          | -                 |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

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

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

| Property                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#question_transformer_implementation ) | No      | string | No         | -          | -                 |
| - [](#question_transformer_additionalProperties )         | No      | object | No         | -          | -                 |

### <a name="question_transformer_implementation"></a>3.1. Property `implementation`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

## <a name="document_retriever"></a>4. Property `document_retriever`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

| Property                                                | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#document_retriever_implementation ) | No      | string | No         | -          | -                 |
| - [](#document_retriever_additionalProperties )         | No      | object | No         | -          | -                 |

### <a name="document_retriever_implementation"></a>4.1. Property `implementation`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

## <a name="document_reranker"></a>5. Property `document_reranker`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

| Property                                               | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------ | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#document_reranker_implementation ) | No      | string | No         | -          | -                 |
| - [](#document_reranker_additionalProperties )         | No      | object | No         | -          | -                 |

### <a name="document_reranker_implementation"></a>5.1. Property `implementation`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

## <a name="result_summarizer"></a>6. Property `result_summarizer`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

| Property                                               | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------ | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#result_summarizer_implementation ) | No      | string | No         | -          | -                 |
| - [](#result_summarizer_additionalProperties )         | No      | object | No         | -          | -                 |

### <a name="result_summarizer_implementation"></a>6.1. Property `implementation`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

----------------------------------------------------------------------------------------------------------------------------
