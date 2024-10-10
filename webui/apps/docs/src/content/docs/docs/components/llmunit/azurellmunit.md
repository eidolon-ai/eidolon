---
title: AzureLLMUnit
description: Description of the AzureLLMUnit component
---

| Property                                                 | Pattern | Type                | Deprecated | Definition            | Title/Description                                                                                                                                                                              |
| -------------------------------------------------------- | ------- | ------------------- | ---------- | --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| + [implementation](#implementation )                     | No      | const               | No         | -                     | Implementation                                                                                                                                                                                 |
| + [model](#model )                                       | No      | [Reference[LLMModel]](/docs/components/llmmodel/overview) | No         | -                     | The model to use for the LLM. Since Azure deployments use custom names, no default is provided. See https://www.eidolonai.com/docs/howto/swap_llm for more details. on defining custom models. |
| - [temperature](#temperature )                           | No      | number              | No         | -                     | Temperature                                                                                                                                                                                    |
| - [force_json](#force_json )                             | No      | boolean             | No         | -                     | Force Json                                                                                                                                                                                     |
| - [max_tokens](#max_tokens )                             | No      | integer             | No         | -                     | Max Tokens                                                                                                                                                                                     |
| - [supports_system_messages](#supports_system_messages ) | No      | boolean             | No         | -                     | Supports System Messages                                                                                                                                                                       |
| - [can_stream](#can_stream )                             | No      | boolean             | No         | -                     | Can Stream                                                                                                                                                                                     |
| + [azure_endpoint](#azure_endpoint )                     | No      | string              | No         | -                     | Azure Endpoint                                                                                                                                                                                 |
| - [azure_ad_token_provider](#azure_ad_token_provider )   | No      | object              | No         | In #/$defs/_Reference | -                                                                                                                                                                                              |
| - [token_provider_scopes](#token_provider_scopes )       | No      | array of string     | No         | -                     | Token Provider Scopes                                                                                                                                                                          |
| - [api_version](#api_version )                           | No      | string              | No         | -                     | Api Version                                                                                                                                                                                    |
| - [client_args](#client_args )                           | No      | object              | No         | -                     | Client Args                                                                                                                                                                                    |

## <a name="implementation"></a>1. Property `implementation`

**Title:** Implementation

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | Yes     |

Specific value: `"AzureLLMUnit"`

## <a name="model"></a>2. Property `model`

|              |                                                              |
| ------------ | ------------------------------------------------------------ |
| **Type**     | [`Reference[LLMModel]`](/docs/components/llmmodel/overview)                                        |
| **Required** | Yes                                                          |
| **Default**  | `{"implementation": "eidolon_ai_sdk.apu.llm_unit.LLMModel"}` |

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

## <a name="azure_endpoint"></a>8. Property `azure_endpoint`

**Title:** Azure Endpoint

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** The azure_endpoint for the Azure LLM API. ie, "https://eidolon-azure.openai.azure.com/"

## <a name="azure_ad_token_provider"></a>9. Property `azure_ad_token_provider`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | #/$defs/_Reference                                                        |

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

### <a name="autogenerated_heading_1"></a>10.1. token_provider_scopes items

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
