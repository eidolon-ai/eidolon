---
title: OpenAIGPT
description: Description of OpenAIGPT component
---

| Property                                     | Pattern | Type        | Deprecated | Definition                                       | Title/Description                              |
| -------------------------------------------- | ------- | ----------- | ---------- | ------------------------------------------------ | ---------------------------------------------- |
| - [implementation](#implementation )         | No      | const       | No         | -                                                | OpenAIGPT                                      |
| - [model](#model )                           | No      | object      | No         | In [LLMModel](/docs/components/llmmodel/overview)                | Overview of LLMModel components                |
| - [temperature](#temperature )               | No      | number      | No         | -                                                | Temperature                                    |
| - [force_json](#force_json )                 | No      | boolean     | No         | -                                                | Force Json                                     |
| - [max_tokens](#max_tokens )                 | No      | Combination | No         | -                                                | Max Tokens                                     |
| - [connection_handler](#connection_handler ) | No      | object      | No         | In [OpenAIConnectionHandler](/docs/components/openaiconnectionhandler/overview) | Overview of OpenAIConnectionHandler components |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OpenAIGPT

Specific value: `"OpenAIGPT"`

## <a name="model"></a>2. Property `model`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{"implementation": "LLMModel"}`                                          |
| **Defined in**            | [LLMModel](/docs/components/llmmodel/overview)                                            |

**Description:** Overview of LLMModel components

| Any of(Option)                                   |
| ------------------------------------------------ |
| [claude-3-haiku-20240307.json](#model_anyOf_i0)  |
| [claude-3-opus-20240229.json](#model_anyOf_i1)   |
| [claude-3-sonnet-20240229.json](#model_anyOf_i2) |
| [gpt-3.5-turbo.json](#model_anyOf_i3)            |
| [gpt-4-turbo.json](#model_anyOf_i4)              |
| [gpt-4o.json](#model_anyOf_i5)                   |
| [llama3-8b.json](#model_anyOf_i6)                |
| [mistral-large-latest.json](#model_anyOf_i7)     |
| [mistral-medium-latest.json](#model_anyOf_i8)    |
| [mistral-small-latest.json](#model_anyOf_i9)     |

### <a name="model_anyOf_i0"></a>2.1. Property `claude-3-haiku-20240307.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./claude-3-haiku-20240307.json                                       |

| Property                                                        | Pattern | Type    | Deprecated | Definition | Title/Description       |
| --------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | ----------------------- |
| - [implementation](#model_anyOf_i0_implementation )             | No      | const   | No         | -          | claude-3-haiku-20240307 |
| + [human_name](#model_anyOf_i0_human_name )                     | No      | string  | No         | -          | Human Name              |
| + [name](#model_anyOf_i0_name )                                 | No      | string  | No         | -          | Name                    |
| + [input_context_limit](#model_anyOf_i0_input_context_limit )   | No      | integer | No         | -          | Input Context Limit     |
| + [output_context_limit](#model_anyOf_i0_output_context_limit ) | No      | integer | No         | -          | Output Context Limit    |
| + [supports_tools](#model_anyOf_i0_supports_tools )             | No      | boolean | No         | -          | Supports Tools          |
| + [supports_image_input](#model_anyOf_i0_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input    |
| + [supports_audio_input](#model_anyOf_i0_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input    |

#### <a name="model_anyOf_i0_implementation"></a>2.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** claude-3-haiku-20240307

Specific value: `"claude-3-haiku-20240307"`

#### <a name="model_anyOf_i0_human_name"></a>2.1.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

#### <a name="model_anyOf_i0_name"></a>2.1.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

#### <a name="model_anyOf_i0_input_context_limit"></a>2.1.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

#### <a name="model_anyOf_i0_output_context_limit"></a>2.1.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

#### <a name="model_anyOf_i0_supports_tools"></a>2.1.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

#### <a name="model_anyOf_i0_supports_image_input"></a>2.1.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

#### <a name="model_anyOf_i0_supports_audio_input"></a>2.1.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

### <a name="model_anyOf_i1"></a>2.2. Property `claude-3-opus-20240229.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./claude-3-opus-20240229.json                                        |

| Property                                                        | Pattern | Type    | Deprecated | Definition | Title/Description      |
| --------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | ---------------------- |
| - [implementation](#model_anyOf_i1_implementation )             | No      | const   | No         | -          | claude-3-opus-20240229 |
| + [human_name](#model_anyOf_i1_human_name )                     | No      | string  | No         | -          | Human Name             |
| + [name](#model_anyOf_i1_name )                                 | No      | string  | No         | -          | Name                   |
| + [input_context_limit](#model_anyOf_i1_input_context_limit )   | No      | integer | No         | -          | Input Context Limit    |
| + [output_context_limit](#model_anyOf_i1_output_context_limit ) | No      | integer | No         | -          | Output Context Limit   |
| + [supports_tools](#model_anyOf_i1_supports_tools )             | No      | boolean | No         | -          | Supports Tools         |
| + [supports_image_input](#model_anyOf_i1_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input   |
| + [supports_audio_input](#model_anyOf_i1_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input   |

#### <a name="model_anyOf_i1_implementation"></a>2.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** claude-3-opus-20240229

Specific value: `"claude-3-opus-20240229"`

#### <a name="model_anyOf_i1_human_name"></a>2.2.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

#### <a name="model_anyOf_i1_name"></a>2.2.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

#### <a name="model_anyOf_i1_input_context_limit"></a>2.2.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

#### <a name="model_anyOf_i1_output_context_limit"></a>2.2.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

#### <a name="model_anyOf_i1_supports_tools"></a>2.2.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

#### <a name="model_anyOf_i1_supports_image_input"></a>2.2.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

#### <a name="model_anyOf_i1_supports_audio_input"></a>2.2.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

### <a name="model_anyOf_i2"></a>2.3. Property `claude-3-sonnet-20240229.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./claude-3-sonnet-20240229.json                                      |

| Property                                                        | Pattern | Type    | Deprecated | Definition | Title/Description        |
| --------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | ------------------------ |
| - [implementation](#model_anyOf_i2_implementation )             | No      | const   | No         | -          | claude-3-sonnet-20240229 |
| + [human_name](#model_anyOf_i2_human_name )                     | No      | string  | No         | -          | Human Name               |
| + [name](#model_anyOf_i2_name )                                 | No      | string  | No         | -          | Name                     |
| + [input_context_limit](#model_anyOf_i2_input_context_limit )   | No      | integer | No         | -          | Input Context Limit      |
| + [output_context_limit](#model_anyOf_i2_output_context_limit ) | No      | integer | No         | -          | Output Context Limit     |
| + [supports_tools](#model_anyOf_i2_supports_tools )             | No      | boolean | No         | -          | Supports Tools           |
| + [supports_image_input](#model_anyOf_i2_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input     |
| + [supports_audio_input](#model_anyOf_i2_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input     |

#### <a name="model_anyOf_i2_implementation"></a>2.3.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** claude-3-sonnet-20240229

Specific value: `"claude-3-sonnet-20240229"`

#### <a name="model_anyOf_i2_human_name"></a>2.3.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

#### <a name="model_anyOf_i2_name"></a>2.3.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

#### <a name="model_anyOf_i2_input_context_limit"></a>2.3.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

#### <a name="model_anyOf_i2_output_context_limit"></a>2.3.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

#### <a name="model_anyOf_i2_supports_tools"></a>2.3.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

#### <a name="model_anyOf_i2_supports_image_input"></a>2.3.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

#### <a name="model_anyOf_i2_supports_audio_input"></a>2.3.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

### <a name="model_anyOf_i3"></a>2.4. Property `gpt-3.5-turbo.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./gpt-3.5-turbo.json                                                 |

| Property                                                        | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#model_anyOf_i3_implementation )             | No      | const   | No         | -          | gpt-3.5-turbo        |
| + [human_name](#model_anyOf_i3_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#model_anyOf_i3_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#model_anyOf_i3_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#model_anyOf_i3_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#model_anyOf_i3_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#model_anyOf_i3_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#model_anyOf_i3_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

#### <a name="model_anyOf_i3_implementation"></a>2.4.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** gpt-3.5-turbo

Specific value: `"gpt-3.5-turbo"`

#### <a name="model_anyOf_i3_human_name"></a>2.4.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

#### <a name="model_anyOf_i3_name"></a>2.4.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

#### <a name="model_anyOf_i3_input_context_limit"></a>2.4.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

#### <a name="model_anyOf_i3_output_context_limit"></a>2.4.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

#### <a name="model_anyOf_i3_supports_tools"></a>2.4.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

#### <a name="model_anyOf_i3_supports_image_input"></a>2.4.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

#### <a name="model_anyOf_i3_supports_audio_input"></a>2.4.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

### <a name="model_anyOf_i4"></a>2.5. Property `gpt-4-turbo.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./gpt-4-turbo.json                                                   |

| Property                                                        | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#model_anyOf_i4_implementation )             | No      | const   | No         | -          | gpt-4-turbo          |
| + [human_name](#model_anyOf_i4_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#model_anyOf_i4_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#model_anyOf_i4_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#model_anyOf_i4_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#model_anyOf_i4_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#model_anyOf_i4_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#model_anyOf_i4_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

#### <a name="model_anyOf_i4_implementation"></a>2.5.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** gpt-4-turbo

Specific value: `"gpt-4-turbo"`

#### <a name="model_anyOf_i4_human_name"></a>2.5.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

#### <a name="model_anyOf_i4_name"></a>2.5.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

#### <a name="model_anyOf_i4_input_context_limit"></a>2.5.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

#### <a name="model_anyOf_i4_output_context_limit"></a>2.5.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

#### <a name="model_anyOf_i4_supports_tools"></a>2.5.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

#### <a name="model_anyOf_i4_supports_image_input"></a>2.5.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

#### <a name="model_anyOf_i4_supports_audio_input"></a>2.5.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

### <a name="model_anyOf_i5"></a>2.6. Property `gpt-4o.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./gpt-4o.json                                                        |

| Property                                                        | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#model_anyOf_i5_implementation )             | No      | const   | No         | -          | gpt-4o               |
| + [human_name](#model_anyOf_i5_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#model_anyOf_i5_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#model_anyOf_i5_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#model_anyOf_i5_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#model_anyOf_i5_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#model_anyOf_i5_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#model_anyOf_i5_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

#### <a name="model_anyOf_i5_implementation"></a>2.6.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** gpt-4o

Specific value: `"gpt-4o"`

#### <a name="model_anyOf_i5_human_name"></a>2.6.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

#### <a name="model_anyOf_i5_name"></a>2.6.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

#### <a name="model_anyOf_i5_input_context_limit"></a>2.6.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

#### <a name="model_anyOf_i5_output_context_limit"></a>2.6.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

#### <a name="model_anyOf_i5_supports_tools"></a>2.6.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

#### <a name="model_anyOf_i5_supports_image_input"></a>2.6.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

#### <a name="model_anyOf_i5_supports_audio_input"></a>2.6.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

### <a name="model_anyOf_i6"></a>2.7. Property `llama3-8b.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./llama3-8b.json                                                     |

| Property                                                        | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#model_anyOf_i6_implementation )             | No      | const   | No         | -          | llama3-8b            |
| + [human_name](#model_anyOf_i6_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#model_anyOf_i6_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#model_anyOf_i6_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#model_anyOf_i6_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#model_anyOf_i6_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#model_anyOf_i6_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#model_anyOf_i6_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

#### <a name="model_anyOf_i6_implementation"></a>2.7.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** llama3-8b

Specific value: `"llama3-8b"`

#### <a name="model_anyOf_i6_human_name"></a>2.7.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

#### <a name="model_anyOf_i6_name"></a>2.7.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

#### <a name="model_anyOf_i6_input_context_limit"></a>2.7.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

#### <a name="model_anyOf_i6_output_context_limit"></a>2.7.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

#### <a name="model_anyOf_i6_supports_tools"></a>2.7.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

#### <a name="model_anyOf_i6_supports_image_input"></a>2.7.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

#### <a name="model_anyOf_i6_supports_audio_input"></a>2.7.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

### <a name="model_anyOf_i7"></a>2.8. Property `mistral-large-latest.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./mistral-large-latest.json                                          |

| Property                                                        | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#model_anyOf_i7_implementation )             | No      | const   | No         | -          | mistral-large-latest |
| + [human_name](#model_anyOf_i7_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#model_anyOf_i7_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#model_anyOf_i7_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#model_anyOf_i7_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#model_anyOf_i7_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#model_anyOf_i7_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#model_anyOf_i7_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

#### <a name="model_anyOf_i7_implementation"></a>2.8.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** mistral-large-latest

Specific value: `"mistral-large-latest"`

#### <a name="model_anyOf_i7_human_name"></a>2.8.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

#### <a name="model_anyOf_i7_name"></a>2.8.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

#### <a name="model_anyOf_i7_input_context_limit"></a>2.8.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

#### <a name="model_anyOf_i7_output_context_limit"></a>2.8.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

#### <a name="model_anyOf_i7_supports_tools"></a>2.8.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

#### <a name="model_anyOf_i7_supports_image_input"></a>2.8.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

#### <a name="model_anyOf_i7_supports_audio_input"></a>2.8.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

### <a name="model_anyOf_i8"></a>2.9. Property `mistral-medium-latest.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./mistral-medium-latest.json                                         |

| Property                                                        | Pattern | Type    | Deprecated | Definition | Title/Description     |
| --------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | --------------------- |
| - [implementation](#model_anyOf_i8_implementation )             | No      | const   | No         | -          | mistral-medium-latest |
| + [human_name](#model_anyOf_i8_human_name )                     | No      | string  | No         | -          | Human Name            |
| + [name](#model_anyOf_i8_name )                                 | No      | string  | No         | -          | Name                  |
| + [input_context_limit](#model_anyOf_i8_input_context_limit )   | No      | integer | No         | -          | Input Context Limit   |
| + [output_context_limit](#model_anyOf_i8_output_context_limit ) | No      | integer | No         | -          | Output Context Limit  |
| + [supports_tools](#model_anyOf_i8_supports_tools )             | No      | boolean | No         | -          | Supports Tools        |
| + [supports_image_input](#model_anyOf_i8_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input  |
| + [supports_audio_input](#model_anyOf_i8_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input  |

#### <a name="model_anyOf_i8_implementation"></a>2.9.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** mistral-medium-latest

Specific value: `"mistral-medium-latest"`

#### <a name="model_anyOf_i8_human_name"></a>2.9.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

#### <a name="model_anyOf_i8_name"></a>2.9.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

#### <a name="model_anyOf_i8_input_context_limit"></a>2.9.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

#### <a name="model_anyOf_i8_output_context_limit"></a>2.9.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

#### <a name="model_anyOf_i8_supports_tools"></a>2.9.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

#### <a name="model_anyOf_i8_supports_image_input"></a>2.9.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

#### <a name="model_anyOf_i8_supports_audio_input"></a>2.9.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

### <a name="model_anyOf_i9"></a>2.10. Property `mistral-small-latest.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./mistral-small-latest.json                                          |

| Property                                                        | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#model_anyOf_i9_implementation )             | No      | const   | No         | -          | mistral-small-latest |
| + [human_name](#model_anyOf_i9_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#model_anyOf_i9_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#model_anyOf_i9_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#model_anyOf_i9_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#model_anyOf_i9_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#model_anyOf_i9_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#model_anyOf_i9_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

#### <a name="model_anyOf_i9_implementation"></a>2.10.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** mistral-small-latest

Specific value: `"mistral-small-latest"`

#### <a name="model_anyOf_i9_human_name"></a>2.10.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

#### <a name="model_anyOf_i9_name"></a>2.10.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

#### <a name="model_anyOf_i9_input_context_limit"></a>2.10.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

#### <a name="model_anyOf_i9_output_context_limit"></a>2.10.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

#### <a name="model_anyOf_i9_supports_tools"></a>2.10.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

#### <a name="model_anyOf_i9_supports_image_input"></a>2.10.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

#### <a name="model_anyOf_i9_supports_audio_input"></a>2.10.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

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

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                 |
| ------------------------------ |
| [item 0](#max_tokens_anyOf_i0) |
| [item 1](#max_tokens_anyOf_i1) |

### <a name="max_tokens_anyOf_i0"></a>5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

### <a name="max_tokens_anyOf_i1"></a>5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

## <a name="connection_handler"></a>6. Property `connection_handler`

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

### <a name="connection_handler_anyOf_i0"></a>6.1. Property `AzureOpenAIConnectionHandler.json`

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

#### <a name="connection_handler_anyOf_i0_implementation"></a>6.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AzureOpenAIConnectionHandler

Specific value: `"AzureOpenAIConnectionHandler"`

#### <a name="connection_handler_anyOf_i0_azure_ad_token_provider"></a>6.1.2. Property `azure_ad_token_provider`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

| Any of(Option)                                                             |
| -------------------------------------------------------------------------- |
| [Reference](#connection_handler_anyOf_i0_azure_ad_token_provider_anyOf_i0) |
| [item 1](#connection_handler_anyOf_i0_azure_ad_token_provider_anyOf_i1)    |

##### <a name="connection_handler_anyOf_i0_azure_ad_token_provider_anyOf_i0"></a>6.1.2.1. Property `Reference`

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

###### <a name="connection_handler_anyOf_i0_azure_ad_token_provider_anyOf_i0_implementation"></a>6.1.2.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="connection_handler_anyOf_i0_azure_ad_token_provider_anyOf_i1"></a>6.1.2.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="connection_handler_anyOf_i0_token_provider_scopes"></a>6.1.3. Property `token_provider_scopes`

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

##### <a name="autogenerated_heading_2"></a>6.1.3.1. token_provider_scopes items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

#### <a name="connection_handler_anyOf_i0_api_version"></a>6.1.4. Property `api_version`

**Title:** Api Version

|              |                |
| ------------ | -------------- |
| **Type**     | `string`       |
| **Required** | No             |
| **Default**  | `"2024-02-01"` |

----------------------------------------------------------------------------------------------------------------------------
