---
title: AzureOpenAIConnectionHandler
description: "Description of AzureOpenAIConnectionHandler component"
---

**Description:** Automatically infers the values from environment variables for:
    - `api_key` from `AZURE_OPENAI_API_KEY` (IFF `api_key` AND 'azure_ad_token_provider' is not provided)
    - `organization` from `OPENAI_ORG_ID`
    - `azure_ad_token` from `AZURE_OPENAI_AD_TOKEN`
    - `api_version` from `OPENAI_API_VERSION`
    - `azure_endpoint` from `AZURE_OPENAI_ENDPOINT`

| Property                                               | Pattern | Type            | Deprecated | Definition           | Title/Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| ------------------------------------------------------ | ------- | --------------- | ---------- | -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| + [implementation](#implementation )                   | No      | const           | No         | -                    | AzureOpenAIConnectionHandler                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| - [azure_ad_token_provider](#azure_ad_token_provider ) | No      | object          | No         | In #/$defs/Reference | Used to create references to other classes. t is designed to be used with two type variables, \`B\` and \`D\` which are<br />the type bound and default type respectively. Neither are required, and if only one type is provided it is assumed<br />to be the bound. Bound is used as the default if no default is provided. default can also be a string which will be<br />looked up from the OS ReferenceResources.<br /><br />Examples:<br />    Reference(implementation=fqn(Foo)                           # Returns an instance of Foo<br />    Reference[FooBase](implementation=fqn(Foo)).instantiate()   # Returns an instance of Foo<br />    Reference[FooBase](implementation=fqn(Bar))                 # Raises ValueError<br />    Reference[FooBase, Foo]().instantiate()                     # Returns an instance of Foo<br />    Reference[FooBase]().instantiate()                          # Returns an instance of FooBase<br /><br />Attributes:<br />    _bound: This is a type variable \`B\` that represents the bound type of the reference. It defaults to \`object\`.<br />    _default: This is a type variable \`D\` that represents the default type of the reference. It defaults to \`None\`.<br />    implementation: This is a string that represents the fully qualified name of the class that the reference points to. It is optional and can be set to \`None\`.<br />    **extra: This is a dictionary that can hold any additional specifications for the reference. It is optional and can be set to \`None\`.<br /><br />Methods:<br />    instantiate: This method is used to create an instance of the class that the reference points to. |
| - [token_provider_scopes](#token_provider_scopes )     | No      | array of string | No         | -                    | Token Provider Scopes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| - [api_version](#api_version )                         | No      | string          | No         | -                    | Api Version                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| - [](#additionalProperties )                           | No      | object          | No         | -                    | -                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | Yes     |

**Description:** AzureOpenAIConnectionHandler

Specific value: `"AzureOpenAIConnectionHandler"`

## <a name="azure_ad_token_provider"></a>2. Property `azure_ad_token_provider`

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

| Property                                                     | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------ | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#azure_ad_token_provider_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#azure_ad_token_provider_additionalProperties )         | No      | object | No         | -          | -                 |

### <a name="azure_ad_token_provider_implementation"></a>2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

## <a name="token_provider_scopes"></a>3. Property `token_provider_scopes`

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

| Each item of this array must be                             | Description |
| ----------------------------------------------------------- | ----------- |
| [token_provider_scopes items](#token_provider_scopes_items) | -           |

### <a name="autogenerated_heading_2"></a>3.1. token_provider_scopes items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

## <a name="api_version"></a>4. Property `api_version`

**Title:** Api Version

|              |                |
| ------------ | -------------- |
| **Type**     | `string`       |
| **Required** | No             |
| **Default**  | `"2024-02-01"` |

----------------------------------------------------------------------------------------------------------------------------
