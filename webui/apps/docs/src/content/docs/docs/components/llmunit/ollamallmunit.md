---
title: OllamaLLMUnit
description: Description of the OllamaLLMUnit component
---

| Property                             | Pattern | Type                | Deprecated | Definition               | Title/Description                                         |
| ------------------------------------ | ------- | ------------------- | ---------- | ------------------------ | --------------------------------------------------------- |
| + [implementation](#implementation ) | No      | const               | No         | -                        | Implementation                                            |
| - [model](#model )                   | No      | [Reference[LLMModel]](/docs/components/llmmodel/overview) | No         | -                        | -                                                         |
| - [temperature](#temperature )       | No      | number              | No         | -                        | Temperature                                               |
| - [force_json](#force_json )         | No      | boolean             | No         | -                        | Force Json                                                |
| - [max_tokens](#max_tokens )         | No      | integer             | No         | -                        | Max Tokens                                                |
| + [ollama_host](#ollama_host )       | No      | string              | No         | -                        | Ollama Host                                               |
| - [client_options](#client_options ) | No      | object              | No         | -                        | Client Options                                            |
| - [chat_options](#chat_options )     | No      | object              | No         | In #/$defs/OllamaOptions | Additional arguments when calling ollama.AsyncClient.chat |

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

## <a name="chat_options"></a>8. Property `chat_options`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |
| **Defined in**            | #/$defs/OllamaOptions                                                     |

**Description:** Additional arguments when calling ollama.AsyncClient.chat

**Description:** Additional arguments when calling ollama.AsyncClient.chat

| Property                                                | Pattern | Type            | Deprecated | Definition | Title/Description |
| ------------------------------------------------------- | ------- | --------------- | ---------- | ---------- | ----------------- |
| + [numa](#chat_options_numa )                           | No      | boolean         | No         | -          | Numa              |
| + [num_ctx](#chat_options_num_ctx )                     | No      | integer         | No         | -          | Num Ctx           |
| + [num_batch](#chat_options_num_batch )                 | No      | integer         | No         | -          | Num Batch         |
| + [num_gpu](#chat_options_num_gpu )                     | No      | integer         | No         | -          | Num Gpu           |
| + [main_gpu](#chat_options_main_gpu )                   | No      | integer         | No         | -          | Main Gpu          |
| + [low_vram](#chat_options_low_vram )                   | No      | boolean         | No         | -          | Low Vram          |
| + [f16_kv](#chat_options_f16_kv )                       | No      | boolean         | No         | -          | F16 Kv            |
| + [logits_all](#chat_options_logits_all )               | No      | boolean         | No         | -          | Logits All        |
| + [vocab_only](#chat_options_vocab_only )               | No      | boolean         | No         | -          | Vocab Only        |
| + [use_mmap](#chat_options_use_mmap )                   | No      | boolean         | No         | -          | Use Mmap          |
| + [use_mlock](#chat_options_use_mlock )                 | No      | boolean         | No         | -          | Use Mlock         |
| + [embedding_only](#chat_options_embedding_only )       | No      | boolean         | No         | -          | Embedding Only    |
| + [num_thread](#chat_options_num_thread )               | No      | integer         | No         | -          | Num Thread        |
| + [num_keep](#chat_options_num_keep )                   | No      | integer         | No         | -          | Num Keep          |
| + [seed](#chat_options_seed )                           | No      | integer         | No         | -          | Seed              |
| + [num_predict](#chat_options_num_predict )             | No      | integer         | No         | -          | Num Predict       |
| + [top_k](#chat_options_top_k )                         | No      | integer         | No         | -          | Top K             |
| + [top_p](#chat_options_top_p )                         | No      | number          | No         | -          | Top P             |
| + [tfs_z](#chat_options_tfs_z )                         | No      | number          | No         | -          | Tfs Z             |
| + [typical_p](#chat_options_typical_p )                 | No      | number          | No         | -          | Typical P         |
| + [repeat_last_n](#chat_options_repeat_last_n )         | No      | integer         | No         | -          | Repeat Last N     |
| + [temperature](#chat_options_temperature )             | No      | number          | No         | -          | Temperature       |
| + [repeat_penalty](#chat_options_repeat_penalty )       | No      | number          | No         | -          | Repeat Penalty    |
| + [presence_penalty](#chat_options_presence_penalty )   | No      | number          | No         | -          | Presence Penalty  |
| + [frequency_penalty](#chat_options_frequency_penalty ) | No      | number          | No         | -          | Frequency Penalty |
| + [mirostat](#chat_options_mirostat )                   | No      | integer         | No         | -          | Mirostat          |
| + [mirostat_tau](#chat_options_mirostat_tau )           | No      | number          | No         | -          | Mirostat Tau      |
| + [mirostat_eta](#chat_options_mirostat_eta )           | No      | number          | No         | -          | Mirostat Eta      |
| + [penalize_newline](#chat_options_penalize_newline )   | No      | boolean         | No         | -          | Penalize Newline  |
| + [stop](#chat_options_stop )                           | No      | array of string | No         | -          | Stop              |

### <a name="chat_options_numa"></a>8.1. Property `numa`

**Title:** Numa

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

### <a name="chat_options_num_ctx"></a>8.2. Property `num_ctx`

**Title:** Num Ctx

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

### <a name="chat_options_num_batch"></a>8.3. Property `num_batch`

**Title:** Num Batch

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

### <a name="chat_options_num_gpu"></a>8.4. Property `num_gpu`

**Title:** Num Gpu

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

### <a name="chat_options_main_gpu"></a>8.5. Property `main_gpu`

**Title:** Main Gpu

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

### <a name="chat_options_low_vram"></a>8.6. Property `low_vram`

**Title:** Low Vram

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

### <a name="chat_options_f16_kv"></a>8.7. Property `f16_kv`

**Title:** F16 Kv

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

### <a name="chat_options_logits_all"></a>8.8. Property `logits_all`

**Title:** Logits All

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

### <a name="chat_options_vocab_only"></a>8.9. Property `vocab_only`

**Title:** Vocab Only

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

### <a name="chat_options_use_mmap"></a>8.10. Property `use_mmap`

**Title:** Use Mmap

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

### <a name="chat_options_use_mlock"></a>8.11. Property `use_mlock`

**Title:** Use Mlock

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

### <a name="chat_options_embedding_only"></a>8.12. Property `embedding_only`

**Title:** Embedding Only

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

### <a name="chat_options_num_thread"></a>8.13. Property `num_thread`

**Title:** Num Thread

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

### <a name="chat_options_num_keep"></a>8.14. Property `num_keep`

**Title:** Num Keep

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

### <a name="chat_options_seed"></a>8.15. Property `seed`

**Title:** Seed

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

### <a name="chat_options_num_predict"></a>8.16. Property `num_predict`

**Title:** Num Predict

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

### <a name="chat_options_top_k"></a>8.17. Property `top_k`

**Title:** Top K

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

### <a name="chat_options_top_p"></a>8.18. Property `top_p`

**Title:** Top P

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

### <a name="chat_options_tfs_z"></a>8.19. Property `tfs_z`

**Title:** Tfs Z

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

### <a name="chat_options_typical_p"></a>8.20. Property `typical_p`

**Title:** Typical P

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

### <a name="chat_options_repeat_last_n"></a>8.21. Property `repeat_last_n`

**Title:** Repeat Last N

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

### <a name="chat_options_temperature"></a>8.22. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

### <a name="chat_options_repeat_penalty"></a>8.23. Property `repeat_penalty`

**Title:** Repeat Penalty

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

### <a name="chat_options_presence_penalty"></a>8.24. Property `presence_penalty`

**Title:** Presence Penalty

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

### <a name="chat_options_frequency_penalty"></a>8.25. Property `frequency_penalty`

**Title:** Frequency Penalty

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

### <a name="chat_options_mirostat"></a>8.26. Property `mirostat`

**Title:** Mirostat

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

### <a name="chat_options_mirostat_tau"></a>8.27. Property `mirostat_tau`

**Title:** Mirostat Tau

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

### <a name="chat_options_mirostat_eta"></a>8.28. Property `mirostat_eta`

**Title:** Mirostat Eta

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

### <a name="chat_options_penalize_newline"></a>8.29. Property `penalize_newline`

**Title:** Penalize Newline

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

### <a name="chat_options_stop"></a>8.30. Property `stop`

**Title:** Stop

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of string` |
| **Required** | Yes               |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be        | Description |
| -------------------------------------- | ----------- |
| [stop items](#chat_options_stop_items) | -           |

#### <a name="autogenerated_heading_1"></a>8.30.1. stop items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

----------------------------------------------------------------------------------------------------------------------------
