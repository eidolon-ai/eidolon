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
| + [host](#host )                     | No      | string              | No         | -                        | Host                                                      |
| - [client_options](#client_options ) | No      | object              | No         | In #/$defs/OllamaOptions | Additional arguments when calling ollama.AsyncClient.chat |

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

## <a name="host"></a>6. Property `host`

**Title:** Host

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Running Ollama location.
Defaults to envar OLLAMA_HOST with fallback to 127.0.0.1:11434 if that is not set.

## <a name="client_options"></a>7. Property `client_options`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |
| **Defined in**            | #/$defs/OllamaOptions                                                     |

**Description:** Additional arguments when calling ollama.AsyncClient.chat

**Description:** Additional arguments when calling ollama.AsyncClient.chat

| Property                                                  | Pattern | Type            | Deprecated | Definition | Title/Description |
| --------------------------------------------------------- | ------- | --------------- | ---------- | ---------- | ----------------- |
| + [numa](#client_options_numa )                           | No      | boolean         | No         | -          | Numa              |
| + [num_ctx](#client_options_num_ctx )                     | No      | integer         | No         | -          | Num Ctx           |
| + [num_batch](#client_options_num_batch )                 | No      | integer         | No         | -          | Num Batch         |
| + [num_gpu](#client_options_num_gpu )                     | No      | integer         | No         | -          | Num Gpu           |
| + [main_gpu](#client_options_main_gpu )                   | No      | integer         | No         | -          | Main Gpu          |
| + [low_vram](#client_options_low_vram )                   | No      | boolean         | No         | -          | Low Vram          |
| + [f16_kv](#client_options_f16_kv )                       | No      | boolean         | No         | -          | F16 Kv            |
| + [logits_all](#client_options_logits_all )               | No      | boolean         | No         | -          | Logits All        |
| + [vocab_only](#client_options_vocab_only )               | No      | boolean         | No         | -          | Vocab Only        |
| + [use_mmap](#client_options_use_mmap )                   | No      | boolean         | No         | -          | Use Mmap          |
| + [use_mlock](#client_options_use_mlock )                 | No      | boolean         | No         | -          | Use Mlock         |
| + [embedding_only](#client_options_embedding_only )       | No      | boolean         | No         | -          | Embedding Only    |
| + [num_thread](#client_options_num_thread )               | No      | integer         | No         | -          | Num Thread        |
| + [num_keep](#client_options_num_keep )                   | No      | integer         | No         | -          | Num Keep          |
| + [seed](#client_options_seed )                           | No      | integer         | No         | -          | Seed              |
| + [num_predict](#client_options_num_predict )             | No      | integer         | No         | -          | Num Predict       |
| + [top_k](#client_options_top_k )                         | No      | integer         | No         | -          | Top K             |
| + [top_p](#client_options_top_p )                         | No      | number          | No         | -          | Top P             |
| + [tfs_z](#client_options_tfs_z )                         | No      | number          | No         | -          | Tfs Z             |
| + [typical_p](#client_options_typical_p )                 | No      | number          | No         | -          | Typical P         |
| + [repeat_last_n](#client_options_repeat_last_n )         | No      | integer         | No         | -          | Repeat Last N     |
| + [temperature](#client_options_temperature )             | No      | number          | No         | -          | Temperature       |
| + [repeat_penalty](#client_options_repeat_penalty )       | No      | number          | No         | -          | Repeat Penalty    |
| + [presence_penalty](#client_options_presence_penalty )   | No      | number          | No         | -          | Presence Penalty  |
| + [frequency_penalty](#client_options_frequency_penalty ) | No      | number          | No         | -          | Frequency Penalty |
| + [mirostat](#client_options_mirostat )                   | No      | integer         | No         | -          | Mirostat          |
| + [mirostat_tau](#client_options_mirostat_tau )           | No      | number          | No         | -          | Mirostat Tau      |
| + [mirostat_eta](#client_options_mirostat_eta )           | No      | number          | No         | -          | Mirostat Eta      |
| + [penalize_newline](#client_options_penalize_newline )   | No      | boolean         | No         | -          | Penalize Newline  |
| + [stop](#client_options_stop )                           | No      | array of string | No         | -          | Stop              |

### <a name="client_options_numa"></a>7.1. Property `numa`

**Title:** Numa

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

### <a name="client_options_num_ctx"></a>7.2. Property `num_ctx`

**Title:** Num Ctx

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

### <a name="client_options_num_batch"></a>7.3. Property `num_batch`

**Title:** Num Batch

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

### <a name="client_options_num_gpu"></a>7.4. Property `num_gpu`

**Title:** Num Gpu

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

### <a name="client_options_main_gpu"></a>7.5. Property `main_gpu`

**Title:** Main Gpu

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

### <a name="client_options_low_vram"></a>7.6. Property `low_vram`

**Title:** Low Vram

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

### <a name="client_options_f16_kv"></a>7.7. Property `f16_kv`

**Title:** F16 Kv

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

### <a name="client_options_logits_all"></a>7.8. Property `logits_all`

**Title:** Logits All

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

### <a name="client_options_vocab_only"></a>7.9. Property `vocab_only`

**Title:** Vocab Only

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

### <a name="client_options_use_mmap"></a>7.10. Property `use_mmap`

**Title:** Use Mmap

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

### <a name="client_options_use_mlock"></a>7.11. Property `use_mlock`

**Title:** Use Mlock

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

### <a name="client_options_embedding_only"></a>7.12. Property `embedding_only`

**Title:** Embedding Only

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

### <a name="client_options_num_thread"></a>7.13. Property `num_thread`

**Title:** Num Thread

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

### <a name="client_options_num_keep"></a>7.14. Property `num_keep`

**Title:** Num Keep

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

### <a name="client_options_seed"></a>7.15. Property `seed`

**Title:** Seed

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

### <a name="client_options_num_predict"></a>7.16. Property `num_predict`

**Title:** Num Predict

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

### <a name="client_options_top_k"></a>7.17. Property `top_k`

**Title:** Top K

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

### <a name="client_options_top_p"></a>7.18. Property `top_p`

**Title:** Top P

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

### <a name="client_options_tfs_z"></a>7.19. Property `tfs_z`

**Title:** Tfs Z

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

### <a name="client_options_typical_p"></a>7.20. Property `typical_p`

**Title:** Typical P

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

### <a name="client_options_repeat_last_n"></a>7.21. Property `repeat_last_n`

**Title:** Repeat Last N

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

### <a name="client_options_temperature"></a>7.22. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

### <a name="client_options_repeat_penalty"></a>7.23. Property `repeat_penalty`

**Title:** Repeat Penalty

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

### <a name="client_options_presence_penalty"></a>7.24. Property `presence_penalty`

**Title:** Presence Penalty

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

### <a name="client_options_frequency_penalty"></a>7.25. Property `frequency_penalty`

**Title:** Frequency Penalty

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

### <a name="client_options_mirostat"></a>7.26. Property `mirostat`

**Title:** Mirostat

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

### <a name="client_options_mirostat_tau"></a>7.27. Property `mirostat_tau`

**Title:** Mirostat Tau

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

### <a name="client_options_mirostat_eta"></a>7.28. Property `mirostat_eta`

**Title:** Mirostat Eta

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

### <a name="client_options_penalize_newline"></a>7.29. Property `penalize_newline`

**Title:** Penalize Newline

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

### <a name="client_options_stop"></a>7.30. Property `stop`

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

| Each item of this array must be          | Description |
| ---------------------------------------- | ----------- |
| [stop items](#client_options_stop_items) | -           |

#### <a name="autogenerated_heading_1"></a>7.30.1. stop items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

----------------------------------------------------------------------------------------------------------------------------
