---
title: MultiQuestionTransformer
description: "Description of MultiQuestionTransformer component"
---
# MultiQuestionTransformer

- [1. [Optional] Property implementation](#implementation)
- [2. [Optional] Property keep_original](#keep_original)
- [3. [Optional] Property number_to_generate](#number_to_generate)
- [4. [Optional] Property prompt](#prompt)

**Title:** MultiQuestionTransformer

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

Specific value: `"MultiQuestionTransformer"`

</blockquote>
</details>

<details>
<summary>
<strong> <a name="keep_original"></a>2. [Optional] Property keep_original</strong>  

</summary>
<blockquote>

**Title:** Keep Original

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

**Description:** Whether to keep the original question in the output

</blockquote>
</details>

<details>
<summary>
<strong> <a name="number_to_generate"></a>3. [Optional] Property number_to_generate</strong>  

</summary>
<blockquote>

**Title:** Number To Generate

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `3`       |

**Description:** The number of questions to generate

</blockquote>
</details>

<details>
<summary>
<strong> <a name="prompt"></a>4. [Optional] Property prompt</strong>  

</summary>
<blockquote>

**Title:** Prompt

|              |                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| **Required** | No                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| **Default**  | `"You are an AI language model assistant. Your task is to generate {{number_to_generate}} different versions of the given user \n    question to retrieve relevant documents from a vector  database. By generating multiple perspectives on the user question, \n    your goal is to help the user overcome some of the limitations of distance-based similarity search. Provide these alternative \n    questions separated by newlines. Original question: {{question}}"` |

**Description:** The prompt to be used for the question transformer. This should be a template where the user question is the field {{question}}

</blockquote>
</details>

----------------------------------------------------------------------------------------------------------------------------
