---
title: MistralMedium
description: Description of MistralMedium component
---

| Property                                             | Pattern | Type            | Deprecated | Definition                       | Title/Description                                                    |
| ---------------------------------------------------- | ------- | --------------- | ---------- | -------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#implementation )                 | No      | const           | No         | -                                | MistralMedium                                                        |
| - [max_num_function_calls](#max_num_function_calls ) | No      | integer         | No         | -                                | Max Num Function Calls                                               |
| - [io_unit](#io_unit )                               | No      | object          | No         | -                                | IOUnit Reference                                                     |
| - [memory_unit](#memory_unit )                       | No      | object          | No         | -                                | MemoryUnit Reference                                                 |
| - [llm_unit](#llm_unit )                             | No      | object          | No         | In [LLMUnit](/docs/components/llmunit/overview) | Overview of <class 'eidolon_ai_sdk.apu.llm_unit.LLMUnit'> components |
| - [logic_units](#logic_units )                       | No      | array of object | No         | -                                | Logic Units                                                          |
| - [audio_unit](#audio_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [image_unit](#image_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [record_conversation](#record_conversation )       | No      | boolean         | No         | -                                | Record Conversation                                                  |
| - [allow_tool_errors](#allow_tool_errors )           | No      | boolean         | No         | -                                | Allow Tool Errors                                                    |
| - [document_processor](#document_processor )         | No      | object          | No         | -                                | DocumentProcessor Reference                                          |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** MistralMedium

Specific value: `"MistralMedium"`

## <a name="max_num_function_calls"></a>2. Property `max_num_function_calls`

**Title:** Max Num Function Calls

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `10`      |

**Description:** The maximum number of function calls to make in a single request.

## <a name="io_unit"></a>3. Property `io_unit`

**Title:** IOUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"IOUnit"`                                                                |

| Property                                     | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#io_unit_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#io_unit_additionalProperties )         | No      | object | No         | -          | -                 |

### <a name="io_unit_implementation"></a>3.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

## <a name="memory_unit"></a>4. Property `memory_unit`

**Title:** MemoryUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"MemoryUnit"`                                                            |

| Property                                         | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------ | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#memory_unit_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#memory_unit_additionalProperties )         | No      | object | No         | -          | -                 |

### <a name="memory_unit_implementation"></a>4.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

## <a name="llm_unit"></a>5. Property `llm_unit`

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

### <a name="llm_unit_anyOf_i0"></a>5.1. Property `AnthropicLLMUnit.json`

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

#### <a name="llm_unit_anyOf_i0_implementation"></a>5.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AnthropicLLMUnit

Specific value: `"AnthropicLLMUnit"`

#### <a name="llm_unit_anyOf_i0_model"></a>5.1.2. Property `model`

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

##### <a name="llm_unit_anyOf_i0_model_implementation"></a>5.1.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="llm_unit_anyOf_i0_temperature"></a>5.1.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

#### <a name="llm_unit_anyOf_i0_max_tokens"></a>5.1.4. Property `max_tokens`

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

##### <a name="llm_unit_anyOf_i0_max_tokens_anyOf_i0"></a>5.1.4.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

##### <a name="llm_unit_anyOf_i0_max_tokens_anyOf_i1"></a>5.1.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="llm_unit_anyOf_i0_client_args"></a>5.1.5. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

### <a name="llm_unit_anyOf_i1"></a>5.2. Property `MistralGPT.json`

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

#### <a name="llm_unit_anyOf_i1_implementation"></a>5.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** MistralGPT

Specific value: `"MistralGPT"`

#### <a name="llm_unit_anyOf_i1_model"></a>5.2.2. Property `model`

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

##### <a name="llm_unit_anyOf_i1_model_implementation"></a>5.2.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="llm_unit_anyOf_i1_temperature"></a>5.2.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

#### <a name="llm_unit_anyOf_i1_force_json"></a>5.2.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

#### <a name="llm_unit_anyOf_i1_max_tokens"></a>5.2.5. Property `max_tokens`

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

##### <a name="llm_unit_anyOf_i1_max_tokens_anyOf_i0"></a>5.2.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

##### <a name="llm_unit_anyOf_i1_max_tokens_anyOf_i1"></a>5.2.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="llm_unit_anyOf_i1_client_args"></a>5.2.6. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

### <a name="llm_unit_anyOf_i2"></a>5.3. Property `OpenAIGPT.json`

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

#### <a name="llm_unit_anyOf_i2_implementation"></a>5.3.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OpenAIGPT

Specific value: `"OpenAIGPT"`

#### <a name="llm_unit_anyOf_i2_model"></a>5.3.2. Property `model`

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

##### <a name="llm_unit_anyOf_i2_model_implementation"></a>5.3.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="llm_unit_anyOf_i2_temperature"></a>5.3.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

#### <a name="llm_unit_anyOf_i2_force_json"></a>5.3.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

#### <a name="llm_unit_anyOf_i2_max_tokens"></a>5.3.5. Property `max_tokens`

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

##### <a name="llm_unit_anyOf_i2_max_tokens_anyOf_i0"></a>5.3.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

##### <a name="llm_unit_anyOf_i2_max_tokens_anyOf_i1"></a>5.3.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="llm_unit_anyOf_i2_connection_handler"></a>5.3.6. Property `connection_handler`

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

##### <a name="llm_unit_anyOf_i2_connection_handler_implementation"></a>5.3.6.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

### <a name="llm_unit_anyOf_i3"></a>5.4. Property `ToolCallLLMWrapper.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./ToolCallLLMWrapper.json                                            |

| Property                                                         | Pattern | Type        | Deprecated | Definition                     | Title/Description                                                    |
| ---------------------------------------------------------------- | ------- | ----------- | ---------- | ------------------------------ | -------------------------------------------------------------------- |
| - [implementation](#llm_unit_anyOf_i3_implementation )           | No      | const       | No         | -                              | ToolCallLLMWrapper                                                   |
| - [tool_message_prompt](#llm_unit_anyOf_i3_tool_message_prompt ) | No      | string      | No         | -                              | Tool Message Prompt                                                  |
| - [llm_unit](#llm_unit_anyOf_i3_llm_unit )                       | No      | object      | No         | Same as [llm_unit](#llm_unit ) | Overview of <class 'eidolon_ai_sdk.apu.llm_unit.LLMUnit'> components |
| - [model](#llm_unit_anyOf_i3_model )                             | No      | Combination | No         | -                              | -                                                                    |

#### <a name="llm_unit_anyOf_i3_implementation"></a>5.4.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ToolCallLLMWrapper

Specific value: `"ToolCallLLMWrapper"`

#### <a name="llm_unit_anyOf_i3_tool_message_prompt"></a>5.4.2. Property `tool_message_prompt`

**Title:** Tool Message Prompt

|              |                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Required** | No                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Default**  | `"You must follow these instructions:\nYou can select zero or more of the above tools based on the user query\nIf there are multiple tools required, make sure a list of tools are returned in a JSON array.\nIf there is no tool that match the user request or you have already answered the question, you will respond with empty json array for the tools.\nYou can also add any additional notes or explanations in the notes field."` |

#### <a name="llm_unit_anyOf_i3_llm_unit"></a>5.4.3. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Same definition as**    | [llm_unit](#llm_unit)                                                     |

**Description:** Overview of <class 'eidolon_ai_sdk.apu.llm_unit.LLMUnit'> components

#### <a name="llm_unit_anyOf_i3_model"></a>5.4.4. Property `model`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                          |
| ------------------------------------------------------- |
| [LLMModel Reference](#llm_unit_anyOf_i3_model_anyOf_i0) |
| [item 1](#llm_unit_anyOf_i3_model_anyOf_i1)             |

##### <a name="llm_unit_anyOf_i3_model_anyOf_i0"></a>5.4.4.1. Property `LLMModel Reference`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.llm_unit.LLMModel"`                                  |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#llm_unit_anyOf_i3_model_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#llm_unit_anyOf_i3_model_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="llm_unit_anyOf_i3_model_anyOf_i0_implementation"></a>5.4.4.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="llm_unit_anyOf_i3_model_anyOf_i1"></a>5.4.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

## <a name="logic_units"></a>6. Property `logic_units`

**Title:** Logic Units

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of object` |
| **Required** | No                |
| **Default**  | `[]`              |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be           | Description |
| ----------------------------------------- | ----------- |
| [LogicUnit Reference](#logic_units_items) | -           |

### <a name="autogenerated_heading_2"></a>6.1. LogicUnit Reference

**Title:** LogicUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.logic_unit.LogicUnit"`                               |

| Property                                               | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------ | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#logic_units_items_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#logic_units_items_additionalProperties )         | No      | object | No         | -          | -                 |

#### <a name="logic_units_items_implementation"></a>6.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

## <a name="audio_unit"></a>7. Property `audio_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                              |
| ------------------------------------------- |
| [AudioUnit Reference](#audio_unit_anyOf_i0) |
| [item 1](#audio_unit_anyOf_i1)              |

### <a name="audio_unit_anyOf_i0"></a>7.1. Property `AudioUnit Reference`

**Title:** AudioUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.audio_unit.AudioUnit"`                               |

| Property                                                 | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#audio_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#audio_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

#### <a name="audio_unit_anyOf_i0_implementation"></a>7.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

### <a name="audio_unit_anyOf_i1"></a>7.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

## <a name="image_unit"></a>8. Property `image_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                              |
| ------------------------------------------- |
| [ImageUnit Reference](#image_unit_anyOf_i0) |
| [item 1](#image_unit_anyOf_i1)              |

### <a name="image_unit_anyOf_i0"></a>8.1. Property `ImageUnit Reference`

**Title:** ImageUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.image_unit.ImageUnit"`                               |

| Property                                                 | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#image_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#image_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

#### <a name="image_unit_anyOf_i0_implementation"></a>8.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

### <a name="image_unit_anyOf_i1"></a>8.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

## <a name="record_conversation"></a>9. Property `record_conversation`

**Title:** Record Conversation

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

## <a name="allow_tool_errors"></a>10. Property `allow_tool_errors`

**Title:** Allow Tool Errors

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

## <a name="document_processor"></a>11. Property `document_processor`

**Title:** DocumentProcessor Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"DocumentProcessor"`                                                     |

| Property                                                | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#document_processor_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#document_processor_additionalProperties )         | No      | object | No         | -          | -                 |

### <a name="document_processor_implementation"></a>11.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

----------------------------------------------------------------------------------------------------------------------------
