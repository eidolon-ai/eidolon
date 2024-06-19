---
title: OpenAIImageUnit
description: Description of OpenAIImageUnit component
---

| Property                                                       | Pattern | Type   | Deprecated | Definition                                       | Title/Description                              |
| -------------------------------------------------------------- | ------- | ------ | ---------- | ------------------------------------------------ | ---------------------------------------------- |
| - [implementation](#implementation )                           | No      | const  | No         | -                                                | OpenAIImageUnit                                |
| - [image_to_text_prompt](#image_to_text_prompt )               | No      | string | No         | -                                                | Image To Text Prompt                           |
| - [text_to_image_prompt](#text_to_image_prompt )               | No      | string | No         | -                                                | Text To Image Prompt                           |
| - [connection_handler](#connection_handler )                   | No      | object | No         | In [OpenAIConnectionHandler](/docs/components/openaiconnectionhandler/overview) | Overview of OpenAIConnectionHandler components |
| - [image_to_text_model](#image_to_text_model )                 | No      | string | No         | -                                                | Image To Text Model                            |
| - [text_to_image_model](#text_to_image_model )                 | No      | string | No         | -                                                | Text To Image Model                            |
| - [temperature](#temperature )                                 | No      | number | No         | -                                                | Temperature                                    |
| - [image_to_text_system_prompt](#image_to_text_system_prompt ) | No      | string | No         | -                                                | Image To Text System Prompt                    |

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

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"OpenAIConnectionHandler"`                                               |
| **Defined in**            | [OpenAIConnectionHandler](/docs/components/openaiconnectionhandler/overview)                             |

**Description:** Overview of OpenAIConnectionHandler components

| Property                                                                  | Pattern | Type            | Deprecated | Definition | Title/Description            |
| ------------------------------------------------------------------------- | ------- | --------------- | ---------- | ---------- | ---------------------------- |
| - [implementation](#connection_handler_implementation )                   | No      | const           | No         | -          | AzureOpenAIConnectionHandler |
| - [azure_ad_token_provider](#connection_handler_azure_ad_token_provider ) | No      | Combination     | No         | -          | -                            |
| - [token_provider_scopes](#connection_handler_token_provider_scopes )     | No      | array of string | No         | -          | Token Provider Scopes        |
| - [api_version](#connection_handler_api_version )                         | No      | string          | No         | -          | Api Version                  |
| - [](#connection_handler_additionalProperties )                           | No      | object          | No         | -          | -                            |

### <a name="connection_handler_implementation"></a>4.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AzureOpenAIConnectionHandler

Specific value: `"AzureOpenAIConnectionHandler"`

### <a name="connection_handler_azure_ad_token_provider"></a>4.2. Property `azure_ad_token_provider`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

| Any of(Option)                                                    |
| ----------------------------------------------------------------- |
| [Reference](#connection_handler_azure_ad_token_provider_anyOf_i0) |
| [item 1](#connection_handler_azure_ad_token_provider_anyOf_i1)    |

#### <a name="connection_handler_azure_ad_token_provider_anyOf_i0"></a>4.2.1. Property `Reference`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | #/$defs/Reference                                                         |

**Description:** Used to create references to other classes. t is designed to be used with two type variables, `B` and `D` which are
the type bound and default type respectively. Neither are required, and if only one type is provided it is assumed
to be the bound. Bound is used as the default if no default is provided. default can also be a string which will be
looked up from the OS ReferenceResources.

Examples:
    Reference(implementation=fqn(Foo)                           # Returns an instance of Foo
    Reference[FooBase](implementation=fqn(Foo)).instantiate()   # Returns an instance of Foo
    Reference[FooBase](implementation=fqn(Bar))                 # Raises ValueError
    Reference[FooBase, Foo]().instantiate()                     # Returns an instance of Foo
    Reference[FooBase]().instantiate()                          # Returns an instance of FooBase

Attributes:
    _bound: This is a type variable `B` that represents the bound type of the reference. It defaults to `object`.
    _default: This is a type variable `D` that represents the default type of the reference. It defaults to `None`.
    implementation: This is a string that represents the fully qualified name of the class that the reference points to. It is optional and can be set to `None`.
    **extra: This is a dictionary that can hold any additional specifications for the reference. It is optional and can be set to `None`.

Methods:
    instantiate: This method is used to create an instance of the class that the reference points to.

| Property                                                                                 | Pattern | Type   | Deprecated | Definition | Title/Description |
| ---------------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#connection_handler_azure_ad_token_provider_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#connection_handler_azure_ad_token_provider_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

##### <a name="connection_handler_azure_ad_token_provider_anyOf_i0_implementation"></a>4.2.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="connection_handler_azure_ad_token_provider_anyOf_i1"></a>4.2.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

### <a name="connection_handler_token_provider_scopes"></a>4.3. Property `token_provider_scopes`

**Title:** Token Provider Scopes

|              |                                                    |
| ------------ | -------------------------------------------------- |
| **Type**     | `array of string`                                  |
| **Required** | No                                                 |
| **Default**  | `["https://cognitiveservices.azure.com/.default"]` |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                                                | Description |
| ------------------------------------------------------------------------------ | ----------- |
| [token_provider_scopes items](#connection_handler_token_provider_scopes_items) | -           |

#### <a name="autogenerated_heading_2"></a>4.3.1. token_provider_scopes items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

### <a name="connection_handler_api_version"></a>4.4. Property `api_version`

**Title:** Api Version

|              |                |
| ------------ | -------------- |
| **Type**     | `string`       |
| **Required** | No             |
| **Default**  | `"2024-02-01"` |

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
