---
title: OpenAIImageUnit
description: "Description of OpenAIImageUnit component"
---

| Property                                                       | Pattern | Type                               | Deprecated | Definition                                       | Title/Description                              |
| -------------------------------------------------------------- | ------- | ---------------------------------- | ---------- | ------------------------------------------------ | ---------------------------------------------- |
| - [implementation](#implementation )                           | No      | const                              | No         | -                                                | OpenAIImageUnit                                |
| - [image_to_text_prompt](#image_to_text_prompt )               | No      | string                             | No         | -                                                | Image To Text Prompt                           |
| - [text_to_image_prompt](#text_to_image_prompt )               | No      | string                             | No         | -                                                | Text To Image Prompt                           |
| - [connection_handler](#connection_handler )                   | No      | Reference[OpenAIConnectionHandler] | No         | In [OpenAIConnectionHandler](/docs/components/openaiconnectionhandler/overview) | Overview of OpenAIConnectionHandler components |
| - [image_to_text_model](#image_to_text_model )                 | No      | string                             | No         | -                                                | Image To Text Model                            |
| - [text_to_image_model](#text_to_image_model )                 | No      | string                             | No         | -                                                | Text To Image Model                            |
| - [temperature](#temperature )                                 | No      | number                             | No         | -                                                | Temperature                                    |
| - [image_to_text_system_prompt](#image_to_text_system_prompt ) | No      | string                             | No         | -                                                | Image To Text System Prompt                    |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OpenAIImageUnit

Specific value: `"OpenAIImageUnit"`

## <a name="image_to_text_prompt"></a>2. Property `image_to_text_prompt`

**Title:** Image To Text Prompt

|              |                                                     |
| ------------ | --------------------------------------------------- |
| **Type**     | `string`                                            |
| **Required** | No                                                  |
| **Default**  | `"Use the following prompt to describe the image:"` |

**Description:** The prompt to use for the conversion. The text should be very verbose and detailed.

## <a name="text_to_image_prompt"></a>3. Property `text_to_image_prompt`

**Title:** Text To Image Prompt

|              |                                               |
| ------------ | --------------------------------------------- |
| **Type**     | `string`                                      |
| **Required** | No                                            |
| **Default**  | `"Use the provided text to create an image:"` |

**Description:** The prompt to use for the conversion. The text should be very verbose and detailed.

## <a name="connection_handler"></a>4. Property `connection_handler`

|                |                                                 |
| -------------- | ----------------------------------------------- |
| **Type**       | `Reference[OpenAIConnectionHandler]`            |
| **Required**   | No                                              |
| **Default**    | `{"implementation": "OpenAIConnectionHandler"}` |
| **Defined in** | [OpenAIConnectionHandler](/docs/components/openaiconnectionhandler/overview)   |

**Description:** Overview of OpenAIConnectionHandler components

## <a name="image_to_text_model"></a>5. Property `image_to_text_model`

**Title:** Image To Text Model

|              |                 |
| ------------ | --------------- |
| **Type**     | `string`        |
| **Required** | No              |
| **Default**  | `"gpt-4-turbo"` |

**Description:** The model to use for the vision LLM.

## <a name="text_to_image_model"></a>6. Property `text_to_image_model`

**Title:** Text To Image Model

|              |              |
| ------------ | ------------ |
| **Type**     | `string`     |
| **Required** | No           |
| **Default**  | `"dall-e-3"` |

**Description:** The model to use for the vision LLM.

## <a name="temperature"></a>7. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

## <a name="image_to_text_system_prompt"></a>8. Property `image_to_text_system_prompt`

**Title:** Image To Text System Prompt

|              |                                                                                                                                                                               |
| ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                                                                                      |
| **Required** | No                                                                                                                                                                            |
| **Default**  | `"You are an expert at answering questions about images. You are presented with an image and a question and must answer the question based on the information in the image."` |

**Description:** The system prompt to use for text to image.

----------------------------------------------------------------------------------------------------------------------------
