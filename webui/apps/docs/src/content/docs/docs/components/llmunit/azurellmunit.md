---
title: AzureLLMUnit
description: "Description of AzureLLMUnit component"
---

| Property                                                 | Pattern | Type                | Deprecated | Definition           | Title/Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| -------------------------------------------------------- | ------- | ------------------- | ---------- | -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| - [implementation](#implementation )                     | No      | const               | No         | -                    | AzureLLMUnit                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| + [model](#model )                                       | No      | Reference[LLMModel] | No         | In                   | The model to use for the LLM. Since Azure deployments use custom names, no default is provided. See https://www.eidolonai.com/docs/howto/swap_llm for more details. on defining custom models.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| - [temperature](#temperature )                           | No      | number              | No         | -                    | Temperature                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| - [force_json](#force_json )                             | No      | boolean             | No         | -                    | Force Json                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| - [max_tokens](#max_tokens )                             | No      | integer             | No         | -                    | Max Tokens                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| - [supports_system_messages](#supports_system_messages ) | No      | boolean             | No         | -                    | Supports System Messages                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| - [can_stream](#can_stream )                             | No      | boolean             | No         | -                    | Can Stream                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| + [base_url](#base_url )                                 | No      | string              | No         | -                    | Base Url                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| - [azure_ad_token_provider](#azure_ad_token_provider )   | No      | object              | No         | In #/$defs/Reference | Used to create references to other classes. t is designed to be used with two type variables, \`B\` and \`D\` which are<br />the type bound and default type respectively. Neither are required, and if only one type is provided it is assumed<br />to be the bound. Bound is used as the default if no default is provided. default can also be a string which will be<br />looked up from the OS ReferenceResources.<br /><br />Examples:<br />    Reference(implementation=fqn(Foo)                           # Returns an instance of Foo<br />    Reference[FooBase](implementation=fqn(Foo)).instantiate()   # Returns an instance of Foo<br />    Reference[FooBase](implementation=fqn(Bar))                 # Raises ValueError<br />    Reference[FooBase, Foo]().instantiate()                     # Returns an instance of Foo<br />    Reference[FooBase]().instantiate()                          # Returns an instance of FooBase<br /><br />Attributes:<br />    _bound: This is a type variable \`B\` that represents the bound type of the reference. It defaults to \`object\`.<br />    _default: This is a type variable \`D\` that represents the default type of the reference. It defaults to \`None\`.<br />    implementation: This is a string that represents the fully qualified name of the class that the reference points to. It is optional and can be set to \`None\`.<br />    **extra: This is a dictionary that can hold any additional specifications for the reference. It is optional and can be set to \`None\`.<br /><br />Methods:<br />    instantiate: This method is used to create an instance of the class that the reference points to. |
| - [token_provider_scopes](#token_provider_scopes )       | No      | array of string     | No         | -                    | Token Provider Scopes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| - [api_version](#api_version )                           | No      | string              | No         | -                    | Api Version                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| - [client_args](#client_args )                           | No      | object              | No         | -                    | Client Args                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AzureLLMUnit

Specific value: `"AzureLLMUnit"`

## <a name="model"></a>2. Property `model`

|                |                       |
| -------------- | --------------------- |
| **Type**       | `Reference[LLMModel]` |
| **Required**   | Yes                   |
| **Defined in** |                       |

**Description:** The model to use for the LLM. Since Azure deployments use custom names, no default is provided. See https://www.eidolonai.com/docs/howto/swap_llm for more details. on defining custom models.

## <a name="temperature"></a>3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

## <a name="force_json"></a>4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

## <a name="max_tokens"></a>5. Property `max_tokens`

**Title:** Max Tokens

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `null`    |

## <a name="supports_system_messages"></a>6. Property `supports_system_messages`

**Title:** Supports System Messages

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

## <a name="can_stream"></a>7. Property `can_stream`

**Title:** Can Stream

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

## <a name="base_url"></a>8. Property `base_url`

**Title:** Base Url

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** The base URL for the Azure LLM API. ie, "https://eidolon-azure.openai.azure.com/openai"

## <a name="azure_ad_token_provider"></a>9. Property `azure_ad_token_provider`

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

### <a name="azure_ad_token_provider_implementation"></a>9.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

## <a name="token_provider_scopes"></a>10. Property `token_provider_scopes`

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

### <a name="autogenerated_heading_2"></a>10.1. token_provider_scopes items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

## <a name="api_version"></a>11. Property `api_version`

**Title:** Api Version

|              |                |
| ------------ | -------------- |
| **Type**     | `string`       |
| **Required** | No             |
| **Default**  | `"2024-02-01"` |

## <a name="client_args"></a>12. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

----------------------------------------------------------------------------------------------------------------------------
