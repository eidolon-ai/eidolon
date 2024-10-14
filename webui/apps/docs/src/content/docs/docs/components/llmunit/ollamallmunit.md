---
title: OllamaLLMUnit
description: Description of the OllamaLLMUnit component
---

| Property                             | Pattern | Type                | Deprecated | Definition | Title/Description |
| ------------------------------------ | ------- | ------------------- | ---------- | ---------- | ----------------- |
| + [implementation](#implementation ) | No      | const               | No         | -          | Implementation    |
| - [model](#model )                   | No      | [Reference[LLMModel]](/docs/components/llmmodel/overview) | No         | -          | -                 |
| - [temperature](#temperature )       | No      | number              | No         | -          | Temperature       |
| - [force_json](#force_json )         | No      | boolean             | No         | -          | Force Json        |
| - [max_tokens](#max_tokens )         | No      | integer             | No         | -          | Max Tokens        |
| + [ollama_host](#ollama_host )       | No      | string              | No         | -          | Ollama Host       |
| - [client_options](#client_options ) | No      | object              | No         | -          | Client Options    |

## <a name="implementation"></a>1. Property `implementation`

**Title:** Implementation

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | Yes     |

Specific value: `"OllamaLLMUnit"`

## <a name="model"></a>2. Property `model`

|              |                                                              |
| ------------ | ------------------------------------------------------------ |
| **Type**     | [`Reference[LLMModel]`](/docs/components/llmmodel/overview)                                        |
| **Required** | No                                                           |
| **Default**  | `{"implementation": "eidolon_ai_sdk.apu.llm_unit.LLMModel"}` |

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

## <a name="ollama_host"></a>6. Property `ollama_host`

**Title:** Ollama Host

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Running Ollama location.
Defaults to envar OLLAMA_HOST with fallback to 127.0.0.1:11434 if that is not set.

## <a name="client_options"></a>7. Property `client_options`

**Title:** Client Options

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

**Description:** Extra key-value arguments when instantiating ollama.AsyncClient.

----------------------------------------------------------------------------------------------------------------------------
