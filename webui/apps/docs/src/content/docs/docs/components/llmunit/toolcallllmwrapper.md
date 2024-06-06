---
title: ToolCallLLMWrapper
description: Description of ToolCallLLMWrapper component
---

| Property                                       | Pattern | Type        | Deprecated | Definition                       | Title/Description                                                    |
| ---------------------------------------------- | ------- | ----------- | ---------- | -------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#implementation )           | No      | const       | No         | -                                | ToolCallLLMWrapper                                                   |
| - [tool_message_prompt](#tool_message_prompt ) | No      | string      | No         | -                                | Tool Message Prompt                                                  |
| - [llm_unit](#llm_unit )                       | No      | object      | No         | In [LLMUnit](/docs/components/llmunit/overview) | Overview of <class 'eidolon_ai_sdk.apu.llm_unit.LLMUnit'> components |
| - [model](#model )                             | No      | Combination | No         | -                                | -                                                                    |

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
| **Default**               | `"LLMUnit"`                                                               |
| **Defined in**            | [LLMUnit](/docs/components/llmunit/overview)                                             |

**Description:** Overview of <class 'eidolon_ai_sdk.apu.llm_unit.LLMUnit'> components

| Any of(Option)                                |
| --------------------------------------------- |
| [AnthropicLLMUnit.json](#llm_unit_anyOf_i0)   |
| [MistralGPT.json](#llm_unit_anyOf_i1)         |
| [OpenAIGPT.json](#llm_unit_anyOf_i2)          |
| [ToolCallLLMWrapper.json](#llm_unit_anyOf_i3) |

### <a name="llm_unit_anyOf_i0"></a>3.1. Property `AnthropicLLMUnit.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./AnthropicLLMUnit.json                                              |

| Property                                               | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------ | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#llm_unit_anyOf_i0_implementation ) | No      | const       | No         | -          | AnthropicLLMUnit   |
| - [model](#llm_unit_anyOf_i0_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#llm_unit_anyOf_i0_temperature )       | No      | number      | No         | -          | Temperature        |
| - [max_tokens](#llm_unit_anyOf_i0_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_args](#llm_unit_anyOf_i0_client_args )       | No      | object      | No         | -          | Client Args        |

#### <a name="llm_unit_anyOf_i0_implementation"></a>3.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AnthropicLLMUnit

Specific value: `"AnthropicLLMUnit"`

#### <a name="llm_unit_anyOf_i0_model"></a>3.1.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"claude-3-opus-20240229"`                                                |

| Property                                                     | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------ | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#llm_unit_anyOf_i0_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#llm_unit_anyOf_i0_model_additionalProperties )         | No      | object | No         | -          | -                 |

##### <a name="llm_unit_anyOf_i0_model_implementation"></a>3.1.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="llm_unit_anyOf_i0_temperature"></a>3.1.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

#### <a name="llm_unit_anyOf_i0_max_tokens"></a>3.1.4. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                   |
| ------------------------------------------------ |
| [item 0](#llm_unit_anyOf_i0_max_tokens_anyOf_i0) |
| [item 1](#llm_unit_anyOf_i0_max_tokens_anyOf_i1) |

##### <a name="llm_unit_anyOf_i0_max_tokens_anyOf_i0"></a>3.1.4.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

##### <a name="llm_unit_anyOf_i0_max_tokens_anyOf_i1"></a>3.1.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="llm_unit_anyOf_i0_client_args"></a>3.1.5. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

### <a name="llm_unit_anyOf_i1"></a>3.2. Property `MistralGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./MistralGPT.json                                                    |

| Property                                               | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------ | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#llm_unit_anyOf_i1_implementation ) | No      | const       | No         | -          | MistralGPT         |
| - [model](#llm_unit_anyOf_i1_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#llm_unit_anyOf_i1_temperature )       | No      | number      | No         | -          | Temperature        |
| - [force_json](#llm_unit_anyOf_i1_force_json )         | No      | boolean     | No         | -          | Force Json         |
| - [max_tokens](#llm_unit_anyOf_i1_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_args](#llm_unit_anyOf_i1_client_args )       | No      | object      | No         | -          | Client Args        |

#### <a name="llm_unit_anyOf_i1_implementation"></a>3.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** MistralGPT

Specific value: `"MistralGPT"`

#### <a name="llm_unit_anyOf_i1_model"></a>3.2.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"mistral-large-latest"`                                                  |

| Property                                                     | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------ | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#llm_unit_anyOf_i1_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#llm_unit_anyOf_i1_model_additionalProperties )         | No      | object | No         | -          | -                 |

##### <a name="llm_unit_anyOf_i1_model_implementation"></a>3.2.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="llm_unit_anyOf_i1_temperature"></a>3.2.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

#### <a name="llm_unit_anyOf_i1_force_json"></a>3.2.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

#### <a name="llm_unit_anyOf_i1_max_tokens"></a>3.2.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                   |
| ------------------------------------------------ |
| [item 0](#llm_unit_anyOf_i1_max_tokens_anyOf_i0) |
| [item 1](#llm_unit_anyOf_i1_max_tokens_anyOf_i1) |

##### <a name="llm_unit_anyOf_i1_max_tokens_anyOf_i0"></a>3.2.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

##### <a name="llm_unit_anyOf_i1_max_tokens_anyOf_i1"></a>3.2.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="llm_unit_anyOf_i1_client_args"></a>3.2.6. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

### <a name="llm_unit_anyOf_i2"></a>3.3. Property `OpenAIGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./OpenAIGPT.json                                                     |

| Property                                                       | Pattern | Type        | Deprecated | Definition | Title/Description                 |
| -------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | --------------------------------- |
| - [implementation](#llm_unit_anyOf_i2_implementation )         | No      | const       | No         | -          | OpenAIGPT                         |
| - [model](#llm_unit_anyOf_i2_model )                           | No      | object      | No         | -          | LLMModel Reference                |
| - [temperature](#llm_unit_anyOf_i2_temperature )               | No      | number      | No         | -          | Temperature                       |
| - [force_json](#llm_unit_anyOf_i2_force_json )                 | No      | boolean     | No         | -          | Force Json                        |
| - [max_tokens](#llm_unit_anyOf_i2_max_tokens )                 | No      | Combination | No         | -          | Max Tokens                        |
| - [connection_handler](#llm_unit_anyOf_i2_connection_handler ) | No      | object      | No         | -          | OpenAIConnectionHandler Reference |

#### <a name="llm_unit_anyOf_i2_implementation"></a>3.3.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OpenAIGPT

Specific value: `"OpenAIGPT"`

#### <a name="llm_unit_anyOf_i2_model"></a>3.3.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"gpt-4-turbo"`                                                           |

| Property                                                     | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------ | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#llm_unit_anyOf_i2_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#llm_unit_anyOf_i2_model_additionalProperties )         | No      | object | No         | -          | -                 |

##### <a name="llm_unit_anyOf_i2_model_implementation"></a>3.3.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="llm_unit_anyOf_i2_temperature"></a>3.3.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

#### <a name="llm_unit_anyOf_i2_force_json"></a>3.3.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

#### <a name="llm_unit_anyOf_i2_max_tokens"></a>3.3.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                   |
| ------------------------------------------------ |
| [item 0](#llm_unit_anyOf_i2_max_tokens_anyOf_i0) |
| [item 1](#llm_unit_anyOf_i2_max_tokens_anyOf_i1) |

##### <a name="llm_unit_anyOf_i2_max_tokens_anyOf_i0"></a>3.3.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

##### <a name="llm_unit_anyOf_i2_max_tokens_anyOf_i1"></a>3.3.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="llm_unit_anyOf_i2_connection_handler"></a>3.3.6. Property `connection_handler`

**Title:** OpenAIConnectionHandler Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"OpenAIConnectionHandler"`                                               |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#llm_unit_anyOf_i2_connection_handler_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#llm_unit_anyOf_i2_connection_handler_additionalProperties )         | No      | object | No         | -          | -                 |

##### <a name="llm_unit_anyOf_i2_connection_handler_implementation"></a>3.3.6.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

### <a name="llm_unit_anyOf_i3"></a>3.4. Property `ToolCallLLMWrapper.json`

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

| Any of(Option)                        |
| ------------------------------------- |
| [LLMModel Reference](#model_anyOf_i0) |
| [item 1](#model_anyOf_i1)             |

### <a name="model_anyOf_i0"></a>4.1. Property `LLMModel Reference`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.llm_unit.LLMModel"`                                  |

| Property                                            | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#model_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#model_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

#### <a name="model_anyOf_i0_implementation"></a>4.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

### <a name="model_anyOf_i1"></a>4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

----------------------------------------------------------------------------------------------------------------------------
