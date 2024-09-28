---
title: OpenAIImageUnit
description: "Description of OpenAIImageUnit component"
---
# OpenAIImageUnit

- [1. [Optional] Property implementation](#implementation)
- [2. [Optional] Property image_to_text_prompt](#image_to_text_prompt)
- [3. [Optional] Property text_to_image_prompt](#text_to_image_prompt)
- [4. [Optional] Property connection_handler](#connection_handler)
- [5. [Optional] Property image_to_text_model](#image_to_text_model)
- [6. [Optional] Property text_to_image_model](#text_to_image_model)
- [7. [Optional] Property temperature](#temperature)
- [8. [Optional] Property image_to_text_system_prompt](#image_to_text_system_prompt)

**Title:** OpenAIImageUnit

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

Specific value: `"OpenAIImageUnit"`

</blockquote>
</details>

<details>
<summary>
<strong> <a name="image_to_text_prompt"></a>2. [Optional] Property image_to_text_prompt</strong>  

</summary>
<blockquote>

**Title:** Image To Text Prompt

|              |                                                     |
| ------------ | --------------------------------------------------- |
| **Type**     | `string`                                            |
| **Required** | No                                                  |
| **Default**  | `"Use the following prompt to describe the image:"` |

**Description:** The prompt to use for the conversion. The text should be very verbose and detailed.

</blockquote>
</details>

<details>
<summary>
<strong> <a name="text_to_image_prompt"></a>3. [Optional] Property text_to_image_prompt</strong>  

</summary>
<blockquote>

**Title:** Text To Image Prompt

|              |                                               |
| ------------ | --------------------------------------------- |
| **Type**     | `string`                                      |
| **Required** | No                                            |
| **Default**  | `"Use the provided text to create an image:"` |

**Description:** The prompt to use for the conversion. The text should be very verbose and detailed.

</blockquote>
</details>

<details>
<summary>
<strong> <a name="connection_handler"></a>4. [Optional] Property connection_handler</strong>  

</summary>
<blockquote>

|              |                                                 |
| ------------ | ----------------------------------------------- |
| **Type**     | [`Reference[OpenAIConnectionHandler]`](/docs/components/openaiconnectionhandler/overview)            |
| **Required** | No                                              |
| **Default**  | `{"implementation": "OpenAIConnectionHandler"}` |

</blockquote>
</details>

<details>
<summary>
<strong> <a name="image_to_text_model"></a>5. [Optional] Property image_to_text_model</strong>  

</summary>
<blockquote>

**Title:** Image To Text Model

|              |                 |
| ------------ | --------------- |
| **Type**     | `string`        |
| **Required** | No              |
| **Default**  | `"gpt-4-turbo"` |

**Description:** The model to use for the vision LLM.

</blockquote>
</details>

<details>
<summary>
<strong> <a name="text_to_image_model"></a>6. [Optional] Property text_to_image_model</strong>  

</summary>
<blockquote>

**Title:** Text To Image Model

|              |              |
| ------------ | ------------ |
| **Type**     | `string`     |
| **Required** | No           |
| **Default**  | `"dall-e-3"` |

**Description:** The model to use for the vision LLM.

</blockquote>
</details>

<details>
<summary>
<strong> <a name="temperature"></a>7. [Optional] Property temperature</strong>  

</summary>
<blockquote>

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

</blockquote>
</details>

<details>
<summary>
<strong> <a name="image_to_text_system_prompt"></a>8. [Optional] Property image_to_text_system_prompt</strong>  

</summary>
<blockquote>

**Title:** Image To Text System Prompt

|              |                                                                                                                                                                               |
| ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                                                                                      |
| **Required** | No                                                                                                                                                                            |
| **Default**  | `"You are an expert at answering questions about images. You are presented with an image and a question and must answer the question based on the information in the image."` |

**Description:** The system prompt to use for text to image.

</blockquote>
</details>

----------------------------------------------------------------------------------------------------------------------------
