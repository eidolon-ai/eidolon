---
title: ToolCallLLMWrapper
description: Description of ToolCallLLMWrapper component
---

| Property                                       | Pattern | Type        | Deprecated | Definition                       | Title/Description              |
| ---------------------------------------------- | ------- | ----------- | ---------- | -------------------------------- | ------------------------------ |
| - [implementation](#implementation )           | No      | const       | No         | -                                | ToolCallLLMWrapper             |
| - [tool_message_prompt](#tool_message_prompt ) | No      | string      | No         | -                                | Tool Message Prompt            |
| - [llm_unit](#llm_unit )                       | No      | object      | No         | In [LLMUnit](/docs/components/llmunit/overview) | Overview of LLMUnit components |
| - [model](#model )                             | No      | Combination | No         | -                                | -                              |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ToolCallLLMWrapper

Specific value: `"ToolCallLLMWrapper"`

## <a name="tool_message_prompt"></a>2. Property `tool_message_prompt`

**Title:** Tool Message Prompt

|              |                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Required** | No                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Default**  | `"You must follow these instructions:\nYou can select zero or more of the above tools based on the user query\nIf there are multiple tools required, make sure a list of tools are returned in a JSON array.\nIf there is no tool that match the user request or you have already answered the question, you will respond with empty json array for the tools.\nYou can also add any additional notes or explanations in the notes field."` |

## <a name="llm_unit"></a>3. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"OpenAIGPT"`                                                             |
| **Defined in**            | [LLMUnit](/docs/components/llmunit/overview)                                             |

**Description:** Overview of LLMUnit components

| One of(Option)                                |
| --------------------------------------------- |
| [AnthropicLLMUnit.json](#llm_unit_oneOf_i0)   |
| [MistralGPT.json](#llm_unit_oneOf_i1)         |
| [OllamaLLMUnit.json](#llm_unit_oneOf_i2)      |
| [OpenAIGPT.json](#llm_unit_oneOf_i3)          |
| [ToolCallLLMWrapper.json](#llm_unit_oneOf_i4) |

### <a name="llm_unit_oneOf_i0"></a>3.1. Property `AnthropicLLMUnit.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./AnthropicLLMUnit.json                                              |

| Property                                               | Pattern | Type        | Deprecated | Definition                        | Title/Description               |
| ------------------------------------------------------ | ------- | ----------- | ---------- | --------------------------------- | ------------------------------- |
| - [implementation](#llm_unit_oneOf_i0_implementation ) | No      | const       | No         | -                                 | AnthropicLLMUnit                |
| - [model](#llm_unit_oneOf_i0_model )                   | No      | object      | No         | In [LLMModel](/docs/components/llmmodel/overview) | Overview of LLMModel components |
| - [temperature](#llm_unit_oneOf_i0_temperature )       | No      | number      | No         | -                                 | Temperature                     |
| - [max_tokens](#llm_unit_oneOf_i0_max_tokens )         | No      | Combination | No         | -                                 | Max Tokens                      |
| - [client_args](#llm_unit_oneOf_i0_client_args )       | No      | object      | No         | -                                 | Client Args                     |

#### <a name="llm_unit_oneOf_i0_implementation"></a>3.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AnthropicLLMUnit

Specific value: `"AnthropicLLMUnit"`

#### <a name="llm_unit_oneOf_i0_model"></a>3.1.2. Property `model`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMModel"`                                                              |
| **Defined in**            | [LLMModel](/docs/components/llmmodel/overview)                                            |

**Description:** Overview of LLMModel components

| One of(Option)                                                     |
| ------------------------------------------------------------------ |
| [claude-3-haiku-20240307.json](#llm_unit_oneOf_i0_model_oneOf_i0)  |
| [claude-3-opus-20240229.json](#llm_unit_oneOf_i0_model_oneOf_i1)   |
| [claude-3-sonnet-20240229.json](#llm_unit_oneOf_i0_model_oneOf_i2) |
| [gpt-3.5-turbo.json](#llm_unit_oneOf_i0_model_oneOf_i3)            |
| [gpt-4-turbo.json](#llm_unit_oneOf_i0_model_oneOf_i4)              |
| [gpt-4o.json](#llm_unit_oneOf_i0_model_oneOf_i5)                   |
| [llama3-8b.json](#llm_unit_oneOf_i0_model_oneOf_i6)                |
| [mistral-large-latest.json](#llm_unit_oneOf_i0_model_oneOf_i7)     |
| [mistral-medium-latest.json](#llm_unit_oneOf_i0_model_oneOf_i8)    |
| [mistral-small-latest.json](#llm_unit_oneOf_i0_model_oneOf_i9)     |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i0"></a>3.1.2.1. Property `claude-3-haiku-20240307.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./claude-3-haiku-20240307.json                                       |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description       |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | ----------------------- |
| - [implementation](#llm_unit_oneOf_i0_model_oneOf_i0_implementation )             | No      | const   | No         | -          | claude-3-haiku-20240307 |
| + [human_name](#llm_unit_oneOf_i0_model_oneOf_i0_human_name )                     | No      | string  | No         | -          | Human Name              |
| + [name](#llm_unit_oneOf_i0_model_oneOf_i0_name )                                 | No      | string  | No         | -          | Name                    |
| + [input_context_limit](#llm_unit_oneOf_i0_model_oneOf_i0_input_context_limit )   | No      | integer | No         | -          | Input Context Limit     |
| + [output_context_limit](#llm_unit_oneOf_i0_model_oneOf_i0_output_context_limit ) | No      | integer | No         | -          | Output Context Limit    |
| + [supports_tools](#llm_unit_oneOf_i0_model_oneOf_i0_supports_tools )             | No      | boolean | No         | -          | Supports Tools          |
| + [supports_image_input](#llm_unit_oneOf_i0_model_oneOf_i0_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input    |
| + [supports_audio_input](#llm_unit_oneOf_i0_model_oneOf_i0_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input    |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i0_implementation"></a>3.1.2.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** claude-3-haiku-20240307

Specific value: `"claude-3-haiku-20240307"`

###### <a name="llm_unit_oneOf_i0_model_oneOf_i0_human_name"></a>3.1.2.1.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i0_name"></a>3.1.2.1.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i0_input_context_limit"></a>3.1.2.1.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i0_output_context_limit"></a>3.1.2.1.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i0_supports_tools"></a>3.1.2.1.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i0_supports_image_input"></a>3.1.2.1.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i0_supports_audio_input"></a>3.1.2.1.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i1"></a>3.1.2.2. Property `claude-3-opus-20240229.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./claude-3-opus-20240229.json                                        |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description      |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | ---------------------- |
| - [implementation](#llm_unit_oneOf_i0_model_oneOf_i1_implementation )             | No      | const   | No         | -          | claude-3-opus-20240229 |
| + [human_name](#llm_unit_oneOf_i0_model_oneOf_i1_human_name )                     | No      | string  | No         | -          | Human Name             |
| + [name](#llm_unit_oneOf_i0_model_oneOf_i1_name )                                 | No      | string  | No         | -          | Name                   |
| + [input_context_limit](#llm_unit_oneOf_i0_model_oneOf_i1_input_context_limit )   | No      | integer | No         | -          | Input Context Limit    |
| + [output_context_limit](#llm_unit_oneOf_i0_model_oneOf_i1_output_context_limit ) | No      | integer | No         | -          | Output Context Limit   |
| + [supports_tools](#llm_unit_oneOf_i0_model_oneOf_i1_supports_tools )             | No      | boolean | No         | -          | Supports Tools         |
| + [supports_image_input](#llm_unit_oneOf_i0_model_oneOf_i1_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input   |
| + [supports_audio_input](#llm_unit_oneOf_i0_model_oneOf_i1_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input   |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i1_implementation"></a>3.1.2.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** claude-3-opus-20240229

Specific value: `"claude-3-opus-20240229"`

###### <a name="llm_unit_oneOf_i0_model_oneOf_i1_human_name"></a>3.1.2.2.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i1_name"></a>3.1.2.2.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i1_input_context_limit"></a>3.1.2.2.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i1_output_context_limit"></a>3.1.2.2.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i1_supports_tools"></a>3.1.2.2.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i1_supports_image_input"></a>3.1.2.2.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i1_supports_audio_input"></a>3.1.2.2.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i2"></a>3.1.2.3. Property `claude-3-sonnet-20240229.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./claude-3-sonnet-20240229.json                                      |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description        |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | ------------------------ |
| - [implementation](#llm_unit_oneOf_i0_model_oneOf_i2_implementation )             | No      | const   | No         | -          | claude-3-sonnet-20240229 |
| + [human_name](#llm_unit_oneOf_i0_model_oneOf_i2_human_name )                     | No      | string  | No         | -          | Human Name               |
| + [name](#llm_unit_oneOf_i0_model_oneOf_i2_name )                                 | No      | string  | No         | -          | Name                     |
| + [input_context_limit](#llm_unit_oneOf_i0_model_oneOf_i2_input_context_limit )   | No      | integer | No         | -          | Input Context Limit      |
| + [output_context_limit](#llm_unit_oneOf_i0_model_oneOf_i2_output_context_limit ) | No      | integer | No         | -          | Output Context Limit     |
| + [supports_tools](#llm_unit_oneOf_i0_model_oneOf_i2_supports_tools )             | No      | boolean | No         | -          | Supports Tools           |
| + [supports_image_input](#llm_unit_oneOf_i0_model_oneOf_i2_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input     |
| + [supports_audio_input](#llm_unit_oneOf_i0_model_oneOf_i2_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input     |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i2_implementation"></a>3.1.2.3.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** claude-3-sonnet-20240229

Specific value: `"claude-3-sonnet-20240229"`

###### <a name="llm_unit_oneOf_i0_model_oneOf_i2_human_name"></a>3.1.2.3.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i2_name"></a>3.1.2.3.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i2_input_context_limit"></a>3.1.2.3.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i2_output_context_limit"></a>3.1.2.3.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i2_supports_tools"></a>3.1.2.3.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i2_supports_image_input"></a>3.1.2.3.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i2_supports_audio_input"></a>3.1.2.3.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i3"></a>3.1.2.4. Property `gpt-3.5-turbo.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./gpt-3.5-turbo.json                                                 |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_oneOf_i0_model_oneOf_i3_implementation )             | No      | const   | No         | -          | gpt-3.5-turbo        |
| + [human_name](#llm_unit_oneOf_i0_model_oneOf_i3_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_oneOf_i0_model_oneOf_i3_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_oneOf_i0_model_oneOf_i3_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_oneOf_i0_model_oneOf_i3_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_oneOf_i0_model_oneOf_i3_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_oneOf_i0_model_oneOf_i3_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_oneOf_i0_model_oneOf_i3_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i3_implementation"></a>3.1.2.4.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** gpt-3.5-turbo

Specific value: `"gpt-3.5-turbo"`

###### <a name="llm_unit_oneOf_i0_model_oneOf_i3_human_name"></a>3.1.2.4.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i3_name"></a>3.1.2.4.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i3_input_context_limit"></a>3.1.2.4.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i3_output_context_limit"></a>3.1.2.4.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i3_supports_tools"></a>3.1.2.4.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i3_supports_image_input"></a>3.1.2.4.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i3_supports_audio_input"></a>3.1.2.4.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i4"></a>3.1.2.5. Property `gpt-4-turbo.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./gpt-4-turbo.json                                                   |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_oneOf_i0_model_oneOf_i4_implementation )             | No      | const   | No         | -          | gpt-4-turbo          |
| + [human_name](#llm_unit_oneOf_i0_model_oneOf_i4_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_oneOf_i0_model_oneOf_i4_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_oneOf_i0_model_oneOf_i4_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_oneOf_i0_model_oneOf_i4_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_oneOf_i0_model_oneOf_i4_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_oneOf_i0_model_oneOf_i4_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_oneOf_i0_model_oneOf_i4_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i4_implementation"></a>3.1.2.5.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** gpt-4-turbo

Specific value: `"gpt-4-turbo"`

###### <a name="llm_unit_oneOf_i0_model_oneOf_i4_human_name"></a>3.1.2.5.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i4_name"></a>3.1.2.5.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i4_input_context_limit"></a>3.1.2.5.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i4_output_context_limit"></a>3.1.2.5.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i4_supports_tools"></a>3.1.2.5.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i4_supports_image_input"></a>3.1.2.5.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i4_supports_audio_input"></a>3.1.2.5.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i5"></a>3.1.2.6. Property `gpt-4o.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./gpt-4o.json                                                        |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_oneOf_i0_model_oneOf_i5_implementation )             | No      | const   | No         | -          | gpt-4o               |
| + [human_name](#llm_unit_oneOf_i0_model_oneOf_i5_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_oneOf_i0_model_oneOf_i5_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_oneOf_i0_model_oneOf_i5_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_oneOf_i0_model_oneOf_i5_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_oneOf_i0_model_oneOf_i5_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_oneOf_i0_model_oneOf_i5_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_oneOf_i0_model_oneOf_i5_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i5_implementation"></a>3.1.2.6.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** gpt-4o

Specific value: `"gpt-4o"`

###### <a name="llm_unit_oneOf_i0_model_oneOf_i5_human_name"></a>3.1.2.6.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i5_name"></a>3.1.2.6.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i5_input_context_limit"></a>3.1.2.6.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i5_output_context_limit"></a>3.1.2.6.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i5_supports_tools"></a>3.1.2.6.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i5_supports_image_input"></a>3.1.2.6.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i5_supports_audio_input"></a>3.1.2.6.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i6"></a>3.1.2.7. Property `llama3-8b.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./llama3-8b.json                                                     |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_oneOf_i0_model_oneOf_i6_implementation )             | No      | const   | No         | -          | llama3-8b            |
| + [human_name](#llm_unit_oneOf_i0_model_oneOf_i6_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_oneOf_i0_model_oneOf_i6_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_oneOf_i0_model_oneOf_i6_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_oneOf_i0_model_oneOf_i6_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_oneOf_i0_model_oneOf_i6_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_oneOf_i0_model_oneOf_i6_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_oneOf_i0_model_oneOf_i6_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i6_implementation"></a>3.1.2.7.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** llama3-8b

Specific value: `"llama3-8b"`

###### <a name="llm_unit_oneOf_i0_model_oneOf_i6_human_name"></a>3.1.2.7.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i6_name"></a>3.1.2.7.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i6_input_context_limit"></a>3.1.2.7.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i6_output_context_limit"></a>3.1.2.7.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i6_supports_tools"></a>3.1.2.7.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i6_supports_image_input"></a>3.1.2.7.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i6_supports_audio_input"></a>3.1.2.7.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i7"></a>3.1.2.8. Property `mistral-large-latest.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./mistral-large-latest.json                                          |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_oneOf_i0_model_oneOf_i7_implementation )             | No      | const   | No         | -          | mistral-large-latest |
| + [human_name](#llm_unit_oneOf_i0_model_oneOf_i7_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_oneOf_i0_model_oneOf_i7_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_oneOf_i0_model_oneOf_i7_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_oneOf_i0_model_oneOf_i7_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_oneOf_i0_model_oneOf_i7_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_oneOf_i0_model_oneOf_i7_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_oneOf_i0_model_oneOf_i7_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i7_implementation"></a>3.1.2.8.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** mistral-large-latest

Specific value: `"mistral-large-latest"`

###### <a name="llm_unit_oneOf_i0_model_oneOf_i7_human_name"></a>3.1.2.8.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i7_name"></a>3.1.2.8.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i7_input_context_limit"></a>3.1.2.8.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i7_output_context_limit"></a>3.1.2.8.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i7_supports_tools"></a>3.1.2.8.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i7_supports_image_input"></a>3.1.2.8.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i7_supports_audio_input"></a>3.1.2.8.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i8"></a>3.1.2.9. Property `mistral-medium-latest.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./mistral-medium-latest.json                                         |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description     |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | --------------------- |
| - [implementation](#llm_unit_oneOf_i0_model_oneOf_i8_implementation )             | No      | const   | No         | -          | mistral-medium-latest |
| + [human_name](#llm_unit_oneOf_i0_model_oneOf_i8_human_name )                     | No      | string  | No         | -          | Human Name            |
| + [name](#llm_unit_oneOf_i0_model_oneOf_i8_name )                                 | No      | string  | No         | -          | Name                  |
| + [input_context_limit](#llm_unit_oneOf_i0_model_oneOf_i8_input_context_limit )   | No      | integer | No         | -          | Input Context Limit   |
| + [output_context_limit](#llm_unit_oneOf_i0_model_oneOf_i8_output_context_limit ) | No      | integer | No         | -          | Output Context Limit  |
| + [supports_tools](#llm_unit_oneOf_i0_model_oneOf_i8_supports_tools )             | No      | boolean | No         | -          | Supports Tools        |
| + [supports_image_input](#llm_unit_oneOf_i0_model_oneOf_i8_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input  |
| + [supports_audio_input](#llm_unit_oneOf_i0_model_oneOf_i8_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input  |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i8_implementation"></a>3.1.2.9.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** mistral-medium-latest

Specific value: `"mistral-medium-latest"`

###### <a name="llm_unit_oneOf_i0_model_oneOf_i8_human_name"></a>3.1.2.9.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i8_name"></a>3.1.2.9.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i8_input_context_limit"></a>3.1.2.9.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i8_output_context_limit"></a>3.1.2.9.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i8_supports_tools"></a>3.1.2.9.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i8_supports_image_input"></a>3.1.2.9.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i8_supports_audio_input"></a>3.1.2.9.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i9"></a>3.1.2.10. Property `mistral-small-latest.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./mistral-small-latest.json                                          |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_oneOf_i0_model_oneOf_i9_implementation )             | No      | const   | No         | -          | mistral-small-latest |
| + [human_name](#llm_unit_oneOf_i0_model_oneOf_i9_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_oneOf_i0_model_oneOf_i9_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_oneOf_i0_model_oneOf_i9_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_oneOf_i0_model_oneOf_i9_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_oneOf_i0_model_oneOf_i9_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_oneOf_i0_model_oneOf_i9_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_oneOf_i0_model_oneOf_i9_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i9_implementation"></a>3.1.2.10.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** mistral-small-latest

Specific value: `"mistral-small-latest"`

###### <a name="llm_unit_oneOf_i0_model_oneOf_i9_human_name"></a>3.1.2.10.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i9_name"></a>3.1.2.10.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i9_input_context_limit"></a>3.1.2.10.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i9_output_context_limit"></a>3.1.2.10.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i9_supports_tools"></a>3.1.2.10.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i9_supports_image_input"></a>3.1.2.10.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i9_supports_audio_input"></a>3.1.2.10.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

#### <a name="llm_unit_oneOf_i0_temperature"></a>3.1.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

#### <a name="llm_unit_oneOf_i0_max_tokens"></a>3.1.4. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                   |
| ------------------------------------------------ |
| [item 0](#llm_unit_oneOf_i0_max_tokens_anyOf_i0) |
| [item 1](#llm_unit_oneOf_i0_max_tokens_anyOf_i1) |

##### <a name="llm_unit_oneOf_i0_max_tokens_anyOf_i0"></a>3.1.4.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

##### <a name="llm_unit_oneOf_i0_max_tokens_anyOf_i1"></a>3.1.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="llm_unit_oneOf_i0_client_args"></a>3.1.5. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

### <a name="llm_unit_oneOf_i1"></a>3.2. Property `MistralGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./MistralGPT.json                                                    |

| Property                                               | Pattern | Type        | Deprecated | Definition                        | Title/Description               |
| ------------------------------------------------------ | ------- | ----------- | ---------- | --------------------------------- | ------------------------------- |
| - [implementation](#llm_unit_oneOf_i1_implementation ) | No      | const       | No         | -                                 | MistralGPT                      |
| - [model](#llm_unit_oneOf_i1_model )                   | No      | object      | No         | In [LLMModel](/docs/components/llmmodel/overview) | Overview of LLMModel components |
| - [temperature](#llm_unit_oneOf_i1_temperature )       | No      | number      | No         | -                                 | Temperature                     |
| - [force_json](#llm_unit_oneOf_i1_force_json )         | No      | boolean     | No         | -                                 | Force Json                      |
| - [max_tokens](#llm_unit_oneOf_i1_max_tokens )         | No      | Combination | No         | -                                 | Max Tokens                      |
| - [client_args](#llm_unit_oneOf_i1_client_args )       | No      | object      | No         | -                                 | Client Args                     |

#### <a name="llm_unit_oneOf_i1_implementation"></a>3.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** MistralGPT

Specific value: `"MistralGPT"`

#### <a name="llm_unit_oneOf_i1_model"></a>3.2.2. Property `model`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMModel"`                                                              |
| **Defined in**            | [LLMModel](/docs/components/llmmodel/overview)                                            |

**Description:** Overview of LLMModel components

| One of(Option)                                                     |
| ------------------------------------------------------------------ |
| [claude-3-haiku-20240307.json](#llm_unit_oneOf_i0_model_oneOf_i0)  |
| [claude-3-opus-20240229.json](#llm_unit_oneOf_i0_model_oneOf_i1)   |
| [claude-3-sonnet-20240229.json](#llm_unit_oneOf_i0_model_oneOf_i2) |
| [gpt-3.5-turbo.json](#llm_unit_oneOf_i0_model_oneOf_i3)            |
| [gpt-4-turbo.json](#llm_unit_oneOf_i0_model_oneOf_i4)              |
| [gpt-4o.json](#llm_unit_oneOf_i0_model_oneOf_i5)                   |
| [llama3-8b.json](#llm_unit_oneOf_i0_model_oneOf_i6)                |
| [mistral-large-latest.json](#llm_unit_oneOf_i0_model_oneOf_i7)     |
| [mistral-medium-latest.json](#llm_unit_oneOf_i0_model_oneOf_i8)    |
| [mistral-small-latest.json](#llm_unit_oneOf_i0_model_oneOf_i9)     |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i0"></a>3.2.2.1. Property `claude-3-haiku-20240307.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./claude-3-haiku-20240307.json                                       |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description       |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | ----------------------- |
| - [implementation](#llm_unit_oneOf_i0_model_oneOf_i0_implementation )             | No      | const   | No         | -          | claude-3-haiku-20240307 |
| + [human_name](#llm_unit_oneOf_i0_model_oneOf_i0_human_name )                     | No      | string  | No         | -          | Human Name              |
| + [name](#llm_unit_oneOf_i0_model_oneOf_i0_name )                                 | No      | string  | No         | -          | Name                    |
| + [input_context_limit](#llm_unit_oneOf_i0_model_oneOf_i0_input_context_limit )   | No      | integer | No         | -          | Input Context Limit     |
| + [output_context_limit](#llm_unit_oneOf_i0_model_oneOf_i0_output_context_limit ) | No      | integer | No         | -          | Output Context Limit    |
| + [supports_tools](#llm_unit_oneOf_i0_model_oneOf_i0_supports_tools )             | No      | boolean | No         | -          | Supports Tools          |
| + [supports_image_input](#llm_unit_oneOf_i0_model_oneOf_i0_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input    |
| + [supports_audio_input](#llm_unit_oneOf_i0_model_oneOf_i0_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input    |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i0_implementation"></a>3.2.2.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** claude-3-haiku-20240307

Specific value: `"claude-3-haiku-20240307"`

###### <a name="llm_unit_oneOf_i0_model_oneOf_i0_human_name"></a>3.2.2.1.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i0_name"></a>3.2.2.1.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i0_input_context_limit"></a>3.2.2.1.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i0_output_context_limit"></a>3.2.2.1.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i0_supports_tools"></a>3.2.2.1.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i0_supports_image_input"></a>3.2.2.1.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i0_supports_audio_input"></a>3.2.2.1.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i1"></a>3.2.2.2. Property `claude-3-opus-20240229.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./claude-3-opus-20240229.json                                        |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description      |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | ---------------------- |
| - [implementation](#llm_unit_oneOf_i0_model_oneOf_i1_implementation )             | No      | const   | No         | -          | claude-3-opus-20240229 |
| + [human_name](#llm_unit_oneOf_i0_model_oneOf_i1_human_name )                     | No      | string  | No         | -          | Human Name             |
| + [name](#llm_unit_oneOf_i0_model_oneOf_i1_name )                                 | No      | string  | No         | -          | Name                   |
| + [input_context_limit](#llm_unit_oneOf_i0_model_oneOf_i1_input_context_limit )   | No      | integer | No         | -          | Input Context Limit    |
| + [output_context_limit](#llm_unit_oneOf_i0_model_oneOf_i1_output_context_limit ) | No      | integer | No         | -          | Output Context Limit   |
| + [supports_tools](#llm_unit_oneOf_i0_model_oneOf_i1_supports_tools )             | No      | boolean | No         | -          | Supports Tools         |
| + [supports_image_input](#llm_unit_oneOf_i0_model_oneOf_i1_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input   |
| + [supports_audio_input](#llm_unit_oneOf_i0_model_oneOf_i1_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input   |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i1_implementation"></a>3.2.2.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** claude-3-opus-20240229

Specific value: `"claude-3-opus-20240229"`

###### <a name="llm_unit_oneOf_i0_model_oneOf_i1_human_name"></a>3.2.2.2.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i1_name"></a>3.2.2.2.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i1_input_context_limit"></a>3.2.2.2.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i1_output_context_limit"></a>3.2.2.2.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i1_supports_tools"></a>3.2.2.2.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i1_supports_image_input"></a>3.2.2.2.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i1_supports_audio_input"></a>3.2.2.2.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i2"></a>3.2.2.3. Property `claude-3-sonnet-20240229.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./claude-3-sonnet-20240229.json                                      |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description        |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | ------------------------ |
| - [implementation](#llm_unit_oneOf_i0_model_oneOf_i2_implementation )             | No      | const   | No         | -          | claude-3-sonnet-20240229 |
| + [human_name](#llm_unit_oneOf_i0_model_oneOf_i2_human_name )                     | No      | string  | No         | -          | Human Name               |
| + [name](#llm_unit_oneOf_i0_model_oneOf_i2_name )                                 | No      | string  | No         | -          | Name                     |
| + [input_context_limit](#llm_unit_oneOf_i0_model_oneOf_i2_input_context_limit )   | No      | integer | No         | -          | Input Context Limit      |
| + [output_context_limit](#llm_unit_oneOf_i0_model_oneOf_i2_output_context_limit ) | No      | integer | No         | -          | Output Context Limit     |
| + [supports_tools](#llm_unit_oneOf_i0_model_oneOf_i2_supports_tools )             | No      | boolean | No         | -          | Supports Tools           |
| + [supports_image_input](#llm_unit_oneOf_i0_model_oneOf_i2_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input     |
| + [supports_audio_input](#llm_unit_oneOf_i0_model_oneOf_i2_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input     |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i2_implementation"></a>3.2.2.3.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** claude-3-sonnet-20240229

Specific value: `"claude-3-sonnet-20240229"`

###### <a name="llm_unit_oneOf_i0_model_oneOf_i2_human_name"></a>3.2.2.3.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i2_name"></a>3.2.2.3.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i2_input_context_limit"></a>3.2.2.3.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i2_output_context_limit"></a>3.2.2.3.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i2_supports_tools"></a>3.2.2.3.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i2_supports_image_input"></a>3.2.2.3.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i2_supports_audio_input"></a>3.2.2.3.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i3"></a>3.2.2.4. Property `gpt-3.5-turbo.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./gpt-3.5-turbo.json                                                 |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_oneOf_i0_model_oneOf_i3_implementation )             | No      | const   | No         | -          | gpt-3.5-turbo        |
| + [human_name](#llm_unit_oneOf_i0_model_oneOf_i3_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_oneOf_i0_model_oneOf_i3_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_oneOf_i0_model_oneOf_i3_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_oneOf_i0_model_oneOf_i3_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_oneOf_i0_model_oneOf_i3_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_oneOf_i0_model_oneOf_i3_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_oneOf_i0_model_oneOf_i3_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i3_implementation"></a>3.2.2.4.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** gpt-3.5-turbo

Specific value: `"gpt-3.5-turbo"`

###### <a name="llm_unit_oneOf_i0_model_oneOf_i3_human_name"></a>3.2.2.4.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i3_name"></a>3.2.2.4.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i3_input_context_limit"></a>3.2.2.4.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i3_output_context_limit"></a>3.2.2.4.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i3_supports_tools"></a>3.2.2.4.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i3_supports_image_input"></a>3.2.2.4.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i3_supports_audio_input"></a>3.2.2.4.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i4"></a>3.2.2.5. Property `gpt-4-turbo.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./gpt-4-turbo.json                                                   |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_oneOf_i0_model_oneOf_i4_implementation )             | No      | const   | No         | -          | gpt-4-turbo          |
| + [human_name](#llm_unit_oneOf_i0_model_oneOf_i4_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_oneOf_i0_model_oneOf_i4_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_oneOf_i0_model_oneOf_i4_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_oneOf_i0_model_oneOf_i4_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_oneOf_i0_model_oneOf_i4_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_oneOf_i0_model_oneOf_i4_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_oneOf_i0_model_oneOf_i4_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i4_implementation"></a>3.2.2.5.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** gpt-4-turbo

Specific value: `"gpt-4-turbo"`

###### <a name="llm_unit_oneOf_i0_model_oneOf_i4_human_name"></a>3.2.2.5.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i4_name"></a>3.2.2.5.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i4_input_context_limit"></a>3.2.2.5.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i4_output_context_limit"></a>3.2.2.5.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i4_supports_tools"></a>3.2.2.5.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i4_supports_image_input"></a>3.2.2.5.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i4_supports_audio_input"></a>3.2.2.5.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i5"></a>3.2.2.6. Property `gpt-4o.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./gpt-4o.json                                                        |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_oneOf_i0_model_oneOf_i5_implementation )             | No      | const   | No         | -          | gpt-4o               |
| + [human_name](#llm_unit_oneOf_i0_model_oneOf_i5_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_oneOf_i0_model_oneOf_i5_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_oneOf_i0_model_oneOf_i5_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_oneOf_i0_model_oneOf_i5_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_oneOf_i0_model_oneOf_i5_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_oneOf_i0_model_oneOf_i5_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_oneOf_i0_model_oneOf_i5_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i5_implementation"></a>3.2.2.6.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** gpt-4o

Specific value: `"gpt-4o"`

###### <a name="llm_unit_oneOf_i0_model_oneOf_i5_human_name"></a>3.2.2.6.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i5_name"></a>3.2.2.6.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i5_input_context_limit"></a>3.2.2.6.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i5_output_context_limit"></a>3.2.2.6.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i5_supports_tools"></a>3.2.2.6.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i5_supports_image_input"></a>3.2.2.6.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i5_supports_audio_input"></a>3.2.2.6.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i6"></a>3.2.2.7. Property `llama3-8b.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./llama3-8b.json                                                     |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_oneOf_i0_model_oneOf_i6_implementation )             | No      | const   | No         | -          | llama3-8b            |
| + [human_name](#llm_unit_oneOf_i0_model_oneOf_i6_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_oneOf_i0_model_oneOf_i6_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_oneOf_i0_model_oneOf_i6_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_oneOf_i0_model_oneOf_i6_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_oneOf_i0_model_oneOf_i6_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_oneOf_i0_model_oneOf_i6_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_oneOf_i0_model_oneOf_i6_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i6_implementation"></a>3.2.2.7.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** llama3-8b

Specific value: `"llama3-8b"`

###### <a name="llm_unit_oneOf_i0_model_oneOf_i6_human_name"></a>3.2.2.7.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i6_name"></a>3.2.2.7.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i6_input_context_limit"></a>3.2.2.7.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i6_output_context_limit"></a>3.2.2.7.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i6_supports_tools"></a>3.2.2.7.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i6_supports_image_input"></a>3.2.2.7.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i6_supports_audio_input"></a>3.2.2.7.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i7"></a>3.2.2.8. Property `mistral-large-latest.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./mistral-large-latest.json                                          |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_oneOf_i0_model_oneOf_i7_implementation )             | No      | const   | No         | -          | mistral-large-latest |
| + [human_name](#llm_unit_oneOf_i0_model_oneOf_i7_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_oneOf_i0_model_oneOf_i7_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_oneOf_i0_model_oneOf_i7_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_oneOf_i0_model_oneOf_i7_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_oneOf_i0_model_oneOf_i7_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_oneOf_i0_model_oneOf_i7_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_oneOf_i0_model_oneOf_i7_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i7_implementation"></a>3.2.2.8.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** mistral-large-latest

Specific value: `"mistral-large-latest"`

###### <a name="llm_unit_oneOf_i0_model_oneOf_i7_human_name"></a>3.2.2.8.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i7_name"></a>3.2.2.8.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i7_input_context_limit"></a>3.2.2.8.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i7_output_context_limit"></a>3.2.2.8.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i7_supports_tools"></a>3.2.2.8.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i7_supports_image_input"></a>3.2.2.8.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i7_supports_audio_input"></a>3.2.2.8.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i8"></a>3.2.2.9. Property `mistral-medium-latest.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./mistral-medium-latest.json                                         |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description     |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | --------------------- |
| - [implementation](#llm_unit_oneOf_i0_model_oneOf_i8_implementation )             | No      | const   | No         | -          | mistral-medium-latest |
| + [human_name](#llm_unit_oneOf_i0_model_oneOf_i8_human_name )                     | No      | string  | No         | -          | Human Name            |
| + [name](#llm_unit_oneOf_i0_model_oneOf_i8_name )                                 | No      | string  | No         | -          | Name                  |
| + [input_context_limit](#llm_unit_oneOf_i0_model_oneOf_i8_input_context_limit )   | No      | integer | No         | -          | Input Context Limit   |
| + [output_context_limit](#llm_unit_oneOf_i0_model_oneOf_i8_output_context_limit ) | No      | integer | No         | -          | Output Context Limit  |
| + [supports_tools](#llm_unit_oneOf_i0_model_oneOf_i8_supports_tools )             | No      | boolean | No         | -          | Supports Tools        |
| + [supports_image_input](#llm_unit_oneOf_i0_model_oneOf_i8_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input  |
| + [supports_audio_input](#llm_unit_oneOf_i0_model_oneOf_i8_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input  |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i8_implementation"></a>3.2.2.9.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** mistral-medium-latest

Specific value: `"mistral-medium-latest"`

###### <a name="llm_unit_oneOf_i0_model_oneOf_i8_human_name"></a>3.2.2.9.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i8_name"></a>3.2.2.9.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i8_input_context_limit"></a>3.2.2.9.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i8_output_context_limit"></a>3.2.2.9.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i8_supports_tools"></a>3.2.2.9.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i8_supports_image_input"></a>3.2.2.9.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i8_supports_audio_input"></a>3.2.2.9.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i9"></a>3.2.2.10. Property `mistral-small-latest.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./mistral-small-latest.json                                          |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_oneOf_i0_model_oneOf_i9_implementation )             | No      | const   | No         | -          | mistral-small-latest |
| + [human_name](#llm_unit_oneOf_i0_model_oneOf_i9_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_oneOf_i0_model_oneOf_i9_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_oneOf_i0_model_oneOf_i9_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_oneOf_i0_model_oneOf_i9_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_oneOf_i0_model_oneOf_i9_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_oneOf_i0_model_oneOf_i9_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_oneOf_i0_model_oneOf_i9_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i9_implementation"></a>3.2.2.10.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** mistral-small-latest

Specific value: `"mistral-small-latest"`

###### <a name="llm_unit_oneOf_i0_model_oneOf_i9_human_name"></a>3.2.2.10.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i9_name"></a>3.2.2.10.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i9_input_context_limit"></a>3.2.2.10.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i9_output_context_limit"></a>3.2.2.10.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i9_supports_tools"></a>3.2.2.10.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i9_supports_image_input"></a>3.2.2.10.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i9_supports_audio_input"></a>3.2.2.10.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

#### <a name="llm_unit_oneOf_i1_temperature"></a>3.2.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

#### <a name="llm_unit_oneOf_i1_force_json"></a>3.2.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

#### <a name="llm_unit_oneOf_i1_max_tokens"></a>3.2.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                   |
| ------------------------------------------------ |
| [item 0](#llm_unit_oneOf_i1_max_tokens_anyOf_i0) |
| [item 1](#llm_unit_oneOf_i1_max_tokens_anyOf_i1) |

##### <a name="llm_unit_oneOf_i1_max_tokens_anyOf_i0"></a>3.2.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

##### <a name="llm_unit_oneOf_i1_max_tokens_anyOf_i1"></a>3.2.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="llm_unit_oneOf_i1_client_args"></a>3.2.6. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

### <a name="llm_unit_oneOf_i2"></a>3.3. Property `OllamaLLMUnit.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./OllamaLLMUnit.json                                                 |

| Property                                               | Pattern | Type        | Deprecated | Definition                        | Title/Description               |
| ------------------------------------------------------ | ------- | ----------- | ---------- | --------------------------------- | ------------------------------- |
| - [implementation](#llm_unit_oneOf_i2_implementation ) | No      | const       | No         | -                                 | OllamaLLMUnit                   |
| - [model](#llm_unit_oneOf_i2_model )                   | No      | object      | No         | In [LLMModel](/docs/components/llmmodel/overview) | Overview of LLMModel components |
| - [temperature](#llm_unit_oneOf_i2_temperature )       | No      | number      | No         | -                                 | Temperature                     |
| - [force_json](#llm_unit_oneOf_i2_force_json )         | No      | boolean     | No         | -                                 | Force Json                      |
| - [max_tokens](#llm_unit_oneOf_i2_max_tokens )         | No      | Combination | No         | -                                 | Max Tokens                      |
| - [client_options](#llm_unit_oneOf_i2_client_options ) | No      | object      | No         | -                                 | Client Options                  |

#### <a name="llm_unit_oneOf_i2_implementation"></a>3.3.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OllamaLLMUnit

Specific value: `"OllamaLLMUnit"`

#### <a name="llm_unit_oneOf_i2_model"></a>3.3.2. Property `model`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"llama3"`                                                                |
| **Defined in**            | [LLMModel](/docs/components/llmmodel/overview)                                            |

**Description:** Overview of LLMModel components

| One of(Option)                                                     |
| ------------------------------------------------------------------ |
| [claude-3-haiku-20240307.json](#llm_unit_oneOf_i0_model_oneOf_i0)  |
| [claude-3-opus-20240229.json](#llm_unit_oneOf_i0_model_oneOf_i1)   |
| [claude-3-sonnet-20240229.json](#llm_unit_oneOf_i0_model_oneOf_i2) |
| [gpt-3.5-turbo.json](#llm_unit_oneOf_i0_model_oneOf_i3)            |
| [gpt-4-turbo.json](#llm_unit_oneOf_i0_model_oneOf_i4)              |
| [gpt-4o.json](#llm_unit_oneOf_i0_model_oneOf_i5)                   |
| [llama3-8b.json](#llm_unit_oneOf_i0_model_oneOf_i6)                |
| [mistral-large-latest.json](#llm_unit_oneOf_i0_model_oneOf_i7)     |
| [mistral-medium-latest.json](#llm_unit_oneOf_i0_model_oneOf_i8)    |
| [mistral-small-latest.json](#llm_unit_oneOf_i0_model_oneOf_i9)     |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i0"></a>3.3.2.1. Property `claude-3-haiku-20240307.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./claude-3-haiku-20240307.json                                       |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description       |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | ----------------------- |
| - [implementation](#llm_unit_oneOf_i0_model_oneOf_i0_implementation )             | No      | const   | No         | -          | claude-3-haiku-20240307 |
| + [human_name](#llm_unit_oneOf_i0_model_oneOf_i0_human_name )                     | No      | string  | No         | -          | Human Name              |
| + [name](#llm_unit_oneOf_i0_model_oneOf_i0_name )                                 | No      | string  | No         | -          | Name                    |
| + [input_context_limit](#llm_unit_oneOf_i0_model_oneOf_i0_input_context_limit )   | No      | integer | No         | -          | Input Context Limit     |
| + [output_context_limit](#llm_unit_oneOf_i0_model_oneOf_i0_output_context_limit ) | No      | integer | No         | -          | Output Context Limit    |
| + [supports_tools](#llm_unit_oneOf_i0_model_oneOf_i0_supports_tools )             | No      | boolean | No         | -          | Supports Tools          |
| + [supports_image_input](#llm_unit_oneOf_i0_model_oneOf_i0_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input    |
| + [supports_audio_input](#llm_unit_oneOf_i0_model_oneOf_i0_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input    |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i0_implementation"></a>3.3.2.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** claude-3-haiku-20240307

Specific value: `"claude-3-haiku-20240307"`

###### <a name="llm_unit_oneOf_i0_model_oneOf_i0_human_name"></a>3.3.2.1.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i0_name"></a>3.3.2.1.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i0_input_context_limit"></a>3.3.2.1.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i0_output_context_limit"></a>3.3.2.1.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i0_supports_tools"></a>3.3.2.1.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i0_supports_image_input"></a>3.3.2.1.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i0_supports_audio_input"></a>3.3.2.1.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i1"></a>3.3.2.2. Property `claude-3-opus-20240229.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./claude-3-opus-20240229.json                                        |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description      |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | ---------------------- |
| - [implementation](#llm_unit_oneOf_i0_model_oneOf_i1_implementation )             | No      | const   | No         | -          | claude-3-opus-20240229 |
| + [human_name](#llm_unit_oneOf_i0_model_oneOf_i1_human_name )                     | No      | string  | No         | -          | Human Name             |
| + [name](#llm_unit_oneOf_i0_model_oneOf_i1_name )                                 | No      | string  | No         | -          | Name                   |
| + [input_context_limit](#llm_unit_oneOf_i0_model_oneOf_i1_input_context_limit )   | No      | integer | No         | -          | Input Context Limit    |
| + [output_context_limit](#llm_unit_oneOf_i0_model_oneOf_i1_output_context_limit ) | No      | integer | No         | -          | Output Context Limit   |
| + [supports_tools](#llm_unit_oneOf_i0_model_oneOf_i1_supports_tools )             | No      | boolean | No         | -          | Supports Tools         |
| + [supports_image_input](#llm_unit_oneOf_i0_model_oneOf_i1_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input   |
| + [supports_audio_input](#llm_unit_oneOf_i0_model_oneOf_i1_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input   |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i1_implementation"></a>3.3.2.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** claude-3-opus-20240229

Specific value: `"claude-3-opus-20240229"`

###### <a name="llm_unit_oneOf_i0_model_oneOf_i1_human_name"></a>3.3.2.2.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i1_name"></a>3.3.2.2.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i1_input_context_limit"></a>3.3.2.2.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i1_output_context_limit"></a>3.3.2.2.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i1_supports_tools"></a>3.3.2.2.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i1_supports_image_input"></a>3.3.2.2.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i1_supports_audio_input"></a>3.3.2.2.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i2"></a>3.3.2.3. Property `claude-3-sonnet-20240229.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./claude-3-sonnet-20240229.json                                      |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description        |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | ------------------------ |
| - [implementation](#llm_unit_oneOf_i0_model_oneOf_i2_implementation )             | No      | const   | No         | -          | claude-3-sonnet-20240229 |
| + [human_name](#llm_unit_oneOf_i0_model_oneOf_i2_human_name )                     | No      | string  | No         | -          | Human Name               |
| + [name](#llm_unit_oneOf_i0_model_oneOf_i2_name )                                 | No      | string  | No         | -          | Name                     |
| + [input_context_limit](#llm_unit_oneOf_i0_model_oneOf_i2_input_context_limit )   | No      | integer | No         | -          | Input Context Limit      |
| + [output_context_limit](#llm_unit_oneOf_i0_model_oneOf_i2_output_context_limit ) | No      | integer | No         | -          | Output Context Limit     |
| + [supports_tools](#llm_unit_oneOf_i0_model_oneOf_i2_supports_tools )             | No      | boolean | No         | -          | Supports Tools           |
| + [supports_image_input](#llm_unit_oneOf_i0_model_oneOf_i2_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input     |
| + [supports_audio_input](#llm_unit_oneOf_i0_model_oneOf_i2_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input     |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i2_implementation"></a>3.3.2.3.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** claude-3-sonnet-20240229

Specific value: `"claude-3-sonnet-20240229"`

###### <a name="llm_unit_oneOf_i0_model_oneOf_i2_human_name"></a>3.3.2.3.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i2_name"></a>3.3.2.3.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i2_input_context_limit"></a>3.3.2.3.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i2_output_context_limit"></a>3.3.2.3.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i2_supports_tools"></a>3.3.2.3.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i2_supports_image_input"></a>3.3.2.3.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i2_supports_audio_input"></a>3.3.2.3.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i3"></a>3.3.2.4. Property `gpt-3.5-turbo.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./gpt-3.5-turbo.json                                                 |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_oneOf_i0_model_oneOf_i3_implementation )             | No      | const   | No         | -          | gpt-3.5-turbo        |
| + [human_name](#llm_unit_oneOf_i0_model_oneOf_i3_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_oneOf_i0_model_oneOf_i3_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_oneOf_i0_model_oneOf_i3_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_oneOf_i0_model_oneOf_i3_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_oneOf_i0_model_oneOf_i3_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_oneOf_i0_model_oneOf_i3_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_oneOf_i0_model_oneOf_i3_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i3_implementation"></a>3.3.2.4.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** gpt-3.5-turbo

Specific value: `"gpt-3.5-turbo"`

###### <a name="llm_unit_oneOf_i0_model_oneOf_i3_human_name"></a>3.3.2.4.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i3_name"></a>3.3.2.4.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i3_input_context_limit"></a>3.3.2.4.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i3_output_context_limit"></a>3.3.2.4.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i3_supports_tools"></a>3.3.2.4.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i3_supports_image_input"></a>3.3.2.4.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i3_supports_audio_input"></a>3.3.2.4.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i4"></a>3.3.2.5. Property `gpt-4-turbo.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./gpt-4-turbo.json                                                   |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_oneOf_i0_model_oneOf_i4_implementation )             | No      | const   | No         | -          | gpt-4-turbo          |
| + [human_name](#llm_unit_oneOf_i0_model_oneOf_i4_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_oneOf_i0_model_oneOf_i4_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_oneOf_i0_model_oneOf_i4_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_oneOf_i0_model_oneOf_i4_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_oneOf_i0_model_oneOf_i4_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_oneOf_i0_model_oneOf_i4_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_oneOf_i0_model_oneOf_i4_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i4_implementation"></a>3.3.2.5.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** gpt-4-turbo

Specific value: `"gpt-4-turbo"`

###### <a name="llm_unit_oneOf_i0_model_oneOf_i4_human_name"></a>3.3.2.5.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i4_name"></a>3.3.2.5.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i4_input_context_limit"></a>3.3.2.5.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i4_output_context_limit"></a>3.3.2.5.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i4_supports_tools"></a>3.3.2.5.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i4_supports_image_input"></a>3.3.2.5.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i4_supports_audio_input"></a>3.3.2.5.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i5"></a>3.3.2.6. Property `gpt-4o.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./gpt-4o.json                                                        |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_oneOf_i0_model_oneOf_i5_implementation )             | No      | const   | No         | -          | gpt-4o               |
| + [human_name](#llm_unit_oneOf_i0_model_oneOf_i5_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_oneOf_i0_model_oneOf_i5_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_oneOf_i0_model_oneOf_i5_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_oneOf_i0_model_oneOf_i5_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_oneOf_i0_model_oneOf_i5_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_oneOf_i0_model_oneOf_i5_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_oneOf_i0_model_oneOf_i5_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i5_implementation"></a>3.3.2.6.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** gpt-4o

Specific value: `"gpt-4o"`

###### <a name="llm_unit_oneOf_i0_model_oneOf_i5_human_name"></a>3.3.2.6.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i5_name"></a>3.3.2.6.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i5_input_context_limit"></a>3.3.2.6.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i5_output_context_limit"></a>3.3.2.6.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i5_supports_tools"></a>3.3.2.6.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i5_supports_image_input"></a>3.3.2.6.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i5_supports_audio_input"></a>3.3.2.6.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i6"></a>3.3.2.7. Property `llama3-8b.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./llama3-8b.json                                                     |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_oneOf_i0_model_oneOf_i6_implementation )             | No      | const   | No         | -          | llama3-8b            |
| + [human_name](#llm_unit_oneOf_i0_model_oneOf_i6_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_oneOf_i0_model_oneOf_i6_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_oneOf_i0_model_oneOf_i6_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_oneOf_i0_model_oneOf_i6_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_oneOf_i0_model_oneOf_i6_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_oneOf_i0_model_oneOf_i6_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_oneOf_i0_model_oneOf_i6_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i6_implementation"></a>3.3.2.7.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** llama3-8b

Specific value: `"llama3-8b"`

###### <a name="llm_unit_oneOf_i0_model_oneOf_i6_human_name"></a>3.3.2.7.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i6_name"></a>3.3.2.7.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i6_input_context_limit"></a>3.3.2.7.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i6_output_context_limit"></a>3.3.2.7.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i6_supports_tools"></a>3.3.2.7.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i6_supports_image_input"></a>3.3.2.7.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i6_supports_audio_input"></a>3.3.2.7.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i7"></a>3.3.2.8. Property `mistral-large-latest.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./mistral-large-latest.json                                          |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_oneOf_i0_model_oneOf_i7_implementation )             | No      | const   | No         | -          | mistral-large-latest |
| + [human_name](#llm_unit_oneOf_i0_model_oneOf_i7_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_oneOf_i0_model_oneOf_i7_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_oneOf_i0_model_oneOf_i7_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_oneOf_i0_model_oneOf_i7_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_oneOf_i0_model_oneOf_i7_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_oneOf_i0_model_oneOf_i7_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_oneOf_i0_model_oneOf_i7_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i7_implementation"></a>3.3.2.8.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** mistral-large-latest

Specific value: `"mistral-large-latest"`

###### <a name="llm_unit_oneOf_i0_model_oneOf_i7_human_name"></a>3.3.2.8.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i7_name"></a>3.3.2.8.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i7_input_context_limit"></a>3.3.2.8.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i7_output_context_limit"></a>3.3.2.8.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i7_supports_tools"></a>3.3.2.8.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i7_supports_image_input"></a>3.3.2.8.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i7_supports_audio_input"></a>3.3.2.8.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i8"></a>3.3.2.9. Property `mistral-medium-latest.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./mistral-medium-latest.json                                         |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description     |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | --------------------- |
| - [implementation](#llm_unit_oneOf_i0_model_oneOf_i8_implementation )             | No      | const   | No         | -          | mistral-medium-latest |
| + [human_name](#llm_unit_oneOf_i0_model_oneOf_i8_human_name )                     | No      | string  | No         | -          | Human Name            |
| + [name](#llm_unit_oneOf_i0_model_oneOf_i8_name )                                 | No      | string  | No         | -          | Name                  |
| + [input_context_limit](#llm_unit_oneOf_i0_model_oneOf_i8_input_context_limit )   | No      | integer | No         | -          | Input Context Limit   |
| + [output_context_limit](#llm_unit_oneOf_i0_model_oneOf_i8_output_context_limit ) | No      | integer | No         | -          | Output Context Limit  |
| + [supports_tools](#llm_unit_oneOf_i0_model_oneOf_i8_supports_tools )             | No      | boolean | No         | -          | Supports Tools        |
| + [supports_image_input](#llm_unit_oneOf_i0_model_oneOf_i8_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input  |
| + [supports_audio_input](#llm_unit_oneOf_i0_model_oneOf_i8_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input  |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i8_implementation"></a>3.3.2.9.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** mistral-medium-latest

Specific value: `"mistral-medium-latest"`

###### <a name="llm_unit_oneOf_i0_model_oneOf_i8_human_name"></a>3.3.2.9.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i8_name"></a>3.3.2.9.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i8_input_context_limit"></a>3.3.2.9.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i8_output_context_limit"></a>3.3.2.9.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i8_supports_tools"></a>3.3.2.9.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i8_supports_image_input"></a>3.3.2.9.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i8_supports_audio_input"></a>3.3.2.9.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i9"></a>3.3.2.10. Property `mistral-small-latest.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./mistral-small-latest.json                                          |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_oneOf_i0_model_oneOf_i9_implementation )             | No      | const   | No         | -          | mistral-small-latest |
| + [human_name](#llm_unit_oneOf_i0_model_oneOf_i9_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_oneOf_i0_model_oneOf_i9_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_oneOf_i0_model_oneOf_i9_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_oneOf_i0_model_oneOf_i9_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_oneOf_i0_model_oneOf_i9_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_oneOf_i0_model_oneOf_i9_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_oneOf_i0_model_oneOf_i9_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i9_implementation"></a>3.3.2.10.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** mistral-small-latest

Specific value: `"mistral-small-latest"`

###### <a name="llm_unit_oneOf_i0_model_oneOf_i9_human_name"></a>3.3.2.10.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i9_name"></a>3.3.2.10.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i9_input_context_limit"></a>3.3.2.10.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i9_output_context_limit"></a>3.3.2.10.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i9_supports_tools"></a>3.3.2.10.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i9_supports_image_input"></a>3.3.2.10.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i9_supports_audio_input"></a>3.3.2.10.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

#### <a name="llm_unit_oneOf_i2_temperature"></a>3.3.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

#### <a name="llm_unit_oneOf_i2_force_json"></a>3.3.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

#### <a name="llm_unit_oneOf_i2_max_tokens"></a>3.3.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                   |
| ------------------------------------------------ |
| [item 0](#llm_unit_oneOf_i2_max_tokens_anyOf_i0) |
| [item 1](#llm_unit_oneOf_i2_max_tokens_anyOf_i1) |

##### <a name="llm_unit_oneOf_i2_max_tokens_anyOf_i0"></a>3.3.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

##### <a name="llm_unit_oneOf_i2_max_tokens_anyOf_i1"></a>3.3.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="llm_unit_oneOf_i2_client_options"></a>3.3.6. Property `client_options`

**Title:** Client Options

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

### <a name="llm_unit_oneOf_i3"></a>3.4. Property `OpenAIGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./OpenAIGPT.json                                                     |

| Property                                                       | Pattern | Type        | Deprecated | Definition                                       | Title/Description                              |
| -------------------------------------------------------------- | ------- | ----------- | ---------- | ------------------------------------------------ | ---------------------------------------------- |
| - [implementation](#llm_unit_oneOf_i3_implementation )         | No      | const       | No         | -                                                | OpenAIGPT                                      |
| - [model](#llm_unit_oneOf_i3_model )                           | No      | object      | No         | In [LLMModel](/docs/components/llmmodel/overview)                | Overview of LLMModel components                |
| - [temperature](#llm_unit_oneOf_i3_temperature )               | No      | number      | No         | -                                                | Temperature                                    |
| - [force_json](#llm_unit_oneOf_i3_force_json )                 | No      | boolean     | No         | -                                                | Force Json                                     |
| - [max_tokens](#llm_unit_oneOf_i3_max_tokens )                 | No      | Combination | No         | -                                                | Max Tokens                                     |
| - [connection_handler](#llm_unit_oneOf_i3_connection_handler ) | No      | object      | No         | In [OpenAIConnectionHandler](/docs/components/openaiconnectionhandler/overview) | Overview of OpenAIConnectionHandler components |

#### <a name="llm_unit_oneOf_i3_implementation"></a>3.4.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OpenAIGPT

Specific value: `"OpenAIGPT"`

#### <a name="llm_unit_oneOf_i3_model"></a>3.4.2. Property `model`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMModel"`                                                              |
| **Defined in**            | [LLMModel](/docs/components/llmmodel/overview)                                            |

**Description:** Overview of LLMModel components

| One of(Option)                                                     |
| ------------------------------------------------------------------ |
| [claude-3-haiku-20240307.json](#llm_unit_oneOf_i0_model_oneOf_i0)  |
| [claude-3-opus-20240229.json](#llm_unit_oneOf_i0_model_oneOf_i1)   |
| [claude-3-sonnet-20240229.json](#llm_unit_oneOf_i0_model_oneOf_i2) |
| [gpt-3.5-turbo.json](#llm_unit_oneOf_i0_model_oneOf_i3)            |
| [gpt-4-turbo.json](#llm_unit_oneOf_i0_model_oneOf_i4)              |
| [gpt-4o.json](#llm_unit_oneOf_i0_model_oneOf_i5)                   |
| [llama3-8b.json](#llm_unit_oneOf_i0_model_oneOf_i6)                |
| [mistral-large-latest.json](#llm_unit_oneOf_i0_model_oneOf_i7)     |
| [mistral-medium-latest.json](#llm_unit_oneOf_i0_model_oneOf_i8)    |
| [mistral-small-latest.json](#llm_unit_oneOf_i0_model_oneOf_i9)     |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i0"></a>3.4.2.1. Property `claude-3-haiku-20240307.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./claude-3-haiku-20240307.json                                       |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description       |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | ----------------------- |
| - [implementation](#llm_unit_oneOf_i0_model_oneOf_i0_implementation )             | No      | const   | No         | -          | claude-3-haiku-20240307 |
| + [human_name](#llm_unit_oneOf_i0_model_oneOf_i0_human_name )                     | No      | string  | No         | -          | Human Name              |
| + [name](#llm_unit_oneOf_i0_model_oneOf_i0_name )                                 | No      | string  | No         | -          | Name                    |
| + [input_context_limit](#llm_unit_oneOf_i0_model_oneOf_i0_input_context_limit )   | No      | integer | No         | -          | Input Context Limit     |
| + [output_context_limit](#llm_unit_oneOf_i0_model_oneOf_i0_output_context_limit ) | No      | integer | No         | -          | Output Context Limit    |
| + [supports_tools](#llm_unit_oneOf_i0_model_oneOf_i0_supports_tools )             | No      | boolean | No         | -          | Supports Tools          |
| + [supports_image_input](#llm_unit_oneOf_i0_model_oneOf_i0_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input    |
| + [supports_audio_input](#llm_unit_oneOf_i0_model_oneOf_i0_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input    |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i0_implementation"></a>3.4.2.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** claude-3-haiku-20240307

Specific value: `"claude-3-haiku-20240307"`

###### <a name="llm_unit_oneOf_i0_model_oneOf_i0_human_name"></a>3.4.2.1.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i0_name"></a>3.4.2.1.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i0_input_context_limit"></a>3.4.2.1.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i0_output_context_limit"></a>3.4.2.1.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i0_supports_tools"></a>3.4.2.1.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i0_supports_image_input"></a>3.4.2.1.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i0_supports_audio_input"></a>3.4.2.1.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i1"></a>3.4.2.2. Property `claude-3-opus-20240229.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./claude-3-opus-20240229.json                                        |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description      |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | ---------------------- |
| - [implementation](#llm_unit_oneOf_i0_model_oneOf_i1_implementation )             | No      | const   | No         | -          | claude-3-opus-20240229 |
| + [human_name](#llm_unit_oneOf_i0_model_oneOf_i1_human_name )                     | No      | string  | No         | -          | Human Name             |
| + [name](#llm_unit_oneOf_i0_model_oneOf_i1_name )                                 | No      | string  | No         | -          | Name                   |
| + [input_context_limit](#llm_unit_oneOf_i0_model_oneOf_i1_input_context_limit )   | No      | integer | No         | -          | Input Context Limit    |
| + [output_context_limit](#llm_unit_oneOf_i0_model_oneOf_i1_output_context_limit ) | No      | integer | No         | -          | Output Context Limit   |
| + [supports_tools](#llm_unit_oneOf_i0_model_oneOf_i1_supports_tools )             | No      | boolean | No         | -          | Supports Tools         |
| + [supports_image_input](#llm_unit_oneOf_i0_model_oneOf_i1_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input   |
| + [supports_audio_input](#llm_unit_oneOf_i0_model_oneOf_i1_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input   |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i1_implementation"></a>3.4.2.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** claude-3-opus-20240229

Specific value: `"claude-3-opus-20240229"`

###### <a name="llm_unit_oneOf_i0_model_oneOf_i1_human_name"></a>3.4.2.2.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i1_name"></a>3.4.2.2.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i1_input_context_limit"></a>3.4.2.2.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i1_output_context_limit"></a>3.4.2.2.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i1_supports_tools"></a>3.4.2.2.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i1_supports_image_input"></a>3.4.2.2.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i1_supports_audio_input"></a>3.4.2.2.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i2"></a>3.4.2.3. Property `claude-3-sonnet-20240229.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./claude-3-sonnet-20240229.json                                      |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description        |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | ------------------------ |
| - [implementation](#llm_unit_oneOf_i0_model_oneOf_i2_implementation )             | No      | const   | No         | -          | claude-3-sonnet-20240229 |
| + [human_name](#llm_unit_oneOf_i0_model_oneOf_i2_human_name )                     | No      | string  | No         | -          | Human Name               |
| + [name](#llm_unit_oneOf_i0_model_oneOf_i2_name )                                 | No      | string  | No         | -          | Name                     |
| + [input_context_limit](#llm_unit_oneOf_i0_model_oneOf_i2_input_context_limit )   | No      | integer | No         | -          | Input Context Limit      |
| + [output_context_limit](#llm_unit_oneOf_i0_model_oneOf_i2_output_context_limit ) | No      | integer | No         | -          | Output Context Limit     |
| + [supports_tools](#llm_unit_oneOf_i0_model_oneOf_i2_supports_tools )             | No      | boolean | No         | -          | Supports Tools           |
| + [supports_image_input](#llm_unit_oneOf_i0_model_oneOf_i2_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input     |
| + [supports_audio_input](#llm_unit_oneOf_i0_model_oneOf_i2_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input     |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i2_implementation"></a>3.4.2.3.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** claude-3-sonnet-20240229

Specific value: `"claude-3-sonnet-20240229"`

###### <a name="llm_unit_oneOf_i0_model_oneOf_i2_human_name"></a>3.4.2.3.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i2_name"></a>3.4.2.3.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i2_input_context_limit"></a>3.4.2.3.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i2_output_context_limit"></a>3.4.2.3.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i2_supports_tools"></a>3.4.2.3.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i2_supports_image_input"></a>3.4.2.3.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i2_supports_audio_input"></a>3.4.2.3.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i3"></a>3.4.2.4. Property `gpt-3.5-turbo.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./gpt-3.5-turbo.json                                                 |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_oneOf_i0_model_oneOf_i3_implementation )             | No      | const   | No         | -          | gpt-3.5-turbo        |
| + [human_name](#llm_unit_oneOf_i0_model_oneOf_i3_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_oneOf_i0_model_oneOf_i3_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_oneOf_i0_model_oneOf_i3_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_oneOf_i0_model_oneOf_i3_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_oneOf_i0_model_oneOf_i3_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_oneOf_i0_model_oneOf_i3_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_oneOf_i0_model_oneOf_i3_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i3_implementation"></a>3.4.2.4.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** gpt-3.5-turbo

Specific value: `"gpt-3.5-turbo"`

###### <a name="llm_unit_oneOf_i0_model_oneOf_i3_human_name"></a>3.4.2.4.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i3_name"></a>3.4.2.4.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i3_input_context_limit"></a>3.4.2.4.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i3_output_context_limit"></a>3.4.2.4.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i3_supports_tools"></a>3.4.2.4.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i3_supports_image_input"></a>3.4.2.4.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i3_supports_audio_input"></a>3.4.2.4.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i4"></a>3.4.2.5. Property `gpt-4-turbo.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./gpt-4-turbo.json                                                   |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_oneOf_i0_model_oneOf_i4_implementation )             | No      | const   | No         | -          | gpt-4-turbo          |
| + [human_name](#llm_unit_oneOf_i0_model_oneOf_i4_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_oneOf_i0_model_oneOf_i4_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_oneOf_i0_model_oneOf_i4_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_oneOf_i0_model_oneOf_i4_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_oneOf_i0_model_oneOf_i4_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_oneOf_i0_model_oneOf_i4_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_oneOf_i0_model_oneOf_i4_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i4_implementation"></a>3.4.2.5.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** gpt-4-turbo

Specific value: `"gpt-4-turbo"`

###### <a name="llm_unit_oneOf_i0_model_oneOf_i4_human_name"></a>3.4.2.5.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i4_name"></a>3.4.2.5.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i4_input_context_limit"></a>3.4.2.5.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i4_output_context_limit"></a>3.4.2.5.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i4_supports_tools"></a>3.4.2.5.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i4_supports_image_input"></a>3.4.2.5.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i4_supports_audio_input"></a>3.4.2.5.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i5"></a>3.4.2.6. Property `gpt-4o.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./gpt-4o.json                                                        |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_oneOf_i0_model_oneOf_i5_implementation )             | No      | const   | No         | -          | gpt-4o               |
| + [human_name](#llm_unit_oneOf_i0_model_oneOf_i5_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_oneOf_i0_model_oneOf_i5_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_oneOf_i0_model_oneOf_i5_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_oneOf_i0_model_oneOf_i5_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_oneOf_i0_model_oneOf_i5_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_oneOf_i0_model_oneOf_i5_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_oneOf_i0_model_oneOf_i5_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i5_implementation"></a>3.4.2.6.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** gpt-4o

Specific value: `"gpt-4o"`

###### <a name="llm_unit_oneOf_i0_model_oneOf_i5_human_name"></a>3.4.2.6.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i5_name"></a>3.4.2.6.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i5_input_context_limit"></a>3.4.2.6.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i5_output_context_limit"></a>3.4.2.6.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i5_supports_tools"></a>3.4.2.6.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i5_supports_image_input"></a>3.4.2.6.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i5_supports_audio_input"></a>3.4.2.6.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i6"></a>3.4.2.7. Property `llama3-8b.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./llama3-8b.json                                                     |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_oneOf_i0_model_oneOf_i6_implementation )             | No      | const   | No         | -          | llama3-8b            |
| + [human_name](#llm_unit_oneOf_i0_model_oneOf_i6_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_oneOf_i0_model_oneOf_i6_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_oneOf_i0_model_oneOf_i6_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_oneOf_i0_model_oneOf_i6_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_oneOf_i0_model_oneOf_i6_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_oneOf_i0_model_oneOf_i6_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_oneOf_i0_model_oneOf_i6_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i6_implementation"></a>3.4.2.7.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** llama3-8b

Specific value: `"llama3-8b"`

###### <a name="llm_unit_oneOf_i0_model_oneOf_i6_human_name"></a>3.4.2.7.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i6_name"></a>3.4.2.7.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i6_input_context_limit"></a>3.4.2.7.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i6_output_context_limit"></a>3.4.2.7.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i6_supports_tools"></a>3.4.2.7.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i6_supports_image_input"></a>3.4.2.7.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i6_supports_audio_input"></a>3.4.2.7.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i7"></a>3.4.2.8. Property `mistral-large-latest.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./mistral-large-latest.json                                          |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_oneOf_i0_model_oneOf_i7_implementation )             | No      | const   | No         | -          | mistral-large-latest |
| + [human_name](#llm_unit_oneOf_i0_model_oneOf_i7_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_oneOf_i0_model_oneOf_i7_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_oneOf_i0_model_oneOf_i7_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_oneOf_i0_model_oneOf_i7_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_oneOf_i0_model_oneOf_i7_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_oneOf_i0_model_oneOf_i7_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_oneOf_i0_model_oneOf_i7_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i7_implementation"></a>3.4.2.8.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** mistral-large-latest

Specific value: `"mistral-large-latest"`

###### <a name="llm_unit_oneOf_i0_model_oneOf_i7_human_name"></a>3.4.2.8.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i7_name"></a>3.4.2.8.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i7_input_context_limit"></a>3.4.2.8.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i7_output_context_limit"></a>3.4.2.8.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i7_supports_tools"></a>3.4.2.8.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i7_supports_image_input"></a>3.4.2.8.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i7_supports_audio_input"></a>3.4.2.8.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i8"></a>3.4.2.9. Property `mistral-medium-latest.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./mistral-medium-latest.json                                         |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description     |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | --------------------- |
| - [implementation](#llm_unit_oneOf_i0_model_oneOf_i8_implementation )             | No      | const   | No         | -          | mistral-medium-latest |
| + [human_name](#llm_unit_oneOf_i0_model_oneOf_i8_human_name )                     | No      | string  | No         | -          | Human Name            |
| + [name](#llm_unit_oneOf_i0_model_oneOf_i8_name )                                 | No      | string  | No         | -          | Name                  |
| + [input_context_limit](#llm_unit_oneOf_i0_model_oneOf_i8_input_context_limit )   | No      | integer | No         | -          | Input Context Limit   |
| + [output_context_limit](#llm_unit_oneOf_i0_model_oneOf_i8_output_context_limit ) | No      | integer | No         | -          | Output Context Limit  |
| + [supports_tools](#llm_unit_oneOf_i0_model_oneOf_i8_supports_tools )             | No      | boolean | No         | -          | Supports Tools        |
| + [supports_image_input](#llm_unit_oneOf_i0_model_oneOf_i8_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input  |
| + [supports_audio_input](#llm_unit_oneOf_i0_model_oneOf_i8_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input  |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i8_implementation"></a>3.4.2.9.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** mistral-medium-latest

Specific value: `"mistral-medium-latest"`

###### <a name="llm_unit_oneOf_i0_model_oneOf_i8_human_name"></a>3.4.2.9.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i8_name"></a>3.4.2.9.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i8_input_context_limit"></a>3.4.2.9.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i8_output_context_limit"></a>3.4.2.9.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i8_supports_tools"></a>3.4.2.9.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i8_supports_image_input"></a>3.4.2.9.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i8_supports_audio_input"></a>3.4.2.9.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i9"></a>3.4.2.10. Property `mistral-small-latest.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./mistral-small-latest.json                                          |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_oneOf_i0_model_oneOf_i9_implementation )             | No      | const   | No         | -          | mistral-small-latest |
| + [human_name](#llm_unit_oneOf_i0_model_oneOf_i9_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_oneOf_i0_model_oneOf_i9_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_oneOf_i0_model_oneOf_i9_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_oneOf_i0_model_oneOf_i9_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_oneOf_i0_model_oneOf_i9_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_oneOf_i0_model_oneOf_i9_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_oneOf_i0_model_oneOf_i9_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i9_implementation"></a>3.4.2.10.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** mistral-small-latest

Specific value: `"mistral-small-latest"`

###### <a name="llm_unit_oneOf_i0_model_oneOf_i9_human_name"></a>3.4.2.10.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i9_name"></a>3.4.2.10.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i9_input_context_limit"></a>3.4.2.10.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i9_output_context_limit"></a>3.4.2.10.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i9_supports_tools"></a>3.4.2.10.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i9_supports_image_input"></a>3.4.2.10.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_oneOf_i0_model_oneOf_i9_supports_audio_input"></a>3.4.2.10.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

#### <a name="llm_unit_oneOf_i3_temperature"></a>3.4.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

#### <a name="llm_unit_oneOf_i3_force_json"></a>3.4.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

#### <a name="llm_unit_oneOf_i3_max_tokens"></a>3.4.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                   |
| ------------------------------------------------ |
| [item 0](#llm_unit_oneOf_i3_max_tokens_anyOf_i0) |
| [item 1](#llm_unit_oneOf_i3_max_tokens_anyOf_i1) |

##### <a name="llm_unit_oneOf_i3_max_tokens_anyOf_i0"></a>3.4.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

##### <a name="llm_unit_oneOf_i3_max_tokens_anyOf_i1"></a>3.4.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="llm_unit_oneOf_i3_connection_handler"></a>3.4.6. Property `connection_handler`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"OpenAIConnectionHandler"`                                               |
| **Defined in**            | [OpenAIConnectionHandler](/docs/components/openaiconnectionhandler/overview)                             |

**Description:** Overview of OpenAIConnectionHandler components

| Property                                                                                    | Pattern | Type            | Deprecated | Definition | Title/Description            |
| ------------------------------------------------------------------------------------------- | ------- | --------------- | ---------- | ---------- | ---------------------------- |
| - [implementation](#llm_unit_oneOf_i3_connection_handler_implementation )                   | No      | const           | No         | -          | AzureOpenAIConnectionHandler |
| - [azure_ad_token_provider](#llm_unit_oneOf_i3_connection_handler_azure_ad_token_provider ) | No      | Combination     | No         | -          | -                            |
| - [token_provider_scopes](#llm_unit_oneOf_i3_connection_handler_token_provider_scopes )     | No      | array of string | No         | -          | Token Provider Scopes        |
| - [api_version](#llm_unit_oneOf_i3_connection_handler_api_version )                         | No      | string          | No         | -          | Api Version                  |
| - [](#llm_unit_oneOf_i3_connection_handler_additionalProperties )                           | No      | object          | No         | -          | -                            |

##### <a name="llm_unit_oneOf_i3_connection_handler_implementation"></a>3.4.6.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AzureOpenAIConnectionHandler

Specific value: `"AzureOpenAIConnectionHandler"`

##### <a name="llm_unit_oneOf_i3_connection_handler_azure_ad_token_provider"></a>3.4.6.2. Property `azure_ad_token_provider`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

| Any of(Option)                                                                      |
| ----------------------------------------------------------------------------------- |
| [Reference](#llm_unit_oneOf_i3_connection_handler_azure_ad_token_provider_anyOf_i0) |
| [item 1](#llm_unit_oneOf_i3_connection_handler_azure_ad_token_provider_anyOf_i1)    |

###### <a name="llm_unit_oneOf_i3_connection_handler_azure_ad_token_provider_anyOf_i0"></a>3.4.6.2.1. Property `Reference`

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

| Property                                                                                                   | Pattern | Type   | Deprecated | Definition | Title/Description |
| ---------------------------------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#llm_unit_oneOf_i3_connection_handler_azure_ad_token_provider_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#llm_unit_oneOf_i3_connection_handler_azure_ad_token_provider_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="llm_unit_oneOf_i3_connection_handler_azure_ad_token_provider_anyOf_i0_implementation"></a>3.4.6.2.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="llm_unit_oneOf_i3_connection_handler_azure_ad_token_provider_anyOf_i1"></a>3.4.6.2.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

##### <a name="llm_unit_oneOf_i3_connection_handler_token_provider_scopes"></a>3.4.6.3. Property `token_provider_scopes`

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

| Each item of this array must be                                                                  | Description |
| ------------------------------------------------------------------------------------------------ | ----------- |
| [token_provider_scopes items](#llm_unit_oneOf_i3_connection_handler_token_provider_scopes_items) | -           |

###### <a name="autogenerated_heading_2"></a>3.4.6.3.1. token_provider_scopes items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

##### <a name="llm_unit_oneOf_i3_connection_handler_api_version"></a>3.4.6.4. Property `api_version`

**Title:** Api Version

|              |                |
| ------------ | -------------- |
| **Type**     | `string`       |
| **Required** | No             |
| **Default**  | `"2024-02-01"` |

### <a name="llm_unit_oneOf_i4"></a>3.5. Property `ToolCallLLMWrapper.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Same definition as**    | [ToolCallLLMWrapper](#root)                                               |

## <a name="model"></a>4. Property `model`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                   |
| -------------------------------- |
| [overview.json](#model_anyOf_i0) |
| [item 1](#model_anyOf_i1)        |

### <a name="model_anyOf_i0"></a>4.1. Property `overview.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMModel"`                                                              |
| **Defined in**            | [LLMModel](/docs/components/llmmodel/overview)                                            |

**Description:** Overview of LLMModel components

| One of(Option)                                                     |
| ------------------------------------------------------------------ |
| [claude-3-haiku-20240307.json](#llm_unit_oneOf_i0_model_oneOf_i0)  |
| [claude-3-opus-20240229.json](#llm_unit_oneOf_i0_model_oneOf_i1)   |
| [claude-3-sonnet-20240229.json](#llm_unit_oneOf_i0_model_oneOf_i2) |
| [gpt-3.5-turbo.json](#llm_unit_oneOf_i0_model_oneOf_i3)            |
| [gpt-4-turbo.json](#llm_unit_oneOf_i0_model_oneOf_i4)              |
| [gpt-4o.json](#llm_unit_oneOf_i0_model_oneOf_i5)                   |
| [llama3-8b.json](#llm_unit_oneOf_i0_model_oneOf_i6)                |
| [mistral-large-latest.json](#llm_unit_oneOf_i0_model_oneOf_i7)     |
| [mistral-medium-latest.json](#llm_unit_oneOf_i0_model_oneOf_i8)    |
| [mistral-small-latest.json](#llm_unit_oneOf_i0_model_oneOf_i9)     |

#### <a name="llm_unit_oneOf_i0_model_oneOf_i0"></a>4.1.1. Property `claude-3-haiku-20240307.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./claude-3-haiku-20240307.json                                       |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description       |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | ----------------------- |
| - [implementation](#llm_unit_oneOf_i0_model_oneOf_i0_implementation )             | No      | const   | No         | -          | claude-3-haiku-20240307 |
| + [human_name](#llm_unit_oneOf_i0_model_oneOf_i0_human_name )                     | No      | string  | No         | -          | Human Name              |
| + [name](#llm_unit_oneOf_i0_model_oneOf_i0_name )                                 | No      | string  | No         | -          | Name                    |
| + [input_context_limit](#llm_unit_oneOf_i0_model_oneOf_i0_input_context_limit )   | No      | integer | No         | -          | Input Context Limit     |
| + [output_context_limit](#llm_unit_oneOf_i0_model_oneOf_i0_output_context_limit ) | No      | integer | No         | -          | Output Context Limit    |
| + [supports_tools](#llm_unit_oneOf_i0_model_oneOf_i0_supports_tools )             | No      | boolean | No         | -          | Supports Tools          |
| + [supports_image_input](#llm_unit_oneOf_i0_model_oneOf_i0_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input    |
| + [supports_audio_input](#llm_unit_oneOf_i0_model_oneOf_i0_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input    |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i0_implementation"></a>4.1.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** claude-3-haiku-20240307

Specific value: `"claude-3-haiku-20240307"`

##### <a name="llm_unit_oneOf_i0_model_oneOf_i0_human_name"></a>4.1.1.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i0_name"></a>4.1.1.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i0_input_context_limit"></a>4.1.1.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i0_output_context_limit"></a>4.1.1.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i0_supports_tools"></a>4.1.1.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i0_supports_image_input"></a>4.1.1.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i0_supports_audio_input"></a>4.1.1.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

#### <a name="llm_unit_oneOf_i0_model_oneOf_i1"></a>4.1.2. Property `claude-3-opus-20240229.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./claude-3-opus-20240229.json                                        |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description      |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | ---------------------- |
| - [implementation](#llm_unit_oneOf_i0_model_oneOf_i1_implementation )             | No      | const   | No         | -          | claude-3-opus-20240229 |
| + [human_name](#llm_unit_oneOf_i0_model_oneOf_i1_human_name )                     | No      | string  | No         | -          | Human Name             |
| + [name](#llm_unit_oneOf_i0_model_oneOf_i1_name )                                 | No      | string  | No         | -          | Name                   |
| + [input_context_limit](#llm_unit_oneOf_i0_model_oneOf_i1_input_context_limit )   | No      | integer | No         | -          | Input Context Limit    |
| + [output_context_limit](#llm_unit_oneOf_i0_model_oneOf_i1_output_context_limit ) | No      | integer | No         | -          | Output Context Limit   |
| + [supports_tools](#llm_unit_oneOf_i0_model_oneOf_i1_supports_tools )             | No      | boolean | No         | -          | Supports Tools         |
| + [supports_image_input](#llm_unit_oneOf_i0_model_oneOf_i1_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input   |
| + [supports_audio_input](#llm_unit_oneOf_i0_model_oneOf_i1_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input   |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i1_implementation"></a>4.1.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** claude-3-opus-20240229

Specific value: `"claude-3-opus-20240229"`

##### <a name="llm_unit_oneOf_i0_model_oneOf_i1_human_name"></a>4.1.2.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i1_name"></a>4.1.2.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i1_input_context_limit"></a>4.1.2.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i1_output_context_limit"></a>4.1.2.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i1_supports_tools"></a>4.1.2.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i1_supports_image_input"></a>4.1.2.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i1_supports_audio_input"></a>4.1.2.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

#### <a name="llm_unit_oneOf_i0_model_oneOf_i2"></a>4.1.3. Property `claude-3-sonnet-20240229.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./claude-3-sonnet-20240229.json                                      |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description        |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | ------------------------ |
| - [implementation](#llm_unit_oneOf_i0_model_oneOf_i2_implementation )             | No      | const   | No         | -          | claude-3-sonnet-20240229 |
| + [human_name](#llm_unit_oneOf_i0_model_oneOf_i2_human_name )                     | No      | string  | No         | -          | Human Name               |
| + [name](#llm_unit_oneOf_i0_model_oneOf_i2_name )                                 | No      | string  | No         | -          | Name                     |
| + [input_context_limit](#llm_unit_oneOf_i0_model_oneOf_i2_input_context_limit )   | No      | integer | No         | -          | Input Context Limit      |
| + [output_context_limit](#llm_unit_oneOf_i0_model_oneOf_i2_output_context_limit ) | No      | integer | No         | -          | Output Context Limit     |
| + [supports_tools](#llm_unit_oneOf_i0_model_oneOf_i2_supports_tools )             | No      | boolean | No         | -          | Supports Tools           |
| + [supports_image_input](#llm_unit_oneOf_i0_model_oneOf_i2_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input     |
| + [supports_audio_input](#llm_unit_oneOf_i0_model_oneOf_i2_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input     |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i2_implementation"></a>4.1.3.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** claude-3-sonnet-20240229

Specific value: `"claude-3-sonnet-20240229"`

##### <a name="llm_unit_oneOf_i0_model_oneOf_i2_human_name"></a>4.1.3.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i2_name"></a>4.1.3.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i2_input_context_limit"></a>4.1.3.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i2_output_context_limit"></a>4.1.3.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i2_supports_tools"></a>4.1.3.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i2_supports_image_input"></a>4.1.3.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i2_supports_audio_input"></a>4.1.3.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

#### <a name="llm_unit_oneOf_i0_model_oneOf_i3"></a>4.1.4. Property `gpt-3.5-turbo.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./gpt-3.5-turbo.json                                                 |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_oneOf_i0_model_oneOf_i3_implementation )             | No      | const   | No         | -          | gpt-3.5-turbo        |
| + [human_name](#llm_unit_oneOf_i0_model_oneOf_i3_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_oneOf_i0_model_oneOf_i3_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_oneOf_i0_model_oneOf_i3_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_oneOf_i0_model_oneOf_i3_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_oneOf_i0_model_oneOf_i3_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_oneOf_i0_model_oneOf_i3_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_oneOf_i0_model_oneOf_i3_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i3_implementation"></a>4.1.4.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** gpt-3.5-turbo

Specific value: `"gpt-3.5-turbo"`

##### <a name="llm_unit_oneOf_i0_model_oneOf_i3_human_name"></a>4.1.4.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i3_name"></a>4.1.4.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i3_input_context_limit"></a>4.1.4.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i3_output_context_limit"></a>4.1.4.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i3_supports_tools"></a>4.1.4.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i3_supports_image_input"></a>4.1.4.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i3_supports_audio_input"></a>4.1.4.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

#### <a name="llm_unit_oneOf_i0_model_oneOf_i4"></a>4.1.5. Property `gpt-4-turbo.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./gpt-4-turbo.json                                                   |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_oneOf_i0_model_oneOf_i4_implementation )             | No      | const   | No         | -          | gpt-4-turbo          |
| + [human_name](#llm_unit_oneOf_i0_model_oneOf_i4_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_oneOf_i0_model_oneOf_i4_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_oneOf_i0_model_oneOf_i4_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_oneOf_i0_model_oneOf_i4_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_oneOf_i0_model_oneOf_i4_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_oneOf_i0_model_oneOf_i4_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_oneOf_i0_model_oneOf_i4_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i4_implementation"></a>4.1.5.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** gpt-4-turbo

Specific value: `"gpt-4-turbo"`

##### <a name="llm_unit_oneOf_i0_model_oneOf_i4_human_name"></a>4.1.5.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i4_name"></a>4.1.5.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i4_input_context_limit"></a>4.1.5.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i4_output_context_limit"></a>4.1.5.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i4_supports_tools"></a>4.1.5.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i4_supports_image_input"></a>4.1.5.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i4_supports_audio_input"></a>4.1.5.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

#### <a name="llm_unit_oneOf_i0_model_oneOf_i5"></a>4.1.6. Property `gpt-4o.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./gpt-4o.json                                                        |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_oneOf_i0_model_oneOf_i5_implementation )             | No      | const   | No         | -          | gpt-4o               |
| + [human_name](#llm_unit_oneOf_i0_model_oneOf_i5_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_oneOf_i0_model_oneOf_i5_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_oneOf_i0_model_oneOf_i5_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_oneOf_i0_model_oneOf_i5_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_oneOf_i0_model_oneOf_i5_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_oneOf_i0_model_oneOf_i5_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_oneOf_i0_model_oneOf_i5_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i5_implementation"></a>4.1.6.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** gpt-4o

Specific value: `"gpt-4o"`

##### <a name="llm_unit_oneOf_i0_model_oneOf_i5_human_name"></a>4.1.6.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i5_name"></a>4.1.6.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i5_input_context_limit"></a>4.1.6.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i5_output_context_limit"></a>4.1.6.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i5_supports_tools"></a>4.1.6.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i5_supports_image_input"></a>4.1.6.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i5_supports_audio_input"></a>4.1.6.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

#### <a name="llm_unit_oneOf_i0_model_oneOf_i6"></a>4.1.7. Property `llama3-8b.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./llama3-8b.json                                                     |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_oneOf_i0_model_oneOf_i6_implementation )             | No      | const   | No         | -          | llama3-8b            |
| + [human_name](#llm_unit_oneOf_i0_model_oneOf_i6_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_oneOf_i0_model_oneOf_i6_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_oneOf_i0_model_oneOf_i6_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_oneOf_i0_model_oneOf_i6_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_oneOf_i0_model_oneOf_i6_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_oneOf_i0_model_oneOf_i6_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_oneOf_i0_model_oneOf_i6_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i6_implementation"></a>4.1.7.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** llama3-8b

Specific value: `"llama3-8b"`

##### <a name="llm_unit_oneOf_i0_model_oneOf_i6_human_name"></a>4.1.7.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i6_name"></a>4.1.7.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i6_input_context_limit"></a>4.1.7.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i6_output_context_limit"></a>4.1.7.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i6_supports_tools"></a>4.1.7.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i6_supports_image_input"></a>4.1.7.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i6_supports_audio_input"></a>4.1.7.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

#### <a name="llm_unit_oneOf_i0_model_oneOf_i7"></a>4.1.8. Property `mistral-large-latest.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./mistral-large-latest.json                                          |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_oneOf_i0_model_oneOf_i7_implementation )             | No      | const   | No         | -          | mistral-large-latest |
| + [human_name](#llm_unit_oneOf_i0_model_oneOf_i7_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_oneOf_i0_model_oneOf_i7_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_oneOf_i0_model_oneOf_i7_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_oneOf_i0_model_oneOf_i7_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_oneOf_i0_model_oneOf_i7_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_oneOf_i0_model_oneOf_i7_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_oneOf_i0_model_oneOf_i7_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i7_implementation"></a>4.1.8.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** mistral-large-latest

Specific value: `"mistral-large-latest"`

##### <a name="llm_unit_oneOf_i0_model_oneOf_i7_human_name"></a>4.1.8.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i7_name"></a>4.1.8.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i7_input_context_limit"></a>4.1.8.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i7_output_context_limit"></a>4.1.8.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i7_supports_tools"></a>4.1.8.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i7_supports_image_input"></a>4.1.8.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i7_supports_audio_input"></a>4.1.8.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

#### <a name="llm_unit_oneOf_i0_model_oneOf_i8"></a>4.1.9. Property `mistral-medium-latest.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./mistral-medium-latest.json                                         |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description     |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | --------------------- |
| - [implementation](#llm_unit_oneOf_i0_model_oneOf_i8_implementation )             | No      | const   | No         | -          | mistral-medium-latest |
| + [human_name](#llm_unit_oneOf_i0_model_oneOf_i8_human_name )                     | No      | string  | No         | -          | Human Name            |
| + [name](#llm_unit_oneOf_i0_model_oneOf_i8_name )                                 | No      | string  | No         | -          | Name                  |
| + [input_context_limit](#llm_unit_oneOf_i0_model_oneOf_i8_input_context_limit )   | No      | integer | No         | -          | Input Context Limit   |
| + [output_context_limit](#llm_unit_oneOf_i0_model_oneOf_i8_output_context_limit ) | No      | integer | No         | -          | Output Context Limit  |
| + [supports_tools](#llm_unit_oneOf_i0_model_oneOf_i8_supports_tools )             | No      | boolean | No         | -          | Supports Tools        |
| + [supports_image_input](#llm_unit_oneOf_i0_model_oneOf_i8_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input  |
| + [supports_audio_input](#llm_unit_oneOf_i0_model_oneOf_i8_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input  |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i8_implementation"></a>4.1.9.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** mistral-medium-latest

Specific value: `"mistral-medium-latest"`

##### <a name="llm_unit_oneOf_i0_model_oneOf_i8_human_name"></a>4.1.9.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i8_name"></a>4.1.9.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i8_input_context_limit"></a>4.1.9.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i8_output_context_limit"></a>4.1.9.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i8_supports_tools"></a>4.1.9.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i8_supports_image_input"></a>4.1.9.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i8_supports_audio_input"></a>4.1.9.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

#### <a name="llm_unit_oneOf_i0_model_oneOf_i9"></a>4.1.10. Property `mistral-small-latest.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./mistral-small-latest.json                                          |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_oneOf_i0_model_oneOf_i9_implementation )             | No      | const   | No         | -          | mistral-small-latest |
| + [human_name](#llm_unit_oneOf_i0_model_oneOf_i9_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_oneOf_i0_model_oneOf_i9_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_oneOf_i0_model_oneOf_i9_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_oneOf_i0_model_oneOf_i9_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_oneOf_i0_model_oneOf_i9_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_oneOf_i0_model_oneOf_i9_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_oneOf_i0_model_oneOf_i9_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i9_implementation"></a>4.1.10.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** mistral-small-latest

Specific value: `"mistral-small-latest"`

##### <a name="llm_unit_oneOf_i0_model_oneOf_i9_human_name"></a>4.1.10.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i9_name"></a>4.1.10.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i9_input_context_limit"></a>4.1.10.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i9_output_context_limit"></a>4.1.10.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i9_supports_tools"></a>4.1.10.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i9_supports_image_input"></a>4.1.10.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_oneOf_i0_model_oneOf_i9_supports_audio_input"></a>4.1.10.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

### <a name="model_anyOf_i1"></a>4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

----------------------------------------------------------------------------------------------------------------------------
