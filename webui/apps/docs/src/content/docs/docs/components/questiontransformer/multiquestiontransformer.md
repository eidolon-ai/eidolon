---
title: MultiQuestionTransformer
description: "Description of MultiQuestionTransformer component"
---

| Property                                     | Pattern | Type    | Deprecated | Definition | Title/Description        |
| -------------------------------------------- | ------- | ------- | ---------- | ---------- | ------------------------ |
| - [implementation](#implementation )         | No      | const   | No         | -          | MultiQuestionTransformer |
| - [keep_original](#keep_original )           | No      | boolean | No         | -          | Keep Original            |
| - [number_to_generate](#number_to_generate ) | No      | integer | No         | -          | Number To Generate       |
| - [prompt](#prompt )                         | No      | string  | No         | -          | Prompt                   |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** MultiQuestionTransformer

Specific value: `"MultiQuestionTransformer"`

## <a name="keep_original"></a>2. Property `keep_original`

**Title:** Keep Original

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

**Description:** Whether to keep the original question in the output

## <a name="number_to_generate"></a>3. Property `number_to_generate`

**Title:** Number To Generate

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `3`       |

**Description:** The number of questions to generate

## <a name="prompt"></a>4. Property `prompt`

**Title:** Prompt

|              |                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| **Required** | No                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| **Default**  | `"You are an AI language model assistant. Your task is to generate {{number_to_generate}} different versions of the given user \n    question to retrieve relevant documents from a vector  database. By generating multiple perspectives on the user question, \n    your goal is to help the user overcome some of the limitations of distance-based similarity search. Provide these alternative \n    questions separated by newlines. Original question: {{question}}"` |

**Description:** The prompt to be used for the question transformer. This should be a template where the user question is the field {{question}}

----------------------------------------------------------------------------------------------------------------------------
