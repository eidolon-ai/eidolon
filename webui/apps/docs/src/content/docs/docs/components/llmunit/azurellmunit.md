---
title: AzureLLMUnit
description: "Description of AzureLLMUnit component"
---

**Description:** Azure LLM Unit. Requires model to be defined. See https://www.eidolonai.com/docs/howto/swap_llm for more details.

Authentication is handled oot with one of two mechanisms:
* Static token defined with AZURE_OPENAI_API_KEY
* Token provider defined by AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, and AZURE_TENANT_ID

To use an alternative authentication mechanism, provide a custom token provider.

| Property                                                 | Pattern | Type                | Deprecated | Definition                        | Title/Description               |
| -------------------------------------------------------- | ------- | ------------------- | ---------- | --------------------------------- | ------------------------------- |
| - [implementation](#implementation )                     | No      | const               | No         | -                                 | AzureLLMUnit                    |
| + [model](#model )                                       | No      | Reference[LLMModel] | No         | In [LLMModel](/docs/components/llmmodel/overview) | Overview of LLMModel components |
| - [temperature](#temperature )                           | No      | number              | No         | -                                 | Temperature                     |
| - [force_json](#force_json )                             | No      | boolean             | No         | -                                 | Force Json                      |
| - [max_tokens](#max_tokens )                             | No      | integer             | No         | -                                 | Max Tokens                      |
| - [supports_system_messages](#supports_system_messages ) | No      | boolean             | No         | -                                 | Supports System Messages        |
| - [can_stream](#can_stream )                             | No      | boolean             | No         | -                                 | Can Stream                      |
| + [azure_endpoint](#azure_endpoint )                     | No      | string              | No         | -                                 | Azure Endpoint                  |
| - [azure_ad_token_provider](#azure_ad_token_provider )   | No      | object              | No         | -                                 | object Reference                |
| - [token_provider_scopes](#token_provider_scopes )       | No      | array of string     | No         | -                                 | Token Provider Scopes           |
| - [api_version](#api_version )                           | No      | string              | No         | -                                 | Api Version                     |
| - [client_args](#client_args )                           | No      | object              | No         | -                                 | Client Args                     |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AzureLLMUnit

Specific value: `"AzureLLMUnit"`

## <a name="model"></a>2. Property `model`

|                |                                |
| -------------- | ------------------------------ |
| **Type**       | `Reference[LLMModel]`          |
| **Required**   | Yes                            |
| **Defined in** | [LLMModel](/docs/components/llmmodel/overview) |

**Description:** Overview of LLMModel components

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

## <a name="azure_endpoint"></a>8. Property `azure_endpoint`

**Title:** Azure Endpoint

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** The azure_endpoint for the Azure LLM API. ie, "https://eidolon-azure.openai.azure.com/"

## <a name="azure_ad_token_provider"></a>9. Property `azure_ad_token_provider`

**Title:** object Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

| Property                                                     | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------ | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#azure_ad_token_provider_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#azure_ad_token_provider_additionalProperties )         | No      | object | No         | -          | -                 |

### <a name="azure_ad_token_provider_implementation"></a>9.1. Property `implementation`

**Title:** Implementation

|              |                     |
| ------------ | ------------------- |
| **Type**     | `string`            |
| **Required** | No                  |
| **Default**  | `"builtins.object"` |

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
