---
title: OpenAIEmbedding
description: Description of OpenAIEmbedding component
---

| Property                                     | Pattern | Type   | Deprecated | Definition                                       | Title/Description                              |
| -------------------------------------------- | ------- | ------ | ---------- | ------------------------------------------------ | ---------------------------------------------- |
| - [implementation](#implementation )         | No      | const  | No         | -                                                | OpenAIEmbedding                                |
| - [model](#model )                           | No      | string | No         | -                                                | Model                                          |
| - [connection_handler](#connection_handler ) | No      | object | No         | In [OpenAIConnectionHandler](/docs/components/openaiconnectionhandler/overview) | Overview of OpenAIConnectionHandler components |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OpenAIEmbedding

Specific value: `"OpenAIEmbedding"`

## <a name="model"></a>2. Property `model`

**Title:** Model

|              |                            |
| ------------ | -------------------------- |
| **Type**     | `string`                   |
| **Required** | No                         |
| **Default**  | `"text-embedding-ada-002"` |

**Description:** The name of the model to use.

## <a name="connection_handler"></a>3. Property `connection_handler`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{"implementation": "OpenAIConnectionHandler"}`                           |
| **Defined in**            | [OpenAIConnectionHandler](/docs/components/openaiconnectionhandler/overview)                             |

**Description:** Overview of OpenAIConnectionHandler components

| Any of(Option)                                                    |
| ----------------------------------------------------------------- |
| [AzureOpenAIConnectionHandler.json](#connection_handler_anyOf_i0) |

### <a name="connection_handler_anyOf_i0"></a>3.1. Property `AzureOpenAIConnectionHandler.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./AzureOpenAIConnectionHandler.json                                  |

**Description:** Automatically infers the values from environment variables for:
    - `api_key` from `AZURE_OPENAI_API_KEY` (IFF `api_key` AND 'azure_ad_token_provider' is not provided)
    - `organization` from `OPENAI_ORG_ID`
    - `azure_ad_token` from `AZURE_OPENAI_AD_TOKEN`
    - `api_version` from `OPENAI_API_VERSION`
    - `azure_endpoint` from `AZURE_OPENAI_ENDPOINT`

| Property                                                                           | Pattern | Type            | Deprecated | Definition | Title/Description            |
| ---------------------------------------------------------------------------------- | ------- | --------------- | ---------- | ---------- | ---------------------------- |
| - [implementation](#connection_handler_anyOf_i0_implementation )                   | No      | const           | No         | -          | AzureOpenAIConnectionHandler |
| - [azure_ad_token_provider](#connection_handler_anyOf_i0_azure_ad_token_provider ) | No      | Combination     | No         | -          | -                            |
| - [token_provider_scopes](#connection_handler_anyOf_i0_token_provider_scopes )     | No      | array of string | No         | -          | Token Provider Scopes        |
| - [api_version](#connection_handler_anyOf_i0_api_version )                         | No      | string          | No         | -          | Api Version                  |
| - [](#connection_handler_anyOf_i0_additionalProperties )                           | No      | object          | No         | -          | -                            |

#### <a name="connection_handler_anyOf_i0_implementation"></a>3.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AzureOpenAIConnectionHandler

Specific value: `"AzureOpenAIConnectionHandler"`

#### <a name="connection_handler_anyOf_i0_azure_ad_token_provider"></a>3.1.2. Property `azure_ad_token_provider`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

| Any of(Option)                                                             |
| -------------------------------------------------------------------------- |
| [Reference](#connection_handler_anyOf_i0_azure_ad_token_provider_anyOf_i0) |
| [item 1](#connection_handler_anyOf_i0_azure_ad_token_provider_anyOf_i1)    |

##### <a name="connection_handler_anyOf_i0_azure_ad_token_provider_anyOf_i0"></a>3.1.2.1. Property `Reference`

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

| Property                                                                                          | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#connection_handler_anyOf_i0_azure_ad_token_provider_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#connection_handler_anyOf_i0_azure_ad_token_provider_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="connection_handler_anyOf_i0_azure_ad_token_provider_anyOf_i0_implementation"></a>3.1.2.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="connection_handler_anyOf_i0_azure_ad_token_provider_anyOf_i1"></a>3.1.2.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="connection_handler_anyOf_i0_token_provider_scopes"></a>3.1.3. Property `token_provider_scopes`

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

| Each item of this array must be                                                         | Description |
| --------------------------------------------------------------------------------------- | ----------- |
| [token_provider_scopes items](#connection_handler_anyOf_i0_token_provider_scopes_items) | -           |

##### <a name="autogenerated_heading_2"></a>3.1.3.1. token_provider_scopes items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

#### <a name="connection_handler_anyOf_i0_api_version"></a>3.1.4. Property `api_version`

**Title:** Api Version

|              |                |
| ------------ | -------------- |
| **Type**     | `string`       |
| **Required** | No             |
| **Default**  | `"2024-02-01"` |

----------------------------------------------------------------------------------------------------------------------------
