---
title: SimpleAgent
description: Description of SimpleAgent component
---

**Description:** The `SimpleAgentSpec` class defines the basic configuration for a SimpleAgent within the Eidolon framework. This
agent is designed to be a flexible, modular component that can interact with various processing units and perform a
range of actions based on its configuration.

| Property                                           | Pattern | Type             | Deprecated | Definition                   | Title/Description                                                                                                                                                                                                                                                                                                                                                                                   |
| -------------------------------------------------- | ------- | ---------------- | ---------- | ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| - [implementation](#implementation )               | No      | const            | No         | -                            | SimpleAgent                                                                                                                                                                                                                                                                                                                                                                                         |
| - [description](#description )                     | No      | Combination      | No         | -                            | Description                                                                                                                                                                                                                                                                                                                                                                                         |
| - [system_prompt](#system_prompt )                 | No      | string           | No         | -                            | System Prompt                                                                                                                                                                                                                                                                                                                                                                                       |
| - [agent_refs](#agent_refs )                       | No      | array of string  | No         | -                            | Agent Refs                                                                                                                                                                                                                                                                                                                                                                                          |
| - [actions](#actions )                             | No      | array            | No         | -                            | Actions                                                                                                                                                                                                                                                                                                                                                                                             |
| - [apu](#apu )                                     | No      | object           | No         | In [APU](/docs/components/apu/overview) | <br />The APU is the main interface for the Agent to interact with the LLM.<br />The APU provides a set of capabilities that encapsulate LLM functionality and creates a clear separation between business logic and the underlying LLM implementation.<br /><br />To learn more, check out our blog article APU: [What is it and how does it work?](https://www.eidolonai.com/what_is_apu/).<br /> |
| - [apus](#apus )                                   | No      | array            | No         | -                            | Apus                                                                                                                                                                                                                                                                                                                                                                                                |
| - [title_generation_mode](#title_generation_mode ) | No      | enum (of string) | No         | -                            | Title Generation Mode                                                                                                                                                                                                                                                                                                                                                                               |
| - [doc_processor](#doc_processor )                 | No      | object           | No         | -                            | DocumentProcessor Reference                                                                                                                                                                                                                                                                                                                                                                         |
| - [](#additionalProperties )                       | No      | object           | No         | -                            | -                                                                                                                                                                                                                                                                                                                                                                                                   |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** SimpleAgent

Specific value: `"SimpleAgent"`

## <a name="description"></a>2. Property `description`

**Title:** Description

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                  |
| ------------------------------- |
| [item 0](#description_anyOf_i0) |
| [item 1](#description_anyOf_i1) |

### <a name="description_anyOf_i0"></a>2.1. Property `item 0`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

### <a name="description_anyOf_i1"></a>2.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

## <a name="system_prompt"></a>3. Property `system_prompt`

**Title:** System Prompt

|              |                                 |
| ------------ | ------------------------------- |
| **Type**     | `string`                        |
| **Required** | No                              |
| **Default**  | `"You are a helpful assistant"` |

## <a name="agent_refs"></a>4. Property `agent_refs`

**Title:** Agent Refs

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of string` |
| **Required** | No                |
| **Default**  | `[]`              |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be       | Description |
| ------------------------------------- | ----------- |
| [agent_refs items](#agent_refs_items) | -           |

### <a name="autogenerated_heading_2"></a>4.1. agent_refs items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

## <a name="actions"></a>5. Property `actions`

**Title:** Actions

|              |                                                                                                                                                                                                                                                                                                   |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `array`                                                                                                                                                                                                                                                                                           |
| **Required** | No                                                                                                                                                                                                                                                                                                |
| **Default**  | `[{"name": "converse", "title": null, "sub_title": null, "description": null, "user_prompt": "{{ body }}", "input_schema": {}, "output_schema": "str", "allow_file_upload": false, "supported_mime_types": [], "allowed_states": ["initialized", "idle", "http_error"], "output_state": "idle"}]` |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be    | Description |
| ---------------------------------- | ----------- |
| [ActionDefinition](#actions_items) | -           |

### <a name="autogenerated_heading_3"></a>5.1. ActionDefinition

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | #/$defs/ActionDefinition                                                  |

| Property                                                       | Pattern | Type            | Deprecated | Definition | Title/Description    |
| -------------------------------------------------------------- | ------- | --------------- | ---------- | ---------- | -------------------- |
| - [name](#actions_items_name )                                 | No      | string          | No         | -          | Name                 |
| - [title](#actions_items_title )                               | No      | Combination     | No         | -          | Title                |
| - [sub_title](#actions_items_sub_title )                       | No      | Combination     | No         | -          | Sub Title            |
| - [description](#actions_items_description )                   | No      | Combination     | No         | -          | Description          |
| - [user_prompt](#actions_items_user_prompt )                   | No      | string          | No         | -          | User Prompt          |
| - [input_schema](#actions_items_input_schema )                 | No      | object          | No         | -          | Input Schema         |
| - [output_schema](#actions_items_output_schema )               | No      | Combination     | No         | -          | Output Schema        |
| - [allow_file_upload](#actions_items_allow_file_upload )       | No      | boolean         | No         | -          | Allow File Upload    |
| - [supported_mime_types](#actions_items_supported_mime_types ) | No      | array of string | No         | -          | Supported Mime Types |
| - [allowed_states](#actions_items_allowed_states )             | No      | array of string | No         | -          | Allowed States       |
| - [output_state](#actions_items_output_state )                 | No      | string          | No         | -          | Output State         |
| - [](#actions_items_additionalProperties )                     | No      | object          | No         | -          | -                    |

#### <a name="actions_items_name"></a>5.1.1. Property `name`

**Title:** Name

|              |              |
| ------------ | ------------ |
| **Type**     | `string`     |
| **Required** | No           |
| **Default**  | `"converse"` |

#### <a name="actions_items_title"></a>5.1.2. Property `title`

**Title:** Title

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                          |
| --------------------------------------- |
| [item 0](#actions_items_title_anyOf_i0) |
| [item 1](#actions_items_title_anyOf_i1) |

##### <a name="actions_items_title_anyOf_i0"></a>5.1.2.1. Property `item 0`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

##### <a name="actions_items_title_anyOf_i1"></a>5.1.2.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="actions_items_sub_title"></a>5.1.3. Property `sub_title`

**Title:** Sub Title

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                              |
| ------------------------------------------- |
| [item 0](#actions_items_sub_title_anyOf_i0) |
| [item 1](#actions_items_sub_title_anyOf_i1) |

##### <a name="actions_items_sub_title_anyOf_i0"></a>5.1.3.1. Property `item 0`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

##### <a name="actions_items_sub_title_anyOf_i1"></a>5.1.3.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="actions_items_description"></a>5.1.4. Property `description`

**Title:** Description

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                |
| --------------------------------------------- |
| [item 0](#actions_items_description_anyOf_i0) |
| [item 1](#actions_items_description_anyOf_i1) |

##### <a name="actions_items_description_anyOf_i0"></a>5.1.4.1. Property `item 0`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

##### <a name="actions_items_description_anyOf_i1"></a>5.1.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="actions_items_user_prompt"></a>5.1.5. Property `user_prompt`

**Title:** User Prompt

|              |                |
| ------------ | -------------- |
| **Type**     | `string`       |
| **Required** | No             |
| **Default**  | `"{{ body }}"` |

#### <a name="actions_items_input_schema"></a>5.1.6. Property `input_schema`

**Title:** Input Schema

|                           |                                                                                                                                      |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| **Type**                  | `object`                                                                                                                             |
| **Required**              | No                                                                                                                                   |
| **Additional properties** | [[Should-conform]](#actions_items_input_schema_additionalProperties "Each additional property must conform to the following schema") |
| **Default**               | `{}`                                                                                                                                 |

| Property                                                | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [](#actions_items_input_schema_additionalProperties ) | No      | object | No         | -          | -                 |

##### <a name="actions_items_input_schema_additionalProperties"></a>5.1.6.1. Property `additionalProperties`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

#### <a name="actions_items_output_schema"></a>5.1.7. Property `output_schema`

**Title:** Output Schema

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"str"`                                                                   |

| Any of(Option)                                  |
| ----------------------------------------------- |
| [item 0](#actions_items_output_schema_anyOf_i0) |
| [item 1](#actions_items_output_schema_anyOf_i1) |

##### <a name="actions_items_output_schema_anyOf_i0"></a>5.1.7.1. Property `item 0`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

Must be one of:
* "str"
Specific value: `"str"`

##### <a name="actions_items_output_schema_anyOf_i1"></a>5.1.7.2. Property `item 1`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

#### <a name="actions_items_allow_file_upload"></a>5.1.8. Property `allow_file_upload`

**Title:** Allow File Upload

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `false`   |

#### <a name="actions_items_supported_mime_types"></a>5.1.9. Property `supported_mime_types`

**Title:** Supported Mime Types

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of string` |
| **Required** | No                |
| **Default**  | `[]`              |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                                         | Description |
| ----------------------------------------------------------------------- | ----------- |
| [supported_mime_types items](#actions_items_supported_mime_types_items) | -           |

##### <a name="autogenerated_heading_4"></a>5.1.9.1. supported_mime_types items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

#### <a name="actions_items_allowed_states"></a>5.1.10. Property `allowed_states`

**Title:** Allowed States

|              |                                         |
| ------------ | --------------------------------------- |
| **Type**     | `array of string`                       |
| **Required** | No                                      |
| **Default**  | `["initialized", "idle", "http_error"]` |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                             | Description |
| ----------------------------------------------------------- | ----------- |
| [allowed_states items](#actions_items_allowed_states_items) | -           |

##### <a name="autogenerated_heading_5"></a>5.1.10.1. allowed_states items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

#### <a name="actions_items_output_state"></a>5.1.11. Property `output_state`

**Title:** Output State

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `"idle"` |

## <a name="apu"></a>6. Property `apu`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"APU"`                                                                   |
| **Defined in**            | [APU](/docs/components/apu/overview)                                                 |

**Description:** 
The APU is the main interface for the Agent to interact with the LLM.
The APU provides a set of capabilities that encapsulate LLM functionality and creates a clear separation between business logic and the underlying LLM implementation.

To learn more, check out our blog article APU: [What is it and how does it work?](https://www.eidolonai.com/what_is_apu/).

| Any of(Option)                          |
| --------------------------------------- |
| [ClaudeHaiku.json](#apu_anyOf_i0)       |
| [ClaudeOpus.json](#apu_anyOf_i1)        |
| [ClaudeSonnet.json](#apu_anyOf_i2)      |
| [ConversationalAPU.json](#apu_anyOf_i3) |
| [GPT3.5-turbo.json](#apu_anyOf_i4)      |
| [GPT4-turbo.json](#apu_anyOf_i5)        |
| [GPT4o.json](#apu_anyOf_i6)             |
| [MistralLarge.json](#apu_anyOf_i7)      |
| [MistralMedium.json](#apu_anyOf_i8)     |
| [MistralSmall.json](#apu_anyOf_i9)      |

### <a name="apu_anyOf_i0"></a>6.1. Property `ClaudeHaiku.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./ClaudeHaiku.json                                                   |

| Property                                                          | Pattern | Type            | Deprecated | Definition                       | Title/Description                                                    |
| ----------------------------------------------------------------- | ------- | --------------- | ---------- | -------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i0_implementation )                 | No      | const           | No         | -                                | ClaudeHaiku                                                          |
| - [max_num_function_calls](#apu_anyOf_i0_max_num_function_calls ) | No      | integer         | No         | -                                | Max Num Function Calls                                               |
| - [io_unit](#apu_anyOf_i0_io_unit )                               | No      | object          | No         | -                                | IOUnit Reference                                                     |
| - [memory_unit](#apu_anyOf_i0_memory_unit )                       | No      | object          | No         | -                                | MemoryUnit Reference                                                 |
| - [llm_unit](#apu_anyOf_i0_llm_unit )                             | No      | object          | No         | In [LLMUnit](/docs/components/llmunit/overview) | Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components |
| - [logic_units](#apu_anyOf_i0_logic_units )                       | No      | array of object | No         | -                                | Logic Units                                                          |
| - [audio_unit](#apu_anyOf_i0_audio_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [image_unit](#apu_anyOf_i0_image_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [record_conversation](#apu_anyOf_i0_record_conversation )       | No      | boolean         | No         | -                                | Record Conversation                                                  |
| - [allow_tool_errors](#apu_anyOf_i0_allow_tool_errors )           | No      | boolean         | No         | -                                | Allow Tool Errors                                                    |
| - [document_processor](#apu_anyOf_i0_document_processor )         | No      | object          | No         | -                                | DocumentProcessor Reference                                          |

#### <a name="apu_anyOf_i0_implementation"></a>6.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ClaudeHaiku

Specific value: `"ClaudeHaiku"`

#### <a name="apu_anyOf_i0_max_num_function_calls"></a>6.1.2. Property `max_num_function_calls`

**Title:** Max Num Function Calls

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `10`      |

**Description:** The maximum number of function calls to make in a single request.

#### <a name="apu_anyOf_i0_io_unit"></a>6.1.3. Property `io_unit`

**Title:** IOUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"IOUnit"`                                                                |

| Property                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_io_unit_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_io_unit_additionalProperties )         | No      | object | No         | -          | -                 |

##### <a name="apu_anyOf_i0_io_unit_implementation"></a>6.1.3.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i0_memory_unit"></a>6.1.4. Property `memory_unit`

**Title:** MemoryUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"MemoryUnit"`                                                            |

| Property                                                      | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_memory_unit_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_memory_unit_additionalProperties )         | No      | object | No         | -          | -                 |

##### <a name="apu_anyOf_i0_memory_unit_implementation"></a>6.1.4.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i0_llm_unit"></a>6.1.5. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Defined in**            | [LLMUnit](/docs/components/llmunit/overview)                                             |

**Description:** Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components

| Any of(Option)                                             |
| ---------------------------------------------------------- |
| [AnthropicLLMUnit.json](#apu_anyOf_i0_llm_unit_anyOf_i0)   |
| [MistralGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i1)         |
| [OpenAIGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i2)          |
| [ToolCallLLMWrapper.json](#apu_anyOf_i0_llm_unit_anyOf_i3) |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i0"></a>6.1.5.1. Property `AnthropicLLMUnit.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./AnthropicLLMUnit.json                                              |

| Property                                                            | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i0_implementation ) | No      | const       | No         | -          | AnthropicLLMUnit   |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i0_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i0_temperature )       | No      | number      | No         | -          | Temperature        |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_args](#apu_anyOf_i0_llm_unit_anyOf_i0_client_args )       | No      | object      | No         | -          | Client Args        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_implementation"></a>6.1.5.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AnthropicLLMUnit

Specific value: `"AnthropicLLMUnit"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model"></a>6.1.5.1.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"claude-3-opus-20240229"`                                                |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i0_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i0_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model_implementation"></a>6.1.5.1.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_temperature"></a>6.1.5.1.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens"></a>6.1.5.1.4. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i0"></a>6.1.5.1.4.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i1"></a>6.1.5.1.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_client_args"></a>6.1.5.1.5. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i1"></a>6.1.5.2. Property `MistralGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./MistralGPT.json                                                    |

| Property                                                            | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i1_implementation ) | No      | const       | No         | -          | MistralGPT         |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i1_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i1_temperature )       | No      | number      | No         | -          | Temperature        |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i1_force_json )         | No      | boolean     | No         | -          | Force Json         |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_args](#apu_anyOf_i0_llm_unit_anyOf_i1_client_args )       | No      | object      | No         | -          | Client Args        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_implementation"></a>6.1.5.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** MistralGPT

Specific value: `"MistralGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model"></a>6.1.5.2.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"mistral-large-latest"`                                                  |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i1_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i1_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model_implementation"></a>6.1.5.2.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_temperature"></a>6.1.5.2.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_force_json"></a>6.1.5.2.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens"></a>6.1.5.2.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i0"></a>6.1.5.2.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i1"></a>6.1.5.2.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_client_args"></a>6.1.5.2.6. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i2"></a>6.1.5.3. Property `OpenAIGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./OpenAIGPT.json                                                     |

| Property                                                                    | Pattern | Type        | Deprecated | Definition | Title/Description                 |
| --------------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | --------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_implementation )         | No      | const       | No         | -          | OpenAIGPT                         |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i2_model )                           | No      | object      | No         | -          | LLMModel Reference                |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i2_temperature )               | No      | number      | No         | -          | Temperature                       |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i2_force_json )                 | No      | boolean     | No         | -          | Force Json                        |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens )                 | No      | Combination | No         | -          | Max Tokens                        |
| - [connection_handler](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler ) | No      | object      | No         | -          | OpenAIConnectionHandler Reference |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_implementation"></a>6.1.5.3.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OpenAIGPT

Specific value: `"OpenAIGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model"></a>6.1.5.3.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"gpt-4-turbo"`                                                           |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i2_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation"></a>6.1.5.3.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_temperature"></a>6.1.5.3.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_force_json"></a>6.1.5.3.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens"></a>6.1.5.3.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i0"></a>6.1.5.3.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i1"></a>6.1.5.3.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler"></a>6.1.5.3.6. Property `connection_handler`

**Title:** OpenAIConnectionHandler Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"OpenAIConnectionHandler"`                                               |

| Property                                                                               | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_implementation"></a>6.1.5.3.6.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i3"></a>6.1.5.4. Property `ToolCallLLMWrapper.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./ToolCallLLMWrapper.json                                            |

| Property                                                                      | Pattern | Type        | Deprecated | Definition                                  | Title/Description                                                    |
| ----------------------------------------------------------------------------- | ------- | ----------- | ---------- | ------------------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_implementation )           | No      | const       | No         | -                                           | ToolCallLLMWrapper                                                   |
| - [tool_message_prompt](#apu_anyOf_i0_llm_unit_anyOf_i3_tool_message_prompt ) | No      | string      | No         | -                                           | Tool Message Prompt                                                  |
| - [llm_unit](#apu_anyOf_i0_llm_unit_anyOf_i3_llm_unit )                       | No      | object      | No         | Same as [llm_unit](#apu_anyOf_i0_llm_unit ) | Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i3_model )                             | No      | Combination | No         | -                                           | -                                                                    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_implementation"></a>6.1.5.4.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ToolCallLLMWrapper

Specific value: `"ToolCallLLMWrapper"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_tool_message_prompt"></a>6.1.5.4.2. Property `tool_message_prompt`

**Title:** Tool Message Prompt

|              |                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Required** | No                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Default**  | `"You must follow these instructions:\nYou can select zero or more of the above tools based on the user query\nIf there are multiple tools required, make sure a list of tools are returned in a JSON array.\nIf there is no tool that match the user request or you have already answered the question, you will respond with empty json array for the tools.\nYou can also add any additional notes or explanations in the notes field."` |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_llm_unit"></a>6.1.5.4.3. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Same definition as**    | [llm_unit](#apu_anyOf_i0_llm_unit)                                        |

**Description:** Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model"></a>6.1.5.4.4. Property `model`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                       |
| -------------------------------------------------------------------- |
| [LLMModel Reference](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i1)             |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0"></a>6.1.5.4.4.1. Property `LLMModel Reference`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.llm_unit.LLMModel"`                                  |

| Property                                                                           | Pattern | Type   | Deprecated | Definition | Title/Description |
| ---------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_implementation"></a>6.1.5.4.4.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i1"></a>6.1.5.4.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i0_logic_units"></a>6.1.6. Property `logic_units`

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

| Each item of this array must be                        | Description |
| ------------------------------------------------------ | ----------- |
| [LogicUnit Reference](#apu_anyOf_i0_logic_units_items) | -           |

##### <a name="autogenerated_heading_6"></a>6.1.6.1. LogicUnit Reference

**Title:** LogicUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.logic_unit.LogicUnit"`                               |

| Property                                                            | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_logic_units_items_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_logic_units_items_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_logic_units_items_implementation"></a>6.1.6.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i0_audio_unit"></a>6.1.7. Property `audio_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                           |
| -------------------------------------------------------- |
| [AudioUnit Reference](#apu_anyOf_i0_audio_unit_anyOf_i0) |
| [item 1](#apu_anyOf_i0_audio_unit_anyOf_i1)              |

##### <a name="apu_anyOf_i0_audio_unit_anyOf_i0"></a>6.1.7.1. Property `AudioUnit Reference`

**Title:** AudioUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.audio_unit.AudioUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_audio_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_audio_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_audio_unit_anyOf_i0_implementation"></a>6.1.7.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i0_audio_unit_anyOf_i1"></a>6.1.7.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i0_image_unit"></a>6.1.8. Property `image_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                           |
| -------------------------------------------------------- |
| [ImageUnit Reference](#apu_anyOf_i0_image_unit_anyOf_i0) |
| [item 1](#apu_anyOf_i0_image_unit_anyOf_i1)              |

##### <a name="apu_anyOf_i0_image_unit_anyOf_i0"></a>6.1.8.1. Property `ImageUnit Reference`

**Title:** ImageUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.image_unit.ImageUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_image_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_image_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_image_unit_anyOf_i0_implementation"></a>6.1.8.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i0_image_unit_anyOf_i1"></a>6.1.8.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i0_record_conversation"></a>6.1.9. Property `record_conversation`

**Title:** Record Conversation

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

#### <a name="apu_anyOf_i0_allow_tool_errors"></a>6.1.10. Property `allow_tool_errors`

**Title:** Allow Tool Errors

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

#### <a name="apu_anyOf_i0_document_processor"></a>6.1.11. Property `document_processor`

**Title:** DocumentProcessor Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"DocumentProcessor"`                                                     |

| Property                                                             | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_document_processor_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_document_processor_additionalProperties )         | No      | object | No         | -          | -                 |

##### <a name="apu_anyOf_i0_document_processor_implementation"></a>6.1.11.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

### <a name="apu_anyOf_i1"></a>6.2. Property `ClaudeOpus.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./ClaudeOpus.json                                                    |

| Property                                                          | Pattern | Type            | Deprecated | Definition                       | Title/Description                                                    |
| ----------------------------------------------------------------- | ------- | --------------- | ---------- | -------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i1_implementation )                 | No      | const           | No         | -                                | ClaudeOpus                                                           |
| - [max_num_function_calls](#apu_anyOf_i1_max_num_function_calls ) | No      | integer         | No         | -                                | Max Num Function Calls                                               |
| - [io_unit](#apu_anyOf_i1_io_unit )                               | No      | object          | No         | -                                | IOUnit Reference                                                     |
| - [memory_unit](#apu_anyOf_i1_memory_unit )                       | No      | object          | No         | -                                | MemoryUnit Reference                                                 |
| - [llm_unit](#apu_anyOf_i1_llm_unit )                             | No      | object          | No         | In [LLMUnit](/docs/components/llmunit/overview) | Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components |
| - [logic_units](#apu_anyOf_i1_logic_units )                       | No      | array of object | No         | -                                | Logic Units                                                          |
| - [audio_unit](#apu_anyOf_i1_audio_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [image_unit](#apu_anyOf_i1_image_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [record_conversation](#apu_anyOf_i1_record_conversation )       | No      | boolean         | No         | -                                | Record Conversation                                                  |
| - [allow_tool_errors](#apu_anyOf_i1_allow_tool_errors )           | No      | boolean         | No         | -                                | Allow Tool Errors                                                    |
| - [document_processor](#apu_anyOf_i1_document_processor )         | No      | object          | No         | -                                | DocumentProcessor Reference                                          |

#### <a name="apu_anyOf_i1_implementation"></a>6.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ClaudeOpus

Specific value: `"ClaudeOpus"`

#### <a name="apu_anyOf_i1_max_num_function_calls"></a>6.2.2. Property `max_num_function_calls`

**Title:** Max Num Function Calls

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `10`      |

**Description:** The maximum number of function calls to make in a single request.

#### <a name="apu_anyOf_i1_io_unit"></a>6.2.3. Property `io_unit`

**Title:** IOUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"IOUnit"`                                                                |

| Property                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i1_io_unit_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i1_io_unit_additionalProperties )         | No      | object | No         | -          | -                 |

##### <a name="apu_anyOf_i1_io_unit_implementation"></a>6.2.3.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i1_memory_unit"></a>6.2.4. Property `memory_unit`

**Title:** MemoryUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"MemoryUnit"`                                                            |

| Property                                                      | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i1_memory_unit_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i1_memory_unit_additionalProperties )         | No      | object | No         | -          | -                 |

##### <a name="apu_anyOf_i1_memory_unit_implementation"></a>6.2.4.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i1_llm_unit"></a>6.2.5. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Defined in**            | [LLMUnit](/docs/components/llmunit/overview)                                             |

**Description:** Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components

| Any of(Option)                                             |
| ---------------------------------------------------------- |
| [AnthropicLLMUnit.json](#apu_anyOf_i0_llm_unit_anyOf_i0)   |
| [MistralGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i1)         |
| [OpenAIGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i2)          |
| [ToolCallLLMWrapper.json](#apu_anyOf_i0_llm_unit_anyOf_i3) |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i0"></a>6.2.5.1. Property `AnthropicLLMUnit.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./AnthropicLLMUnit.json                                              |

| Property                                                            | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i0_implementation ) | No      | const       | No         | -          | AnthropicLLMUnit   |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i0_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i0_temperature )       | No      | number      | No         | -          | Temperature        |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_args](#apu_anyOf_i0_llm_unit_anyOf_i0_client_args )       | No      | object      | No         | -          | Client Args        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_implementation"></a>6.2.5.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AnthropicLLMUnit

Specific value: `"AnthropicLLMUnit"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model"></a>6.2.5.1.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"claude-3-opus-20240229"`                                                |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i0_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i0_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model_implementation"></a>6.2.5.1.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_temperature"></a>6.2.5.1.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens"></a>6.2.5.1.4. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i0"></a>6.2.5.1.4.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i1"></a>6.2.5.1.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_client_args"></a>6.2.5.1.5. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i1"></a>6.2.5.2. Property `MistralGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./MistralGPT.json                                                    |

| Property                                                            | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i1_implementation ) | No      | const       | No         | -          | MistralGPT         |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i1_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i1_temperature )       | No      | number      | No         | -          | Temperature        |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i1_force_json )         | No      | boolean     | No         | -          | Force Json         |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_args](#apu_anyOf_i0_llm_unit_anyOf_i1_client_args )       | No      | object      | No         | -          | Client Args        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_implementation"></a>6.2.5.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** MistralGPT

Specific value: `"MistralGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model"></a>6.2.5.2.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"mistral-large-latest"`                                                  |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i1_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i1_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model_implementation"></a>6.2.5.2.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_temperature"></a>6.2.5.2.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_force_json"></a>6.2.5.2.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens"></a>6.2.5.2.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i0"></a>6.2.5.2.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i1"></a>6.2.5.2.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_client_args"></a>6.2.5.2.6. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i2"></a>6.2.5.3. Property `OpenAIGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./OpenAIGPT.json                                                     |

| Property                                                                    | Pattern | Type        | Deprecated | Definition | Title/Description                 |
| --------------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | --------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_implementation )         | No      | const       | No         | -          | OpenAIGPT                         |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i2_model )                           | No      | object      | No         | -          | LLMModel Reference                |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i2_temperature )               | No      | number      | No         | -          | Temperature                       |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i2_force_json )                 | No      | boolean     | No         | -          | Force Json                        |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens )                 | No      | Combination | No         | -          | Max Tokens                        |
| - [connection_handler](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler ) | No      | object      | No         | -          | OpenAIConnectionHandler Reference |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_implementation"></a>6.2.5.3.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OpenAIGPT

Specific value: `"OpenAIGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model"></a>6.2.5.3.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"gpt-4-turbo"`                                                           |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i2_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation"></a>6.2.5.3.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_temperature"></a>6.2.5.3.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_force_json"></a>6.2.5.3.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens"></a>6.2.5.3.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i0"></a>6.2.5.3.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i1"></a>6.2.5.3.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler"></a>6.2.5.3.6. Property `connection_handler`

**Title:** OpenAIConnectionHandler Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"OpenAIConnectionHandler"`                                               |

| Property                                                                               | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_implementation"></a>6.2.5.3.6.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i3"></a>6.2.5.4. Property `ToolCallLLMWrapper.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./ToolCallLLMWrapper.json                                            |

| Property                                                                      | Pattern | Type        | Deprecated | Definition                                  | Title/Description                                                    |
| ----------------------------------------------------------------------------- | ------- | ----------- | ---------- | ------------------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_implementation )           | No      | const       | No         | -                                           | ToolCallLLMWrapper                                                   |
| - [tool_message_prompt](#apu_anyOf_i0_llm_unit_anyOf_i3_tool_message_prompt ) | No      | string      | No         | -                                           | Tool Message Prompt                                                  |
| - [llm_unit](#apu_anyOf_i0_llm_unit_anyOf_i3_llm_unit )                       | No      | object      | No         | Same as [llm_unit](#apu_anyOf_i0_llm_unit ) | Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i3_model )                             | No      | Combination | No         | -                                           | -                                                                    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_implementation"></a>6.2.5.4.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ToolCallLLMWrapper

Specific value: `"ToolCallLLMWrapper"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_tool_message_prompt"></a>6.2.5.4.2. Property `tool_message_prompt`

**Title:** Tool Message Prompt

|              |                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Required** | No                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Default**  | `"You must follow these instructions:\nYou can select zero or more of the above tools based on the user query\nIf there are multiple tools required, make sure a list of tools are returned in a JSON array.\nIf there is no tool that match the user request or you have already answered the question, you will respond with empty json array for the tools.\nYou can also add any additional notes or explanations in the notes field."` |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_llm_unit"></a>6.2.5.4.3. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Same definition as**    | [llm_unit](#apu_anyOf_i0_llm_unit)                                        |

**Description:** Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model"></a>6.2.5.4.4. Property `model`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                       |
| -------------------------------------------------------------------- |
| [LLMModel Reference](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i1)             |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0"></a>6.2.5.4.4.1. Property `LLMModel Reference`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.llm_unit.LLMModel"`                                  |

| Property                                                                           | Pattern | Type   | Deprecated | Definition | Title/Description |
| ---------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_implementation"></a>6.2.5.4.4.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i1"></a>6.2.5.4.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i1_logic_units"></a>6.2.6. Property `logic_units`

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

| Each item of this array must be                        | Description |
| ------------------------------------------------------ | ----------- |
| [LogicUnit Reference](#apu_anyOf_i1_logic_units_items) | -           |

##### <a name="autogenerated_heading_7"></a>6.2.6.1. LogicUnit Reference

**Title:** LogicUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.logic_unit.LogicUnit"`                               |

| Property                                                            | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i1_logic_units_items_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i1_logic_units_items_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i1_logic_units_items_implementation"></a>6.2.6.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i1_audio_unit"></a>6.2.7. Property `audio_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                           |
| -------------------------------------------------------- |
| [AudioUnit Reference](#apu_anyOf_i1_audio_unit_anyOf_i0) |
| [item 1](#apu_anyOf_i1_audio_unit_anyOf_i1)              |

##### <a name="apu_anyOf_i1_audio_unit_anyOf_i0"></a>6.2.7.1. Property `AudioUnit Reference`

**Title:** AudioUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.audio_unit.AudioUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i1_audio_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i1_audio_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i1_audio_unit_anyOf_i0_implementation"></a>6.2.7.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i1_audio_unit_anyOf_i1"></a>6.2.7.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i1_image_unit"></a>6.2.8. Property `image_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                           |
| -------------------------------------------------------- |
| [ImageUnit Reference](#apu_anyOf_i1_image_unit_anyOf_i0) |
| [item 1](#apu_anyOf_i1_image_unit_anyOf_i1)              |

##### <a name="apu_anyOf_i1_image_unit_anyOf_i0"></a>6.2.8.1. Property `ImageUnit Reference`

**Title:** ImageUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.image_unit.ImageUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i1_image_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i1_image_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i1_image_unit_anyOf_i0_implementation"></a>6.2.8.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i1_image_unit_anyOf_i1"></a>6.2.8.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i1_record_conversation"></a>6.2.9. Property `record_conversation`

**Title:** Record Conversation

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

#### <a name="apu_anyOf_i1_allow_tool_errors"></a>6.2.10. Property `allow_tool_errors`

**Title:** Allow Tool Errors

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

#### <a name="apu_anyOf_i1_document_processor"></a>6.2.11. Property `document_processor`

**Title:** DocumentProcessor Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"DocumentProcessor"`                                                     |

| Property                                                             | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i1_document_processor_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i1_document_processor_additionalProperties )         | No      | object | No         | -          | -                 |

##### <a name="apu_anyOf_i1_document_processor_implementation"></a>6.2.11.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

### <a name="apu_anyOf_i2"></a>6.3. Property `ClaudeSonnet.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./ClaudeSonnet.json                                                  |

| Property                                                          | Pattern | Type            | Deprecated | Definition                       | Title/Description                                                    |
| ----------------------------------------------------------------- | ------- | --------------- | ---------- | -------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i2_implementation )                 | No      | const           | No         | -                                | ClaudeSonnet                                                         |
| - [max_num_function_calls](#apu_anyOf_i2_max_num_function_calls ) | No      | integer         | No         | -                                | Max Num Function Calls                                               |
| - [io_unit](#apu_anyOf_i2_io_unit )                               | No      | object          | No         | -                                | IOUnit Reference                                                     |
| - [memory_unit](#apu_anyOf_i2_memory_unit )                       | No      | object          | No         | -                                | MemoryUnit Reference                                                 |
| - [llm_unit](#apu_anyOf_i2_llm_unit )                             | No      | object          | No         | In [LLMUnit](/docs/components/llmunit/overview) | Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components |
| - [logic_units](#apu_anyOf_i2_logic_units )                       | No      | array of object | No         | -                                | Logic Units                                                          |
| - [audio_unit](#apu_anyOf_i2_audio_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [image_unit](#apu_anyOf_i2_image_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [record_conversation](#apu_anyOf_i2_record_conversation )       | No      | boolean         | No         | -                                | Record Conversation                                                  |
| - [allow_tool_errors](#apu_anyOf_i2_allow_tool_errors )           | No      | boolean         | No         | -                                | Allow Tool Errors                                                    |
| - [document_processor](#apu_anyOf_i2_document_processor )         | No      | object          | No         | -                                | DocumentProcessor Reference                                          |

#### <a name="apu_anyOf_i2_implementation"></a>6.3.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ClaudeSonnet

Specific value: `"ClaudeSonnet"`

#### <a name="apu_anyOf_i2_max_num_function_calls"></a>6.3.2. Property `max_num_function_calls`

**Title:** Max Num Function Calls

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `10`      |

**Description:** The maximum number of function calls to make in a single request.

#### <a name="apu_anyOf_i2_io_unit"></a>6.3.3. Property `io_unit`

**Title:** IOUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"IOUnit"`                                                                |

| Property                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i2_io_unit_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i2_io_unit_additionalProperties )         | No      | object | No         | -          | -                 |

##### <a name="apu_anyOf_i2_io_unit_implementation"></a>6.3.3.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i2_memory_unit"></a>6.3.4. Property `memory_unit`

**Title:** MemoryUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"MemoryUnit"`                                                            |

| Property                                                      | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i2_memory_unit_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i2_memory_unit_additionalProperties )         | No      | object | No         | -          | -                 |

##### <a name="apu_anyOf_i2_memory_unit_implementation"></a>6.3.4.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i2_llm_unit"></a>6.3.5. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Defined in**            | [LLMUnit](/docs/components/llmunit/overview)                                             |

**Description:** Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components

| Any of(Option)                                             |
| ---------------------------------------------------------- |
| [AnthropicLLMUnit.json](#apu_anyOf_i0_llm_unit_anyOf_i0)   |
| [MistralGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i1)         |
| [OpenAIGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i2)          |
| [ToolCallLLMWrapper.json](#apu_anyOf_i0_llm_unit_anyOf_i3) |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i0"></a>6.3.5.1. Property `AnthropicLLMUnit.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./AnthropicLLMUnit.json                                              |

| Property                                                            | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i0_implementation ) | No      | const       | No         | -          | AnthropicLLMUnit   |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i0_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i0_temperature )       | No      | number      | No         | -          | Temperature        |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_args](#apu_anyOf_i0_llm_unit_anyOf_i0_client_args )       | No      | object      | No         | -          | Client Args        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_implementation"></a>6.3.5.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AnthropicLLMUnit

Specific value: `"AnthropicLLMUnit"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model"></a>6.3.5.1.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"claude-3-opus-20240229"`                                                |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i0_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i0_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model_implementation"></a>6.3.5.1.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_temperature"></a>6.3.5.1.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens"></a>6.3.5.1.4. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i0"></a>6.3.5.1.4.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i1"></a>6.3.5.1.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_client_args"></a>6.3.5.1.5. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i1"></a>6.3.5.2. Property `MistralGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./MistralGPT.json                                                    |

| Property                                                            | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i1_implementation ) | No      | const       | No         | -          | MistralGPT         |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i1_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i1_temperature )       | No      | number      | No         | -          | Temperature        |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i1_force_json )         | No      | boolean     | No         | -          | Force Json         |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_args](#apu_anyOf_i0_llm_unit_anyOf_i1_client_args )       | No      | object      | No         | -          | Client Args        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_implementation"></a>6.3.5.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** MistralGPT

Specific value: `"MistralGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model"></a>6.3.5.2.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"mistral-large-latest"`                                                  |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i1_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i1_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model_implementation"></a>6.3.5.2.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_temperature"></a>6.3.5.2.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_force_json"></a>6.3.5.2.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens"></a>6.3.5.2.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i0"></a>6.3.5.2.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i1"></a>6.3.5.2.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_client_args"></a>6.3.5.2.6. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i2"></a>6.3.5.3. Property `OpenAIGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./OpenAIGPT.json                                                     |

| Property                                                                    | Pattern | Type        | Deprecated | Definition | Title/Description                 |
| --------------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | --------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_implementation )         | No      | const       | No         | -          | OpenAIGPT                         |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i2_model )                           | No      | object      | No         | -          | LLMModel Reference                |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i2_temperature )               | No      | number      | No         | -          | Temperature                       |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i2_force_json )                 | No      | boolean     | No         | -          | Force Json                        |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens )                 | No      | Combination | No         | -          | Max Tokens                        |
| - [connection_handler](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler ) | No      | object      | No         | -          | OpenAIConnectionHandler Reference |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_implementation"></a>6.3.5.3.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OpenAIGPT

Specific value: `"OpenAIGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model"></a>6.3.5.3.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"gpt-4-turbo"`                                                           |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i2_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation"></a>6.3.5.3.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_temperature"></a>6.3.5.3.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_force_json"></a>6.3.5.3.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens"></a>6.3.5.3.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i0"></a>6.3.5.3.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i1"></a>6.3.5.3.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler"></a>6.3.5.3.6. Property `connection_handler`

**Title:** OpenAIConnectionHandler Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"OpenAIConnectionHandler"`                                               |

| Property                                                                               | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_implementation"></a>6.3.5.3.6.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i3"></a>6.3.5.4. Property `ToolCallLLMWrapper.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./ToolCallLLMWrapper.json                                            |

| Property                                                                      | Pattern | Type        | Deprecated | Definition                                  | Title/Description                                                    |
| ----------------------------------------------------------------------------- | ------- | ----------- | ---------- | ------------------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_implementation )           | No      | const       | No         | -                                           | ToolCallLLMWrapper                                                   |
| - [tool_message_prompt](#apu_anyOf_i0_llm_unit_anyOf_i3_tool_message_prompt ) | No      | string      | No         | -                                           | Tool Message Prompt                                                  |
| - [llm_unit](#apu_anyOf_i0_llm_unit_anyOf_i3_llm_unit )                       | No      | object      | No         | Same as [llm_unit](#apu_anyOf_i0_llm_unit ) | Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i3_model )                             | No      | Combination | No         | -                                           | -                                                                    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_implementation"></a>6.3.5.4.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ToolCallLLMWrapper

Specific value: `"ToolCallLLMWrapper"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_tool_message_prompt"></a>6.3.5.4.2. Property `tool_message_prompt`

**Title:** Tool Message Prompt

|              |                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Required** | No                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Default**  | `"You must follow these instructions:\nYou can select zero or more of the above tools based on the user query\nIf there are multiple tools required, make sure a list of tools are returned in a JSON array.\nIf there is no tool that match the user request or you have already answered the question, you will respond with empty json array for the tools.\nYou can also add any additional notes or explanations in the notes field."` |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_llm_unit"></a>6.3.5.4.3. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Same definition as**    | [llm_unit](#apu_anyOf_i0_llm_unit)                                        |

**Description:** Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model"></a>6.3.5.4.4. Property `model`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                       |
| -------------------------------------------------------------------- |
| [LLMModel Reference](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i1)             |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0"></a>6.3.5.4.4.1. Property `LLMModel Reference`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.llm_unit.LLMModel"`                                  |

| Property                                                                           | Pattern | Type   | Deprecated | Definition | Title/Description |
| ---------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_implementation"></a>6.3.5.4.4.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i1"></a>6.3.5.4.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i2_logic_units"></a>6.3.6. Property `logic_units`

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

| Each item of this array must be                        | Description |
| ------------------------------------------------------ | ----------- |
| [LogicUnit Reference](#apu_anyOf_i2_logic_units_items) | -           |

##### <a name="autogenerated_heading_8"></a>6.3.6.1. LogicUnit Reference

**Title:** LogicUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.logic_unit.LogicUnit"`                               |

| Property                                                            | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i2_logic_units_items_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i2_logic_units_items_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i2_logic_units_items_implementation"></a>6.3.6.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i2_audio_unit"></a>6.3.7. Property `audio_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                           |
| -------------------------------------------------------- |
| [AudioUnit Reference](#apu_anyOf_i2_audio_unit_anyOf_i0) |
| [item 1](#apu_anyOf_i2_audio_unit_anyOf_i1)              |

##### <a name="apu_anyOf_i2_audio_unit_anyOf_i0"></a>6.3.7.1. Property `AudioUnit Reference`

**Title:** AudioUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.audio_unit.AudioUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i2_audio_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i2_audio_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i2_audio_unit_anyOf_i0_implementation"></a>6.3.7.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i2_audio_unit_anyOf_i1"></a>6.3.7.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i2_image_unit"></a>6.3.8. Property `image_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                           |
| -------------------------------------------------------- |
| [ImageUnit Reference](#apu_anyOf_i2_image_unit_anyOf_i0) |
| [item 1](#apu_anyOf_i2_image_unit_anyOf_i1)              |

##### <a name="apu_anyOf_i2_image_unit_anyOf_i0"></a>6.3.8.1. Property `ImageUnit Reference`

**Title:** ImageUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.image_unit.ImageUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i2_image_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i2_image_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i2_image_unit_anyOf_i0_implementation"></a>6.3.8.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i2_image_unit_anyOf_i1"></a>6.3.8.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i2_record_conversation"></a>6.3.9. Property `record_conversation`

**Title:** Record Conversation

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

#### <a name="apu_anyOf_i2_allow_tool_errors"></a>6.3.10. Property `allow_tool_errors`

**Title:** Allow Tool Errors

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

#### <a name="apu_anyOf_i2_document_processor"></a>6.3.11. Property `document_processor`

**Title:** DocumentProcessor Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"DocumentProcessor"`                                                     |

| Property                                                             | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i2_document_processor_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i2_document_processor_additionalProperties )         | No      | object | No         | -          | -                 |

##### <a name="apu_anyOf_i2_document_processor_implementation"></a>6.3.11.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

### <a name="apu_anyOf_i3"></a>6.4. Property `ConversationalAPU.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./ConversationalAPU.json                                             |

| Property                                                          | Pattern | Type            | Deprecated | Definition                       | Title/Description                                                    |
| ----------------------------------------------------------------- | ------- | --------------- | ---------- | -------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i3_implementation )                 | No      | const           | No         | -                                | ConversationalAPU                                                    |
| - [max_num_function_calls](#apu_anyOf_i3_max_num_function_calls ) | No      | integer         | No         | -                                | Max Num Function Calls                                               |
| - [io_unit](#apu_anyOf_i3_io_unit )                               | No      | object          | No         | -                                | IOUnit Reference                                                     |
| - [memory_unit](#apu_anyOf_i3_memory_unit )                       | No      | object          | No         | -                                | MemoryUnit Reference                                                 |
| - [llm_unit](#apu_anyOf_i3_llm_unit )                             | No      | object          | No         | In [LLMUnit](/docs/components/llmunit/overview) | Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components |
| - [logic_units](#apu_anyOf_i3_logic_units )                       | No      | array of object | No         | -                                | Logic Units                                                          |
| - [audio_unit](#apu_anyOf_i3_audio_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [image_unit](#apu_anyOf_i3_image_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [record_conversation](#apu_anyOf_i3_record_conversation )       | No      | boolean         | No         | -                                | Record Conversation                                                  |
| - [allow_tool_errors](#apu_anyOf_i3_allow_tool_errors )           | No      | boolean         | No         | -                                | Allow Tool Errors                                                    |
| - [document_processor](#apu_anyOf_i3_document_processor )         | No      | object          | No         | -                                | DocumentProcessor Reference                                          |

#### <a name="apu_anyOf_i3_implementation"></a>6.4.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ConversationalAPU

Specific value: `"ConversationalAPU"`

#### <a name="apu_anyOf_i3_max_num_function_calls"></a>6.4.2. Property `max_num_function_calls`

**Title:** Max Num Function Calls

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `10`      |

**Description:** The maximum number of function calls to make in a single request.

#### <a name="apu_anyOf_i3_io_unit"></a>6.4.3. Property `io_unit`

**Title:** IOUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"IOUnit"`                                                                |

| Property                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i3_io_unit_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i3_io_unit_additionalProperties )         | No      | object | No         | -          | -                 |

##### <a name="apu_anyOf_i3_io_unit_implementation"></a>6.4.3.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i3_memory_unit"></a>6.4.4. Property `memory_unit`

**Title:** MemoryUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"MemoryUnit"`                                                            |

| Property                                                      | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i3_memory_unit_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i3_memory_unit_additionalProperties )         | No      | object | No         | -          | -                 |

##### <a name="apu_anyOf_i3_memory_unit_implementation"></a>6.4.4.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i3_llm_unit"></a>6.4.5. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Defined in**            | [LLMUnit](/docs/components/llmunit/overview)                                             |

**Description:** Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components

| Any of(Option)                                             |
| ---------------------------------------------------------- |
| [AnthropicLLMUnit.json](#apu_anyOf_i0_llm_unit_anyOf_i0)   |
| [MistralGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i1)         |
| [OpenAIGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i2)          |
| [ToolCallLLMWrapper.json](#apu_anyOf_i0_llm_unit_anyOf_i3) |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i0"></a>6.4.5.1. Property `AnthropicLLMUnit.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./AnthropicLLMUnit.json                                              |

| Property                                                            | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i0_implementation ) | No      | const       | No         | -          | AnthropicLLMUnit   |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i0_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i0_temperature )       | No      | number      | No         | -          | Temperature        |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_args](#apu_anyOf_i0_llm_unit_anyOf_i0_client_args )       | No      | object      | No         | -          | Client Args        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_implementation"></a>6.4.5.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AnthropicLLMUnit

Specific value: `"AnthropicLLMUnit"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model"></a>6.4.5.1.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"claude-3-opus-20240229"`                                                |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i0_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i0_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model_implementation"></a>6.4.5.1.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_temperature"></a>6.4.5.1.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens"></a>6.4.5.1.4. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i0"></a>6.4.5.1.4.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i1"></a>6.4.5.1.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_client_args"></a>6.4.5.1.5. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i1"></a>6.4.5.2. Property `MistralGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./MistralGPT.json                                                    |

| Property                                                            | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i1_implementation ) | No      | const       | No         | -          | MistralGPT         |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i1_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i1_temperature )       | No      | number      | No         | -          | Temperature        |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i1_force_json )         | No      | boolean     | No         | -          | Force Json         |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_args](#apu_anyOf_i0_llm_unit_anyOf_i1_client_args )       | No      | object      | No         | -          | Client Args        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_implementation"></a>6.4.5.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** MistralGPT

Specific value: `"MistralGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model"></a>6.4.5.2.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"mistral-large-latest"`                                                  |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i1_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i1_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model_implementation"></a>6.4.5.2.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_temperature"></a>6.4.5.2.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_force_json"></a>6.4.5.2.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens"></a>6.4.5.2.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i0"></a>6.4.5.2.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i1"></a>6.4.5.2.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_client_args"></a>6.4.5.2.6. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i2"></a>6.4.5.3. Property `OpenAIGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./OpenAIGPT.json                                                     |

| Property                                                                    | Pattern | Type        | Deprecated | Definition | Title/Description                 |
| --------------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | --------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_implementation )         | No      | const       | No         | -          | OpenAIGPT                         |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i2_model )                           | No      | object      | No         | -          | LLMModel Reference                |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i2_temperature )               | No      | number      | No         | -          | Temperature                       |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i2_force_json )                 | No      | boolean     | No         | -          | Force Json                        |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens )                 | No      | Combination | No         | -          | Max Tokens                        |
| - [connection_handler](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler ) | No      | object      | No         | -          | OpenAIConnectionHandler Reference |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_implementation"></a>6.4.5.3.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OpenAIGPT

Specific value: `"OpenAIGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model"></a>6.4.5.3.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"gpt-4-turbo"`                                                           |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i2_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation"></a>6.4.5.3.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_temperature"></a>6.4.5.3.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_force_json"></a>6.4.5.3.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens"></a>6.4.5.3.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i0"></a>6.4.5.3.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i1"></a>6.4.5.3.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler"></a>6.4.5.3.6. Property `connection_handler`

**Title:** OpenAIConnectionHandler Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"OpenAIConnectionHandler"`                                               |

| Property                                                                               | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_implementation"></a>6.4.5.3.6.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i3"></a>6.4.5.4. Property `ToolCallLLMWrapper.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./ToolCallLLMWrapper.json                                            |

| Property                                                                      | Pattern | Type        | Deprecated | Definition                                  | Title/Description                                                    |
| ----------------------------------------------------------------------------- | ------- | ----------- | ---------- | ------------------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_implementation )           | No      | const       | No         | -                                           | ToolCallLLMWrapper                                                   |
| - [tool_message_prompt](#apu_anyOf_i0_llm_unit_anyOf_i3_tool_message_prompt ) | No      | string      | No         | -                                           | Tool Message Prompt                                                  |
| - [llm_unit](#apu_anyOf_i0_llm_unit_anyOf_i3_llm_unit )                       | No      | object      | No         | Same as [llm_unit](#apu_anyOf_i0_llm_unit ) | Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i3_model )                             | No      | Combination | No         | -                                           | -                                                                    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_implementation"></a>6.4.5.4.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ToolCallLLMWrapper

Specific value: `"ToolCallLLMWrapper"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_tool_message_prompt"></a>6.4.5.4.2. Property `tool_message_prompt`

**Title:** Tool Message Prompt

|              |                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Required** | No                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Default**  | `"You must follow these instructions:\nYou can select zero or more of the above tools based on the user query\nIf there are multiple tools required, make sure a list of tools are returned in a JSON array.\nIf there is no tool that match the user request or you have already answered the question, you will respond with empty json array for the tools.\nYou can also add any additional notes or explanations in the notes field."` |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_llm_unit"></a>6.4.5.4.3. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Same definition as**    | [llm_unit](#apu_anyOf_i0_llm_unit)                                        |

**Description:** Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model"></a>6.4.5.4.4. Property `model`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                       |
| -------------------------------------------------------------------- |
| [LLMModel Reference](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i1)             |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0"></a>6.4.5.4.4.1. Property `LLMModel Reference`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.llm_unit.LLMModel"`                                  |

| Property                                                                           | Pattern | Type   | Deprecated | Definition | Title/Description |
| ---------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_implementation"></a>6.4.5.4.4.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i1"></a>6.4.5.4.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i3_logic_units"></a>6.4.6. Property `logic_units`

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

| Each item of this array must be                        | Description |
| ------------------------------------------------------ | ----------- |
| [LogicUnit Reference](#apu_anyOf_i3_logic_units_items) | -           |

##### <a name="autogenerated_heading_9"></a>6.4.6.1. LogicUnit Reference

**Title:** LogicUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.logic_unit.LogicUnit"`                               |

| Property                                                            | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i3_logic_units_items_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i3_logic_units_items_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i3_logic_units_items_implementation"></a>6.4.6.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i3_audio_unit"></a>6.4.7. Property `audio_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                           |
| -------------------------------------------------------- |
| [AudioUnit Reference](#apu_anyOf_i3_audio_unit_anyOf_i0) |
| [item 1](#apu_anyOf_i3_audio_unit_anyOf_i1)              |

##### <a name="apu_anyOf_i3_audio_unit_anyOf_i0"></a>6.4.7.1. Property `AudioUnit Reference`

**Title:** AudioUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.audio_unit.AudioUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i3_audio_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i3_audio_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i3_audio_unit_anyOf_i0_implementation"></a>6.4.7.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i3_audio_unit_anyOf_i1"></a>6.4.7.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i3_image_unit"></a>6.4.8. Property `image_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                           |
| -------------------------------------------------------- |
| [ImageUnit Reference](#apu_anyOf_i3_image_unit_anyOf_i0) |
| [item 1](#apu_anyOf_i3_image_unit_anyOf_i1)              |

##### <a name="apu_anyOf_i3_image_unit_anyOf_i0"></a>6.4.8.1. Property `ImageUnit Reference`

**Title:** ImageUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.image_unit.ImageUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i3_image_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i3_image_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i3_image_unit_anyOf_i0_implementation"></a>6.4.8.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i3_image_unit_anyOf_i1"></a>6.4.8.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i3_record_conversation"></a>6.4.9. Property `record_conversation`

**Title:** Record Conversation

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

#### <a name="apu_anyOf_i3_allow_tool_errors"></a>6.4.10. Property `allow_tool_errors`

**Title:** Allow Tool Errors

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

#### <a name="apu_anyOf_i3_document_processor"></a>6.4.11. Property `document_processor`

**Title:** DocumentProcessor Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"DocumentProcessor"`                                                     |

| Property                                                             | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i3_document_processor_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i3_document_processor_additionalProperties )         | No      | object | No         | -          | -                 |

##### <a name="apu_anyOf_i3_document_processor_implementation"></a>6.4.11.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

### <a name="apu_anyOf_i4"></a>6.5. Property `GPT3.5-turbo.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./GPT3.5-turbo.json                                                  |

| Property                                                          | Pattern | Type            | Deprecated | Definition                       | Title/Description                                                    |
| ----------------------------------------------------------------- | ------- | --------------- | ---------- | -------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i4_implementation )                 | No      | const           | No         | -                                | GPT3.5-turbo                                                         |
| - [max_num_function_calls](#apu_anyOf_i4_max_num_function_calls ) | No      | integer         | No         | -                                | Max Num Function Calls                                               |
| - [io_unit](#apu_anyOf_i4_io_unit )                               | No      | object          | No         | -                                | IOUnit Reference                                                     |
| - [memory_unit](#apu_anyOf_i4_memory_unit )                       | No      | object          | No         | -                                | MemoryUnit Reference                                                 |
| - [llm_unit](#apu_anyOf_i4_llm_unit )                             | No      | object          | No         | In [LLMUnit](/docs/components/llmunit/overview) | Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components |
| - [logic_units](#apu_anyOf_i4_logic_units )                       | No      | array of object | No         | -                                | Logic Units                                                          |
| - [audio_unit](#apu_anyOf_i4_audio_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [image_unit](#apu_anyOf_i4_image_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [record_conversation](#apu_anyOf_i4_record_conversation )       | No      | boolean         | No         | -                                | Record Conversation                                                  |
| - [allow_tool_errors](#apu_anyOf_i4_allow_tool_errors )           | No      | boolean         | No         | -                                | Allow Tool Errors                                                    |
| - [document_processor](#apu_anyOf_i4_document_processor )         | No      | object          | No         | -                                | DocumentProcessor Reference                                          |

#### <a name="apu_anyOf_i4_implementation"></a>6.5.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** GPT3.5-turbo

Specific value: `"GPT3.5-turbo"`

#### <a name="apu_anyOf_i4_max_num_function_calls"></a>6.5.2. Property `max_num_function_calls`

**Title:** Max Num Function Calls

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `10`      |

**Description:** The maximum number of function calls to make in a single request.

#### <a name="apu_anyOf_i4_io_unit"></a>6.5.3. Property `io_unit`

**Title:** IOUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"IOUnit"`                                                                |

| Property                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i4_io_unit_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i4_io_unit_additionalProperties )         | No      | object | No         | -          | -                 |

##### <a name="apu_anyOf_i4_io_unit_implementation"></a>6.5.3.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i4_memory_unit"></a>6.5.4. Property `memory_unit`

**Title:** MemoryUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"MemoryUnit"`                                                            |

| Property                                                      | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i4_memory_unit_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i4_memory_unit_additionalProperties )         | No      | object | No         | -          | -                 |

##### <a name="apu_anyOf_i4_memory_unit_implementation"></a>6.5.4.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i4_llm_unit"></a>6.5.5. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Defined in**            | [LLMUnit](/docs/components/llmunit/overview)                                             |

**Description:** Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components

| Any of(Option)                                             |
| ---------------------------------------------------------- |
| [AnthropicLLMUnit.json](#apu_anyOf_i0_llm_unit_anyOf_i0)   |
| [MistralGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i1)         |
| [OpenAIGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i2)          |
| [ToolCallLLMWrapper.json](#apu_anyOf_i0_llm_unit_anyOf_i3) |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i0"></a>6.5.5.1. Property `AnthropicLLMUnit.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./AnthropicLLMUnit.json                                              |

| Property                                                            | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i0_implementation ) | No      | const       | No         | -          | AnthropicLLMUnit   |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i0_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i0_temperature )       | No      | number      | No         | -          | Temperature        |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_args](#apu_anyOf_i0_llm_unit_anyOf_i0_client_args )       | No      | object      | No         | -          | Client Args        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_implementation"></a>6.5.5.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AnthropicLLMUnit

Specific value: `"AnthropicLLMUnit"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model"></a>6.5.5.1.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"claude-3-opus-20240229"`                                                |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i0_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i0_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model_implementation"></a>6.5.5.1.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_temperature"></a>6.5.5.1.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens"></a>6.5.5.1.4. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i0"></a>6.5.5.1.4.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i1"></a>6.5.5.1.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_client_args"></a>6.5.5.1.5. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i1"></a>6.5.5.2. Property `MistralGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./MistralGPT.json                                                    |

| Property                                                            | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i1_implementation ) | No      | const       | No         | -          | MistralGPT         |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i1_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i1_temperature )       | No      | number      | No         | -          | Temperature        |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i1_force_json )         | No      | boolean     | No         | -          | Force Json         |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_args](#apu_anyOf_i0_llm_unit_anyOf_i1_client_args )       | No      | object      | No         | -          | Client Args        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_implementation"></a>6.5.5.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** MistralGPT

Specific value: `"MistralGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model"></a>6.5.5.2.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"mistral-large-latest"`                                                  |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i1_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i1_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model_implementation"></a>6.5.5.2.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_temperature"></a>6.5.5.2.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_force_json"></a>6.5.5.2.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens"></a>6.5.5.2.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i0"></a>6.5.5.2.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i1"></a>6.5.5.2.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_client_args"></a>6.5.5.2.6. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i2"></a>6.5.5.3. Property `OpenAIGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./OpenAIGPT.json                                                     |

| Property                                                                    | Pattern | Type        | Deprecated | Definition | Title/Description                 |
| --------------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | --------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_implementation )         | No      | const       | No         | -          | OpenAIGPT                         |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i2_model )                           | No      | object      | No         | -          | LLMModel Reference                |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i2_temperature )               | No      | number      | No         | -          | Temperature                       |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i2_force_json )                 | No      | boolean     | No         | -          | Force Json                        |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens )                 | No      | Combination | No         | -          | Max Tokens                        |
| - [connection_handler](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler ) | No      | object      | No         | -          | OpenAIConnectionHandler Reference |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_implementation"></a>6.5.5.3.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OpenAIGPT

Specific value: `"OpenAIGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model"></a>6.5.5.3.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"gpt-4-turbo"`                                                           |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i2_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation"></a>6.5.5.3.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_temperature"></a>6.5.5.3.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_force_json"></a>6.5.5.3.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens"></a>6.5.5.3.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i0"></a>6.5.5.3.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i1"></a>6.5.5.3.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler"></a>6.5.5.3.6. Property `connection_handler`

**Title:** OpenAIConnectionHandler Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"OpenAIConnectionHandler"`                                               |

| Property                                                                               | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_implementation"></a>6.5.5.3.6.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i3"></a>6.5.5.4. Property `ToolCallLLMWrapper.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./ToolCallLLMWrapper.json                                            |

| Property                                                                      | Pattern | Type        | Deprecated | Definition                                  | Title/Description                                                    |
| ----------------------------------------------------------------------------- | ------- | ----------- | ---------- | ------------------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_implementation )           | No      | const       | No         | -                                           | ToolCallLLMWrapper                                                   |
| - [tool_message_prompt](#apu_anyOf_i0_llm_unit_anyOf_i3_tool_message_prompt ) | No      | string      | No         | -                                           | Tool Message Prompt                                                  |
| - [llm_unit](#apu_anyOf_i0_llm_unit_anyOf_i3_llm_unit )                       | No      | object      | No         | Same as [llm_unit](#apu_anyOf_i0_llm_unit ) | Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i3_model )                             | No      | Combination | No         | -                                           | -                                                                    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_implementation"></a>6.5.5.4.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ToolCallLLMWrapper

Specific value: `"ToolCallLLMWrapper"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_tool_message_prompt"></a>6.5.5.4.2. Property `tool_message_prompt`

**Title:** Tool Message Prompt

|              |                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Required** | No                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Default**  | `"You must follow these instructions:\nYou can select zero or more of the above tools based on the user query\nIf there are multiple tools required, make sure a list of tools are returned in a JSON array.\nIf there is no tool that match the user request or you have already answered the question, you will respond with empty json array for the tools.\nYou can also add any additional notes or explanations in the notes field."` |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_llm_unit"></a>6.5.5.4.3. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Same definition as**    | [llm_unit](#apu_anyOf_i0_llm_unit)                                        |

**Description:** Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model"></a>6.5.5.4.4. Property `model`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                       |
| -------------------------------------------------------------------- |
| [LLMModel Reference](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i1)             |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0"></a>6.5.5.4.4.1. Property `LLMModel Reference`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.llm_unit.LLMModel"`                                  |

| Property                                                                           | Pattern | Type   | Deprecated | Definition | Title/Description |
| ---------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_implementation"></a>6.5.5.4.4.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i1"></a>6.5.5.4.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i4_logic_units"></a>6.5.6. Property `logic_units`

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

| Each item of this array must be                        | Description |
| ------------------------------------------------------ | ----------- |
| [LogicUnit Reference](#apu_anyOf_i4_logic_units_items) | -           |

##### <a name="autogenerated_heading_10"></a>6.5.6.1. LogicUnit Reference

**Title:** LogicUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.logic_unit.LogicUnit"`                               |

| Property                                                            | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i4_logic_units_items_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i4_logic_units_items_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i4_logic_units_items_implementation"></a>6.5.6.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i4_audio_unit"></a>6.5.7. Property `audio_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                           |
| -------------------------------------------------------- |
| [AudioUnit Reference](#apu_anyOf_i4_audio_unit_anyOf_i0) |
| [item 1](#apu_anyOf_i4_audio_unit_anyOf_i1)              |

##### <a name="apu_anyOf_i4_audio_unit_anyOf_i0"></a>6.5.7.1. Property `AudioUnit Reference`

**Title:** AudioUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.audio_unit.AudioUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i4_audio_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i4_audio_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i4_audio_unit_anyOf_i0_implementation"></a>6.5.7.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i4_audio_unit_anyOf_i1"></a>6.5.7.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i4_image_unit"></a>6.5.8. Property `image_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                           |
| -------------------------------------------------------- |
| [ImageUnit Reference](#apu_anyOf_i4_image_unit_anyOf_i0) |
| [item 1](#apu_anyOf_i4_image_unit_anyOf_i1)              |

##### <a name="apu_anyOf_i4_image_unit_anyOf_i0"></a>6.5.8.1. Property `ImageUnit Reference`

**Title:** ImageUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.image_unit.ImageUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i4_image_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i4_image_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i4_image_unit_anyOf_i0_implementation"></a>6.5.8.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i4_image_unit_anyOf_i1"></a>6.5.8.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i4_record_conversation"></a>6.5.9. Property `record_conversation`

**Title:** Record Conversation

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

#### <a name="apu_anyOf_i4_allow_tool_errors"></a>6.5.10. Property `allow_tool_errors`

**Title:** Allow Tool Errors

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

#### <a name="apu_anyOf_i4_document_processor"></a>6.5.11. Property `document_processor`

**Title:** DocumentProcessor Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"DocumentProcessor"`                                                     |

| Property                                                             | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i4_document_processor_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i4_document_processor_additionalProperties )         | No      | object | No         | -          | -                 |

##### <a name="apu_anyOf_i4_document_processor_implementation"></a>6.5.11.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

### <a name="apu_anyOf_i5"></a>6.6. Property `GPT4-turbo.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./GPT4-turbo.json                                                    |

| Property                                                          | Pattern | Type            | Deprecated | Definition                       | Title/Description                                                    |
| ----------------------------------------------------------------- | ------- | --------------- | ---------- | -------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i5_implementation )                 | No      | const           | No         | -                                | GPT4-turbo                                                           |
| - [max_num_function_calls](#apu_anyOf_i5_max_num_function_calls ) | No      | integer         | No         | -                                | Max Num Function Calls                                               |
| - [io_unit](#apu_anyOf_i5_io_unit )                               | No      | object          | No         | -                                | IOUnit Reference                                                     |
| - [memory_unit](#apu_anyOf_i5_memory_unit )                       | No      | object          | No         | -                                | MemoryUnit Reference                                                 |
| - [llm_unit](#apu_anyOf_i5_llm_unit )                             | No      | object          | No         | In [LLMUnit](/docs/components/llmunit/overview) | Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components |
| - [logic_units](#apu_anyOf_i5_logic_units )                       | No      | array of object | No         | -                                | Logic Units                                                          |
| - [audio_unit](#apu_anyOf_i5_audio_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [image_unit](#apu_anyOf_i5_image_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [record_conversation](#apu_anyOf_i5_record_conversation )       | No      | boolean         | No         | -                                | Record Conversation                                                  |
| - [allow_tool_errors](#apu_anyOf_i5_allow_tool_errors )           | No      | boolean         | No         | -                                | Allow Tool Errors                                                    |
| - [document_processor](#apu_anyOf_i5_document_processor )         | No      | object          | No         | -                                | DocumentProcessor Reference                                          |

#### <a name="apu_anyOf_i5_implementation"></a>6.6.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** GPT4-turbo

Specific value: `"GPT4-turbo"`

#### <a name="apu_anyOf_i5_max_num_function_calls"></a>6.6.2. Property `max_num_function_calls`

**Title:** Max Num Function Calls

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `10`      |

**Description:** The maximum number of function calls to make in a single request.

#### <a name="apu_anyOf_i5_io_unit"></a>6.6.3. Property `io_unit`

**Title:** IOUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"IOUnit"`                                                                |

| Property                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i5_io_unit_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i5_io_unit_additionalProperties )         | No      | object | No         | -          | -                 |

##### <a name="apu_anyOf_i5_io_unit_implementation"></a>6.6.3.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i5_memory_unit"></a>6.6.4. Property `memory_unit`

**Title:** MemoryUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"MemoryUnit"`                                                            |

| Property                                                      | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i5_memory_unit_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i5_memory_unit_additionalProperties )         | No      | object | No         | -          | -                 |

##### <a name="apu_anyOf_i5_memory_unit_implementation"></a>6.6.4.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i5_llm_unit"></a>6.6.5. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Defined in**            | [LLMUnit](/docs/components/llmunit/overview)                                             |

**Description:** Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components

| Any of(Option)                                             |
| ---------------------------------------------------------- |
| [AnthropicLLMUnit.json](#apu_anyOf_i0_llm_unit_anyOf_i0)   |
| [MistralGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i1)         |
| [OpenAIGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i2)          |
| [ToolCallLLMWrapper.json](#apu_anyOf_i0_llm_unit_anyOf_i3) |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i0"></a>6.6.5.1. Property `AnthropicLLMUnit.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./AnthropicLLMUnit.json                                              |

| Property                                                            | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i0_implementation ) | No      | const       | No         | -          | AnthropicLLMUnit   |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i0_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i0_temperature )       | No      | number      | No         | -          | Temperature        |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_args](#apu_anyOf_i0_llm_unit_anyOf_i0_client_args )       | No      | object      | No         | -          | Client Args        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_implementation"></a>6.6.5.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AnthropicLLMUnit

Specific value: `"AnthropicLLMUnit"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model"></a>6.6.5.1.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"claude-3-opus-20240229"`                                                |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i0_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i0_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model_implementation"></a>6.6.5.1.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_temperature"></a>6.6.5.1.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens"></a>6.6.5.1.4. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i0"></a>6.6.5.1.4.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i1"></a>6.6.5.1.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_client_args"></a>6.6.5.1.5. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i1"></a>6.6.5.2. Property `MistralGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./MistralGPT.json                                                    |

| Property                                                            | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i1_implementation ) | No      | const       | No         | -          | MistralGPT         |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i1_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i1_temperature )       | No      | number      | No         | -          | Temperature        |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i1_force_json )         | No      | boolean     | No         | -          | Force Json         |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_args](#apu_anyOf_i0_llm_unit_anyOf_i1_client_args )       | No      | object      | No         | -          | Client Args        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_implementation"></a>6.6.5.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** MistralGPT

Specific value: `"MistralGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model"></a>6.6.5.2.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"mistral-large-latest"`                                                  |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i1_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i1_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model_implementation"></a>6.6.5.2.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_temperature"></a>6.6.5.2.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_force_json"></a>6.6.5.2.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens"></a>6.6.5.2.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i0"></a>6.6.5.2.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i1"></a>6.6.5.2.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_client_args"></a>6.6.5.2.6. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i2"></a>6.6.5.3. Property `OpenAIGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./OpenAIGPT.json                                                     |

| Property                                                                    | Pattern | Type        | Deprecated | Definition | Title/Description                 |
| --------------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | --------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_implementation )         | No      | const       | No         | -          | OpenAIGPT                         |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i2_model )                           | No      | object      | No         | -          | LLMModel Reference                |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i2_temperature )               | No      | number      | No         | -          | Temperature                       |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i2_force_json )                 | No      | boolean     | No         | -          | Force Json                        |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens )                 | No      | Combination | No         | -          | Max Tokens                        |
| - [connection_handler](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler ) | No      | object      | No         | -          | OpenAIConnectionHandler Reference |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_implementation"></a>6.6.5.3.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OpenAIGPT

Specific value: `"OpenAIGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model"></a>6.6.5.3.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"gpt-4-turbo"`                                                           |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i2_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation"></a>6.6.5.3.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_temperature"></a>6.6.5.3.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_force_json"></a>6.6.5.3.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens"></a>6.6.5.3.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i0"></a>6.6.5.3.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i1"></a>6.6.5.3.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler"></a>6.6.5.3.6. Property `connection_handler`

**Title:** OpenAIConnectionHandler Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"OpenAIConnectionHandler"`                                               |

| Property                                                                               | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_implementation"></a>6.6.5.3.6.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i3"></a>6.6.5.4. Property `ToolCallLLMWrapper.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./ToolCallLLMWrapper.json                                            |

| Property                                                                      | Pattern | Type        | Deprecated | Definition                                  | Title/Description                                                    |
| ----------------------------------------------------------------------------- | ------- | ----------- | ---------- | ------------------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_implementation )           | No      | const       | No         | -                                           | ToolCallLLMWrapper                                                   |
| - [tool_message_prompt](#apu_anyOf_i0_llm_unit_anyOf_i3_tool_message_prompt ) | No      | string      | No         | -                                           | Tool Message Prompt                                                  |
| - [llm_unit](#apu_anyOf_i0_llm_unit_anyOf_i3_llm_unit )                       | No      | object      | No         | Same as [llm_unit](#apu_anyOf_i0_llm_unit ) | Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i3_model )                             | No      | Combination | No         | -                                           | -                                                                    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_implementation"></a>6.6.5.4.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ToolCallLLMWrapper

Specific value: `"ToolCallLLMWrapper"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_tool_message_prompt"></a>6.6.5.4.2. Property `tool_message_prompt`

**Title:** Tool Message Prompt

|              |                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Required** | No                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Default**  | `"You must follow these instructions:\nYou can select zero or more of the above tools based on the user query\nIf there are multiple tools required, make sure a list of tools are returned in a JSON array.\nIf there is no tool that match the user request or you have already answered the question, you will respond with empty json array for the tools.\nYou can also add any additional notes or explanations in the notes field."` |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_llm_unit"></a>6.6.5.4.3. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Same definition as**    | [llm_unit](#apu_anyOf_i0_llm_unit)                                        |

**Description:** Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model"></a>6.6.5.4.4. Property `model`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                       |
| -------------------------------------------------------------------- |
| [LLMModel Reference](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i1)             |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0"></a>6.6.5.4.4.1. Property `LLMModel Reference`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.llm_unit.LLMModel"`                                  |

| Property                                                                           | Pattern | Type   | Deprecated | Definition | Title/Description |
| ---------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_implementation"></a>6.6.5.4.4.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i1"></a>6.6.5.4.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i5_logic_units"></a>6.6.6. Property `logic_units`

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

| Each item of this array must be                        | Description |
| ------------------------------------------------------ | ----------- |
| [LogicUnit Reference](#apu_anyOf_i5_logic_units_items) | -           |

##### <a name="autogenerated_heading_11"></a>6.6.6.1. LogicUnit Reference

**Title:** LogicUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.logic_unit.LogicUnit"`                               |

| Property                                                            | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i5_logic_units_items_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i5_logic_units_items_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i5_logic_units_items_implementation"></a>6.6.6.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i5_audio_unit"></a>6.6.7. Property `audio_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                           |
| -------------------------------------------------------- |
| [AudioUnit Reference](#apu_anyOf_i5_audio_unit_anyOf_i0) |
| [item 1](#apu_anyOf_i5_audio_unit_anyOf_i1)              |

##### <a name="apu_anyOf_i5_audio_unit_anyOf_i0"></a>6.6.7.1. Property `AudioUnit Reference`

**Title:** AudioUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.audio_unit.AudioUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i5_audio_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i5_audio_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i5_audio_unit_anyOf_i0_implementation"></a>6.6.7.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i5_audio_unit_anyOf_i1"></a>6.6.7.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i5_image_unit"></a>6.6.8. Property `image_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                           |
| -------------------------------------------------------- |
| [ImageUnit Reference](#apu_anyOf_i5_image_unit_anyOf_i0) |
| [item 1](#apu_anyOf_i5_image_unit_anyOf_i1)              |

##### <a name="apu_anyOf_i5_image_unit_anyOf_i0"></a>6.6.8.1. Property `ImageUnit Reference`

**Title:** ImageUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.image_unit.ImageUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i5_image_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i5_image_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i5_image_unit_anyOf_i0_implementation"></a>6.6.8.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i5_image_unit_anyOf_i1"></a>6.6.8.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i5_record_conversation"></a>6.6.9. Property `record_conversation`

**Title:** Record Conversation

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

#### <a name="apu_anyOf_i5_allow_tool_errors"></a>6.6.10. Property `allow_tool_errors`

**Title:** Allow Tool Errors

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

#### <a name="apu_anyOf_i5_document_processor"></a>6.6.11. Property `document_processor`

**Title:** DocumentProcessor Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"DocumentProcessor"`                                                     |

| Property                                                             | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i5_document_processor_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i5_document_processor_additionalProperties )         | No      | object | No         | -          | -                 |

##### <a name="apu_anyOf_i5_document_processor_implementation"></a>6.6.11.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

### <a name="apu_anyOf_i6"></a>6.7. Property `GPT4o.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./GPT4o.json                                                         |

| Property                                                          | Pattern | Type            | Deprecated | Definition                       | Title/Description                                                    |
| ----------------------------------------------------------------- | ------- | --------------- | ---------- | -------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i6_implementation )                 | No      | const           | No         | -                                | GPT4o                                                                |
| - [max_num_function_calls](#apu_anyOf_i6_max_num_function_calls ) | No      | integer         | No         | -                                | Max Num Function Calls                                               |
| - [io_unit](#apu_anyOf_i6_io_unit )                               | No      | object          | No         | -                                | IOUnit Reference                                                     |
| - [memory_unit](#apu_anyOf_i6_memory_unit )                       | No      | object          | No         | -                                | MemoryUnit Reference                                                 |
| - [llm_unit](#apu_anyOf_i6_llm_unit )                             | No      | object          | No         | In [LLMUnit](/docs/components/llmunit/overview) | Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components |
| - [logic_units](#apu_anyOf_i6_logic_units )                       | No      | array of object | No         | -                                | Logic Units                                                          |
| - [audio_unit](#apu_anyOf_i6_audio_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [image_unit](#apu_anyOf_i6_image_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [record_conversation](#apu_anyOf_i6_record_conversation )       | No      | boolean         | No         | -                                | Record Conversation                                                  |
| - [allow_tool_errors](#apu_anyOf_i6_allow_tool_errors )           | No      | boolean         | No         | -                                | Allow Tool Errors                                                    |
| - [document_processor](#apu_anyOf_i6_document_processor )         | No      | object          | No         | -                                | DocumentProcessor Reference                                          |

#### <a name="apu_anyOf_i6_implementation"></a>6.7.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** GPT4o

Specific value: `"GPT4o"`

#### <a name="apu_anyOf_i6_max_num_function_calls"></a>6.7.2. Property `max_num_function_calls`

**Title:** Max Num Function Calls

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `10`      |

**Description:** The maximum number of function calls to make in a single request.

#### <a name="apu_anyOf_i6_io_unit"></a>6.7.3. Property `io_unit`

**Title:** IOUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"IOUnit"`                                                                |

| Property                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i6_io_unit_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i6_io_unit_additionalProperties )         | No      | object | No         | -          | -                 |

##### <a name="apu_anyOf_i6_io_unit_implementation"></a>6.7.3.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i6_memory_unit"></a>6.7.4. Property `memory_unit`

**Title:** MemoryUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"MemoryUnit"`                                                            |

| Property                                                      | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i6_memory_unit_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i6_memory_unit_additionalProperties )         | No      | object | No         | -          | -                 |

##### <a name="apu_anyOf_i6_memory_unit_implementation"></a>6.7.4.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i6_llm_unit"></a>6.7.5. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Defined in**            | [LLMUnit](/docs/components/llmunit/overview)                                             |

**Description:** Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components

| Any of(Option)                                             |
| ---------------------------------------------------------- |
| [AnthropicLLMUnit.json](#apu_anyOf_i0_llm_unit_anyOf_i0)   |
| [MistralGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i1)         |
| [OpenAIGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i2)          |
| [ToolCallLLMWrapper.json](#apu_anyOf_i0_llm_unit_anyOf_i3) |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i0"></a>6.7.5.1. Property `AnthropicLLMUnit.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./AnthropicLLMUnit.json                                              |

| Property                                                            | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i0_implementation ) | No      | const       | No         | -          | AnthropicLLMUnit   |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i0_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i0_temperature )       | No      | number      | No         | -          | Temperature        |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_args](#apu_anyOf_i0_llm_unit_anyOf_i0_client_args )       | No      | object      | No         | -          | Client Args        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_implementation"></a>6.7.5.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AnthropicLLMUnit

Specific value: `"AnthropicLLMUnit"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model"></a>6.7.5.1.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"claude-3-opus-20240229"`                                                |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i0_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i0_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model_implementation"></a>6.7.5.1.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_temperature"></a>6.7.5.1.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens"></a>6.7.5.1.4. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i0"></a>6.7.5.1.4.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i1"></a>6.7.5.1.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_client_args"></a>6.7.5.1.5. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i1"></a>6.7.5.2. Property `MistralGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./MistralGPT.json                                                    |

| Property                                                            | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i1_implementation ) | No      | const       | No         | -          | MistralGPT         |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i1_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i1_temperature )       | No      | number      | No         | -          | Temperature        |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i1_force_json )         | No      | boolean     | No         | -          | Force Json         |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_args](#apu_anyOf_i0_llm_unit_anyOf_i1_client_args )       | No      | object      | No         | -          | Client Args        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_implementation"></a>6.7.5.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** MistralGPT

Specific value: `"MistralGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model"></a>6.7.5.2.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"mistral-large-latest"`                                                  |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i1_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i1_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model_implementation"></a>6.7.5.2.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_temperature"></a>6.7.5.2.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_force_json"></a>6.7.5.2.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens"></a>6.7.5.2.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i0"></a>6.7.5.2.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i1"></a>6.7.5.2.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_client_args"></a>6.7.5.2.6. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i2"></a>6.7.5.3. Property `OpenAIGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./OpenAIGPT.json                                                     |

| Property                                                                    | Pattern | Type        | Deprecated | Definition | Title/Description                 |
| --------------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | --------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_implementation )         | No      | const       | No         | -          | OpenAIGPT                         |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i2_model )                           | No      | object      | No         | -          | LLMModel Reference                |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i2_temperature )               | No      | number      | No         | -          | Temperature                       |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i2_force_json )                 | No      | boolean     | No         | -          | Force Json                        |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens )                 | No      | Combination | No         | -          | Max Tokens                        |
| - [connection_handler](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler ) | No      | object      | No         | -          | OpenAIConnectionHandler Reference |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_implementation"></a>6.7.5.3.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OpenAIGPT

Specific value: `"OpenAIGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model"></a>6.7.5.3.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"gpt-4-turbo"`                                                           |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i2_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation"></a>6.7.5.3.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_temperature"></a>6.7.5.3.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_force_json"></a>6.7.5.3.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens"></a>6.7.5.3.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i0"></a>6.7.5.3.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i1"></a>6.7.5.3.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler"></a>6.7.5.3.6. Property `connection_handler`

**Title:** OpenAIConnectionHandler Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"OpenAIConnectionHandler"`                                               |

| Property                                                                               | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_implementation"></a>6.7.5.3.6.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i3"></a>6.7.5.4. Property `ToolCallLLMWrapper.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./ToolCallLLMWrapper.json                                            |

| Property                                                                      | Pattern | Type        | Deprecated | Definition                                  | Title/Description                                                    |
| ----------------------------------------------------------------------------- | ------- | ----------- | ---------- | ------------------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_implementation )           | No      | const       | No         | -                                           | ToolCallLLMWrapper                                                   |
| - [tool_message_prompt](#apu_anyOf_i0_llm_unit_anyOf_i3_tool_message_prompt ) | No      | string      | No         | -                                           | Tool Message Prompt                                                  |
| - [llm_unit](#apu_anyOf_i0_llm_unit_anyOf_i3_llm_unit )                       | No      | object      | No         | Same as [llm_unit](#apu_anyOf_i0_llm_unit ) | Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i3_model )                             | No      | Combination | No         | -                                           | -                                                                    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_implementation"></a>6.7.5.4.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ToolCallLLMWrapper

Specific value: `"ToolCallLLMWrapper"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_tool_message_prompt"></a>6.7.5.4.2. Property `tool_message_prompt`

**Title:** Tool Message Prompt

|              |                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Required** | No                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Default**  | `"You must follow these instructions:\nYou can select zero or more of the above tools based on the user query\nIf there are multiple tools required, make sure a list of tools are returned in a JSON array.\nIf there is no tool that match the user request or you have already answered the question, you will respond with empty json array for the tools.\nYou can also add any additional notes or explanations in the notes field."` |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_llm_unit"></a>6.7.5.4.3. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Same definition as**    | [llm_unit](#apu_anyOf_i0_llm_unit)                                        |

**Description:** Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model"></a>6.7.5.4.4. Property `model`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                       |
| -------------------------------------------------------------------- |
| [LLMModel Reference](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i1)             |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0"></a>6.7.5.4.4.1. Property `LLMModel Reference`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.llm_unit.LLMModel"`                                  |

| Property                                                                           | Pattern | Type   | Deprecated | Definition | Title/Description |
| ---------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_implementation"></a>6.7.5.4.4.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i1"></a>6.7.5.4.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i6_logic_units"></a>6.7.6. Property `logic_units`

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

| Each item of this array must be                        | Description |
| ------------------------------------------------------ | ----------- |
| [LogicUnit Reference](#apu_anyOf_i6_logic_units_items) | -           |

##### <a name="autogenerated_heading_12"></a>6.7.6.1. LogicUnit Reference

**Title:** LogicUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.logic_unit.LogicUnit"`                               |

| Property                                                            | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i6_logic_units_items_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i6_logic_units_items_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i6_logic_units_items_implementation"></a>6.7.6.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i6_audio_unit"></a>6.7.7. Property `audio_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                           |
| -------------------------------------------------------- |
| [AudioUnit Reference](#apu_anyOf_i6_audio_unit_anyOf_i0) |
| [item 1](#apu_anyOf_i6_audio_unit_anyOf_i1)              |

##### <a name="apu_anyOf_i6_audio_unit_anyOf_i0"></a>6.7.7.1. Property `AudioUnit Reference`

**Title:** AudioUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.audio_unit.AudioUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i6_audio_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i6_audio_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i6_audio_unit_anyOf_i0_implementation"></a>6.7.7.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i6_audio_unit_anyOf_i1"></a>6.7.7.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i6_image_unit"></a>6.7.8. Property `image_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                           |
| -------------------------------------------------------- |
| [ImageUnit Reference](#apu_anyOf_i6_image_unit_anyOf_i0) |
| [item 1](#apu_anyOf_i6_image_unit_anyOf_i1)              |

##### <a name="apu_anyOf_i6_image_unit_anyOf_i0"></a>6.7.8.1. Property `ImageUnit Reference`

**Title:** ImageUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.image_unit.ImageUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i6_image_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i6_image_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i6_image_unit_anyOf_i0_implementation"></a>6.7.8.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i6_image_unit_anyOf_i1"></a>6.7.8.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i6_record_conversation"></a>6.7.9. Property `record_conversation`

**Title:** Record Conversation

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

#### <a name="apu_anyOf_i6_allow_tool_errors"></a>6.7.10. Property `allow_tool_errors`

**Title:** Allow Tool Errors

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

#### <a name="apu_anyOf_i6_document_processor"></a>6.7.11. Property `document_processor`

**Title:** DocumentProcessor Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"DocumentProcessor"`                                                     |

| Property                                                             | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i6_document_processor_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i6_document_processor_additionalProperties )         | No      | object | No         | -          | -                 |

##### <a name="apu_anyOf_i6_document_processor_implementation"></a>6.7.11.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

### <a name="apu_anyOf_i7"></a>6.8. Property `MistralLarge.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./MistralLarge.json                                                  |

| Property                                                          | Pattern | Type            | Deprecated | Definition                       | Title/Description                                                    |
| ----------------------------------------------------------------- | ------- | --------------- | ---------- | -------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i7_implementation )                 | No      | const           | No         | -                                | MistralLarge                                                         |
| - [max_num_function_calls](#apu_anyOf_i7_max_num_function_calls ) | No      | integer         | No         | -                                | Max Num Function Calls                                               |
| - [io_unit](#apu_anyOf_i7_io_unit )                               | No      | object          | No         | -                                | IOUnit Reference                                                     |
| - [memory_unit](#apu_anyOf_i7_memory_unit )                       | No      | object          | No         | -                                | MemoryUnit Reference                                                 |
| - [llm_unit](#apu_anyOf_i7_llm_unit )                             | No      | object          | No         | In [LLMUnit](/docs/components/llmunit/overview) | Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components |
| - [logic_units](#apu_anyOf_i7_logic_units )                       | No      | array of object | No         | -                                | Logic Units                                                          |
| - [audio_unit](#apu_anyOf_i7_audio_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [image_unit](#apu_anyOf_i7_image_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [record_conversation](#apu_anyOf_i7_record_conversation )       | No      | boolean         | No         | -                                | Record Conversation                                                  |
| - [allow_tool_errors](#apu_anyOf_i7_allow_tool_errors )           | No      | boolean         | No         | -                                | Allow Tool Errors                                                    |
| - [document_processor](#apu_anyOf_i7_document_processor )         | No      | object          | No         | -                                | DocumentProcessor Reference                                          |

#### <a name="apu_anyOf_i7_implementation"></a>6.8.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** MistralLarge

Specific value: `"MistralLarge"`

#### <a name="apu_anyOf_i7_max_num_function_calls"></a>6.8.2. Property `max_num_function_calls`

**Title:** Max Num Function Calls

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `10`      |

**Description:** The maximum number of function calls to make in a single request.

#### <a name="apu_anyOf_i7_io_unit"></a>6.8.3. Property `io_unit`

**Title:** IOUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"IOUnit"`                                                                |

| Property                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i7_io_unit_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i7_io_unit_additionalProperties )         | No      | object | No         | -          | -                 |

##### <a name="apu_anyOf_i7_io_unit_implementation"></a>6.8.3.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i7_memory_unit"></a>6.8.4. Property `memory_unit`

**Title:** MemoryUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"MemoryUnit"`                                                            |

| Property                                                      | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i7_memory_unit_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i7_memory_unit_additionalProperties )         | No      | object | No         | -          | -                 |

##### <a name="apu_anyOf_i7_memory_unit_implementation"></a>6.8.4.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i7_llm_unit"></a>6.8.5. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Defined in**            | [LLMUnit](/docs/components/llmunit/overview)                                             |

**Description:** Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components

| Any of(Option)                                             |
| ---------------------------------------------------------- |
| [AnthropicLLMUnit.json](#apu_anyOf_i0_llm_unit_anyOf_i0)   |
| [MistralGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i1)         |
| [OpenAIGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i2)          |
| [ToolCallLLMWrapper.json](#apu_anyOf_i0_llm_unit_anyOf_i3) |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i0"></a>6.8.5.1. Property `AnthropicLLMUnit.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./AnthropicLLMUnit.json                                              |

| Property                                                            | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i0_implementation ) | No      | const       | No         | -          | AnthropicLLMUnit   |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i0_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i0_temperature )       | No      | number      | No         | -          | Temperature        |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_args](#apu_anyOf_i0_llm_unit_anyOf_i0_client_args )       | No      | object      | No         | -          | Client Args        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_implementation"></a>6.8.5.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AnthropicLLMUnit

Specific value: `"AnthropicLLMUnit"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model"></a>6.8.5.1.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"claude-3-opus-20240229"`                                                |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i0_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i0_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model_implementation"></a>6.8.5.1.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_temperature"></a>6.8.5.1.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens"></a>6.8.5.1.4. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i0"></a>6.8.5.1.4.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i1"></a>6.8.5.1.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_client_args"></a>6.8.5.1.5. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i1"></a>6.8.5.2. Property `MistralGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./MistralGPT.json                                                    |

| Property                                                            | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i1_implementation ) | No      | const       | No         | -          | MistralGPT         |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i1_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i1_temperature )       | No      | number      | No         | -          | Temperature        |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i1_force_json )         | No      | boolean     | No         | -          | Force Json         |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_args](#apu_anyOf_i0_llm_unit_anyOf_i1_client_args )       | No      | object      | No         | -          | Client Args        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_implementation"></a>6.8.5.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** MistralGPT

Specific value: `"MistralGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model"></a>6.8.5.2.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"mistral-large-latest"`                                                  |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i1_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i1_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model_implementation"></a>6.8.5.2.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_temperature"></a>6.8.5.2.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_force_json"></a>6.8.5.2.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens"></a>6.8.5.2.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i0"></a>6.8.5.2.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i1"></a>6.8.5.2.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_client_args"></a>6.8.5.2.6. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i2"></a>6.8.5.3. Property `OpenAIGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./OpenAIGPT.json                                                     |

| Property                                                                    | Pattern | Type        | Deprecated | Definition | Title/Description                 |
| --------------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | --------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_implementation )         | No      | const       | No         | -          | OpenAIGPT                         |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i2_model )                           | No      | object      | No         | -          | LLMModel Reference                |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i2_temperature )               | No      | number      | No         | -          | Temperature                       |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i2_force_json )                 | No      | boolean     | No         | -          | Force Json                        |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens )                 | No      | Combination | No         | -          | Max Tokens                        |
| - [connection_handler](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler ) | No      | object      | No         | -          | OpenAIConnectionHandler Reference |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_implementation"></a>6.8.5.3.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OpenAIGPT

Specific value: `"OpenAIGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model"></a>6.8.5.3.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"gpt-4-turbo"`                                                           |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i2_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation"></a>6.8.5.3.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_temperature"></a>6.8.5.3.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_force_json"></a>6.8.5.3.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens"></a>6.8.5.3.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i0"></a>6.8.5.3.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i1"></a>6.8.5.3.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler"></a>6.8.5.3.6. Property `connection_handler`

**Title:** OpenAIConnectionHandler Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"OpenAIConnectionHandler"`                                               |

| Property                                                                               | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_implementation"></a>6.8.5.3.6.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i3"></a>6.8.5.4. Property `ToolCallLLMWrapper.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./ToolCallLLMWrapper.json                                            |

| Property                                                                      | Pattern | Type        | Deprecated | Definition                                  | Title/Description                                                    |
| ----------------------------------------------------------------------------- | ------- | ----------- | ---------- | ------------------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_implementation )           | No      | const       | No         | -                                           | ToolCallLLMWrapper                                                   |
| - [tool_message_prompt](#apu_anyOf_i0_llm_unit_anyOf_i3_tool_message_prompt ) | No      | string      | No         | -                                           | Tool Message Prompt                                                  |
| - [llm_unit](#apu_anyOf_i0_llm_unit_anyOf_i3_llm_unit )                       | No      | object      | No         | Same as [llm_unit](#apu_anyOf_i0_llm_unit ) | Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i3_model )                             | No      | Combination | No         | -                                           | -                                                                    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_implementation"></a>6.8.5.4.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ToolCallLLMWrapper

Specific value: `"ToolCallLLMWrapper"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_tool_message_prompt"></a>6.8.5.4.2. Property `tool_message_prompt`

**Title:** Tool Message Prompt

|              |                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Required** | No                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Default**  | `"You must follow these instructions:\nYou can select zero or more of the above tools based on the user query\nIf there are multiple tools required, make sure a list of tools are returned in a JSON array.\nIf there is no tool that match the user request or you have already answered the question, you will respond with empty json array for the tools.\nYou can also add any additional notes or explanations in the notes field."` |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_llm_unit"></a>6.8.5.4.3. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Same definition as**    | [llm_unit](#apu_anyOf_i0_llm_unit)                                        |

**Description:** Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model"></a>6.8.5.4.4. Property `model`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                       |
| -------------------------------------------------------------------- |
| [LLMModel Reference](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i1)             |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0"></a>6.8.5.4.4.1. Property `LLMModel Reference`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.llm_unit.LLMModel"`                                  |

| Property                                                                           | Pattern | Type   | Deprecated | Definition | Title/Description |
| ---------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_implementation"></a>6.8.5.4.4.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i1"></a>6.8.5.4.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i7_logic_units"></a>6.8.6. Property `logic_units`

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

| Each item of this array must be                        | Description |
| ------------------------------------------------------ | ----------- |
| [LogicUnit Reference](#apu_anyOf_i7_logic_units_items) | -           |

##### <a name="autogenerated_heading_13"></a>6.8.6.1. LogicUnit Reference

**Title:** LogicUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.logic_unit.LogicUnit"`                               |

| Property                                                            | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i7_logic_units_items_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i7_logic_units_items_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i7_logic_units_items_implementation"></a>6.8.6.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i7_audio_unit"></a>6.8.7. Property `audio_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                           |
| -------------------------------------------------------- |
| [AudioUnit Reference](#apu_anyOf_i7_audio_unit_anyOf_i0) |
| [item 1](#apu_anyOf_i7_audio_unit_anyOf_i1)              |

##### <a name="apu_anyOf_i7_audio_unit_anyOf_i0"></a>6.8.7.1. Property `AudioUnit Reference`

**Title:** AudioUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.audio_unit.AudioUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i7_audio_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i7_audio_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i7_audio_unit_anyOf_i0_implementation"></a>6.8.7.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i7_audio_unit_anyOf_i1"></a>6.8.7.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i7_image_unit"></a>6.8.8. Property `image_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                           |
| -------------------------------------------------------- |
| [ImageUnit Reference](#apu_anyOf_i7_image_unit_anyOf_i0) |
| [item 1](#apu_anyOf_i7_image_unit_anyOf_i1)              |

##### <a name="apu_anyOf_i7_image_unit_anyOf_i0"></a>6.8.8.1. Property `ImageUnit Reference`

**Title:** ImageUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.image_unit.ImageUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i7_image_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i7_image_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i7_image_unit_anyOf_i0_implementation"></a>6.8.8.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i7_image_unit_anyOf_i1"></a>6.8.8.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i7_record_conversation"></a>6.8.9. Property `record_conversation`

**Title:** Record Conversation

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

#### <a name="apu_anyOf_i7_allow_tool_errors"></a>6.8.10. Property `allow_tool_errors`

**Title:** Allow Tool Errors

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

#### <a name="apu_anyOf_i7_document_processor"></a>6.8.11. Property `document_processor`

**Title:** DocumentProcessor Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"DocumentProcessor"`                                                     |

| Property                                                             | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i7_document_processor_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i7_document_processor_additionalProperties )         | No      | object | No         | -          | -                 |

##### <a name="apu_anyOf_i7_document_processor_implementation"></a>6.8.11.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

### <a name="apu_anyOf_i8"></a>6.9. Property `MistralMedium.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./MistralMedium.json                                                 |

| Property                                                          | Pattern | Type            | Deprecated | Definition                       | Title/Description                                                    |
| ----------------------------------------------------------------- | ------- | --------------- | ---------- | -------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i8_implementation )                 | No      | const           | No         | -                                | MistralMedium                                                        |
| - [max_num_function_calls](#apu_anyOf_i8_max_num_function_calls ) | No      | integer         | No         | -                                | Max Num Function Calls                                               |
| - [io_unit](#apu_anyOf_i8_io_unit )                               | No      | object          | No         | -                                | IOUnit Reference                                                     |
| - [memory_unit](#apu_anyOf_i8_memory_unit )                       | No      | object          | No         | -                                | MemoryUnit Reference                                                 |
| - [llm_unit](#apu_anyOf_i8_llm_unit )                             | No      | object          | No         | In [LLMUnit](/docs/components/llmunit/overview) | Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components |
| - [logic_units](#apu_anyOf_i8_logic_units )                       | No      | array of object | No         | -                                | Logic Units                                                          |
| - [audio_unit](#apu_anyOf_i8_audio_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [image_unit](#apu_anyOf_i8_image_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [record_conversation](#apu_anyOf_i8_record_conversation )       | No      | boolean         | No         | -                                | Record Conversation                                                  |
| - [allow_tool_errors](#apu_anyOf_i8_allow_tool_errors )           | No      | boolean         | No         | -                                | Allow Tool Errors                                                    |
| - [document_processor](#apu_anyOf_i8_document_processor )         | No      | object          | No         | -                                | DocumentProcessor Reference                                          |

#### <a name="apu_anyOf_i8_implementation"></a>6.9.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** MistralMedium

Specific value: `"MistralMedium"`

#### <a name="apu_anyOf_i8_max_num_function_calls"></a>6.9.2. Property `max_num_function_calls`

**Title:** Max Num Function Calls

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `10`      |

**Description:** The maximum number of function calls to make in a single request.

#### <a name="apu_anyOf_i8_io_unit"></a>6.9.3. Property `io_unit`

**Title:** IOUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"IOUnit"`                                                                |

| Property                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i8_io_unit_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i8_io_unit_additionalProperties )         | No      | object | No         | -          | -                 |

##### <a name="apu_anyOf_i8_io_unit_implementation"></a>6.9.3.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i8_memory_unit"></a>6.9.4. Property `memory_unit`

**Title:** MemoryUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"MemoryUnit"`                                                            |

| Property                                                      | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i8_memory_unit_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i8_memory_unit_additionalProperties )         | No      | object | No         | -          | -                 |

##### <a name="apu_anyOf_i8_memory_unit_implementation"></a>6.9.4.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i8_llm_unit"></a>6.9.5. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Defined in**            | [LLMUnit](/docs/components/llmunit/overview)                                             |

**Description:** Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components

| Any of(Option)                                             |
| ---------------------------------------------------------- |
| [AnthropicLLMUnit.json](#apu_anyOf_i0_llm_unit_anyOf_i0)   |
| [MistralGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i1)         |
| [OpenAIGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i2)          |
| [ToolCallLLMWrapper.json](#apu_anyOf_i0_llm_unit_anyOf_i3) |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i0"></a>6.9.5.1. Property `AnthropicLLMUnit.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./AnthropicLLMUnit.json                                              |

| Property                                                            | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i0_implementation ) | No      | const       | No         | -          | AnthropicLLMUnit   |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i0_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i0_temperature )       | No      | number      | No         | -          | Temperature        |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_args](#apu_anyOf_i0_llm_unit_anyOf_i0_client_args )       | No      | object      | No         | -          | Client Args        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_implementation"></a>6.9.5.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AnthropicLLMUnit

Specific value: `"AnthropicLLMUnit"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model"></a>6.9.5.1.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"claude-3-opus-20240229"`                                                |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i0_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i0_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model_implementation"></a>6.9.5.1.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_temperature"></a>6.9.5.1.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens"></a>6.9.5.1.4. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i0"></a>6.9.5.1.4.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i1"></a>6.9.5.1.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_client_args"></a>6.9.5.1.5. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i1"></a>6.9.5.2. Property `MistralGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./MistralGPT.json                                                    |

| Property                                                            | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i1_implementation ) | No      | const       | No         | -          | MistralGPT         |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i1_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i1_temperature )       | No      | number      | No         | -          | Temperature        |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i1_force_json )         | No      | boolean     | No         | -          | Force Json         |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_args](#apu_anyOf_i0_llm_unit_anyOf_i1_client_args )       | No      | object      | No         | -          | Client Args        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_implementation"></a>6.9.5.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** MistralGPT

Specific value: `"MistralGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model"></a>6.9.5.2.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"mistral-large-latest"`                                                  |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i1_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i1_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model_implementation"></a>6.9.5.2.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_temperature"></a>6.9.5.2.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_force_json"></a>6.9.5.2.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens"></a>6.9.5.2.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i0"></a>6.9.5.2.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i1"></a>6.9.5.2.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_client_args"></a>6.9.5.2.6. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i2"></a>6.9.5.3. Property `OpenAIGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./OpenAIGPT.json                                                     |

| Property                                                                    | Pattern | Type        | Deprecated | Definition | Title/Description                 |
| --------------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | --------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_implementation )         | No      | const       | No         | -          | OpenAIGPT                         |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i2_model )                           | No      | object      | No         | -          | LLMModel Reference                |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i2_temperature )               | No      | number      | No         | -          | Temperature                       |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i2_force_json )                 | No      | boolean     | No         | -          | Force Json                        |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens )                 | No      | Combination | No         | -          | Max Tokens                        |
| - [connection_handler](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler ) | No      | object      | No         | -          | OpenAIConnectionHandler Reference |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_implementation"></a>6.9.5.3.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OpenAIGPT

Specific value: `"OpenAIGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model"></a>6.9.5.3.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"gpt-4-turbo"`                                                           |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i2_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation"></a>6.9.5.3.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_temperature"></a>6.9.5.3.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_force_json"></a>6.9.5.3.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens"></a>6.9.5.3.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i0"></a>6.9.5.3.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i1"></a>6.9.5.3.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler"></a>6.9.5.3.6. Property `connection_handler`

**Title:** OpenAIConnectionHandler Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"OpenAIConnectionHandler"`                                               |

| Property                                                                               | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_implementation"></a>6.9.5.3.6.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i3"></a>6.9.5.4. Property `ToolCallLLMWrapper.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./ToolCallLLMWrapper.json                                            |

| Property                                                                      | Pattern | Type        | Deprecated | Definition                                  | Title/Description                                                    |
| ----------------------------------------------------------------------------- | ------- | ----------- | ---------- | ------------------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_implementation )           | No      | const       | No         | -                                           | ToolCallLLMWrapper                                                   |
| - [tool_message_prompt](#apu_anyOf_i0_llm_unit_anyOf_i3_tool_message_prompt ) | No      | string      | No         | -                                           | Tool Message Prompt                                                  |
| - [llm_unit](#apu_anyOf_i0_llm_unit_anyOf_i3_llm_unit )                       | No      | object      | No         | Same as [llm_unit](#apu_anyOf_i0_llm_unit ) | Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i3_model )                             | No      | Combination | No         | -                                           | -                                                                    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_implementation"></a>6.9.5.4.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ToolCallLLMWrapper

Specific value: `"ToolCallLLMWrapper"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_tool_message_prompt"></a>6.9.5.4.2. Property `tool_message_prompt`

**Title:** Tool Message Prompt

|              |                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Required** | No                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Default**  | `"You must follow these instructions:\nYou can select zero or more of the above tools based on the user query\nIf there are multiple tools required, make sure a list of tools are returned in a JSON array.\nIf there is no tool that match the user request or you have already answered the question, you will respond with empty json array for the tools.\nYou can also add any additional notes or explanations in the notes field."` |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_llm_unit"></a>6.9.5.4.3. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Same definition as**    | [llm_unit](#apu_anyOf_i0_llm_unit)                                        |

**Description:** Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model"></a>6.9.5.4.4. Property `model`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                       |
| -------------------------------------------------------------------- |
| [LLMModel Reference](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i1)             |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0"></a>6.9.5.4.4.1. Property `LLMModel Reference`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.llm_unit.LLMModel"`                                  |

| Property                                                                           | Pattern | Type   | Deprecated | Definition | Title/Description |
| ---------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_implementation"></a>6.9.5.4.4.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i1"></a>6.9.5.4.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i8_logic_units"></a>6.9.6. Property `logic_units`

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

| Each item of this array must be                        | Description |
| ------------------------------------------------------ | ----------- |
| [LogicUnit Reference](#apu_anyOf_i8_logic_units_items) | -           |

##### <a name="autogenerated_heading_14"></a>6.9.6.1. LogicUnit Reference

**Title:** LogicUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.logic_unit.LogicUnit"`                               |

| Property                                                            | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i8_logic_units_items_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i8_logic_units_items_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i8_logic_units_items_implementation"></a>6.9.6.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i8_audio_unit"></a>6.9.7. Property `audio_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                           |
| -------------------------------------------------------- |
| [AudioUnit Reference](#apu_anyOf_i8_audio_unit_anyOf_i0) |
| [item 1](#apu_anyOf_i8_audio_unit_anyOf_i1)              |

##### <a name="apu_anyOf_i8_audio_unit_anyOf_i0"></a>6.9.7.1. Property `AudioUnit Reference`

**Title:** AudioUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.audio_unit.AudioUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i8_audio_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i8_audio_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i8_audio_unit_anyOf_i0_implementation"></a>6.9.7.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i8_audio_unit_anyOf_i1"></a>6.9.7.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i8_image_unit"></a>6.9.8. Property `image_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                           |
| -------------------------------------------------------- |
| [ImageUnit Reference](#apu_anyOf_i8_image_unit_anyOf_i0) |
| [item 1](#apu_anyOf_i8_image_unit_anyOf_i1)              |

##### <a name="apu_anyOf_i8_image_unit_anyOf_i0"></a>6.9.8.1. Property `ImageUnit Reference`

**Title:** ImageUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.image_unit.ImageUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i8_image_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i8_image_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i8_image_unit_anyOf_i0_implementation"></a>6.9.8.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i8_image_unit_anyOf_i1"></a>6.9.8.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i8_record_conversation"></a>6.9.9. Property `record_conversation`

**Title:** Record Conversation

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

#### <a name="apu_anyOf_i8_allow_tool_errors"></a>6.9.10. Property `allow_tool_errors`

**Title:** Allow Tool Errors

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

#### <a name="apu_anyOf_i8_document_processor"></a>6.9.11. Property `document_processor`

**Title:** DocumentProcessor Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"DocumentProcessor"`                                                     |

| Property                                                             | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i8_document_processor_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i8_document_processor_additionalProperties )         | No      | object | No         | -          | -                 |

##### <a name="apu_anyOf_i8_document_processor_implementation"></a>6.9.11.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

### <a name="apu_anyOf_i9"></a>6.10. Property `MistralSmall.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./MistralSmall.json                                                  |

| Property                                                          | Pattern | Type            | Deprecated | Definition                       | Title/Description                                                    |
| ----------------------------------------------------------------- | ------- | --------------- | ---------- | -------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i9_implementation )                 | No      | const           | No         | -                                | MistralSmall                                                         |
| - [max_num_function_calls](#apu_anyOf_i9_max_num_function_calls ) | No      | integer         | No         | -                                | Max Num Function Calls                                               |
| - [io_unit](#apu_anyOf_i9_io_unit )                               | No      | object          | No         | -                                | IOUnit Reference                                                     |
| - [memory_unit](#apu_anyOf_i9_memory_unit )                       | No      | object          | No         | -                                | MemoryUnit Reference                                                 |
| - [llm_unit](#apu_anyOf_i9_llm_unit )                             | No      | object          | No         | In [LLMUnit](/docs/components/llmunit/overview) | Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components |
| - [logic_units](#apu_anyOf_i9_logic_units )                       | No      | array of object | No         | -                                | Logic Units                                                          |
| - [audio_unit](#apu_anyOf_i9_audio_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [image_unit](#apu_anyOf_i9_image_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [record_conversation](#apu_anyOf_i9_record_conversation )       | No      | boolean         | No         | -                                | Record Conversation                                                  |
| - [allow_tool_errors](#apu_anyOf_i9_allow_tool_errors )           | No      | boolean         | No         | -                                | Allow Tool Errors                                                    |
| - [document_processor](#apu_anyOf_i9_document_processor )         | No      | object          | No         | -                                | DocumentProcessor Reference                                          |

#### <a name="apu_anyOf_i9_implementation"></a>6.10.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** MistralSmall

Specific value: `"MistralSmall"`

#### <a name="apu_anyOf_i9_max_num_function_calls"></a>6.10.2. Property `max_num_function_calls`

**Title:** Max Num Function Calls

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `10`      |

**Description:** The maximum number of function calls to make in a single request.

#### <a name="apu_anyOf_i9_io_unit"></a>6.10.3. Property `io_unit`

**Title:** IOUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"IOUnit"`                                                                |

| Property                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i9_io_unit_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i9_io_unit_additionalProperties )         | No      | object | No         | -          | -                 |

##### <a name="apu_anyOf_i9_io_unit_implementation"></a>6.10.3.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i9_memory_unit"></a>6.10.4. Property `memory_unit`

**Title:** MemoryUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"MemoryUnit"`                                                            |

| Property                                                      | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i9_memory_unit_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i9_memory_unit_additionalProperties )         | No      | object | No         | -          | -                 |

##### <a name="apu_anyOf_i9_memory_unit_implementation"></a>6.10.4.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i9_llm_unit"></a>6.10.5. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Defined in**            | [LLMUnit](/docs/components/llmunit/overview)                                             |

**Description:** Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components

| Any of(Option)                                             |
| ---------------------------------------------------------- |
| [AnthropicLLMUnit.json](#apu_anyOf_i0_llm_unit_anyOf_i0)   |
| [MistralGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i1)         |
| [OpenAIGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i2)          |
| [ToolCallLLMWrapper.json](#apu_anyOf_i0_llm_unit_anyOf_i3) |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i0"></a>6.10.5.1. Property `AnthropicLLMUnit.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./AnthropicLLMUnit.json                                              |

| Property                                                            | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i0_implementation ) | No      | const       | No         | -          | AnthropicLLMUnit   |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i0_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i0_temperature )       | No      | number      | No         | -          | Temperature        |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_args](#apu_anyOf_i0_llm_unit_anyOf_i0_client_args )       | No      | object      | No         | -          | Client Args        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_implementation"></a>6.10.5.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AnthropicLLMUnit

Specific value: `"AnthropicLLMUnit"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model"></a>6.10.5.1.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"claude-3-opus-20240229"`                                                |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i0_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i0_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model_implementation"></a>6.10.5.1.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_temperature"></a>6.10.5.1.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens"></a>6.10.5.1.4. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i0"></a>6.10.5.1.4.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i1"></a>6.10.5.1.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_client_args"></a>6.10.5.1.5. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i1"></a>6.10.5.2. Property `MistralGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./MistralGPT.json                                                    |

| Property                                                            | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i1_implementation ) | No      | const       | No         | -          | MistralGPT         |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i1_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i1_temperature )       | No      | number      | No         | -          | Temperature        |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i1_force_json )         | No      | boolean     | No         | -          | Force Json         |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_args](#apu_anyOf_i0_llm_unit_anyOf_i1_client_args )       | No      | object      | No         | -          | Client Args        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_implementation"></a>6.10.5.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** MistralGPT

Specific value: `"MistralGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model"></a>6.10.5.2.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"mistral-large-latest"`                                                  |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i1_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i1_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model_implementation"></a>6.10.5.2.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_temperature"></a>6.10.5.2.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_force_json"></a>6.10.5.2.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens"></a>6.10.5.2.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i0"></a>6.10.5.2.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i1"></a>6.10.5.2.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_client_args"></a>6.10.5.2.6. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i2"></a>6.10.5.3. Property `OpenAIGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./OpenAIGPT.json                                                     |

| Property                                                                    | Pattern | Type        | Deprecated | Definition | Title/Description                 |
| --------------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | --------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_implementation )         | No      | const       | No         | -          | OpenAIGPT                         |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i2_model )                           | No      | object      | No         | -          | LLMModel Reference                |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i2_temperature )               | No      | number      | No         | -          | Temperature                       |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i2_force_json )                 | No      | boolean     | No         | -          | Force Json                        |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens )                 | No      | Combination | No         | -          | Max Tokens                        |
| - [connection_handler](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler ) | No      | object      | No         | -          | OpenAIConnectionHandler Reference |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_implementation"></a>6.10.5.3.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OpenAIGPT

Specific value: `"OpenAIGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model"></a>6.10.5.3.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"gpt-4-turbo"`                                                           |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i2_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation"></a>6.10.5.3.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_temperature"></a>6.10.5.3.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_force_json"></a>6.10.5.3.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens"></a>6.10.5.3.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i0"></a>6.10.5.3.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i1"></a>6.10.5.3.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler"></a>6.10.5.3.6. Property `connection_handler`

**Title:** OpenAIConnectionHandler Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"OpenAIConnectionHandler"`                                               |

| Property                                                                               | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_implementation"></a>6.10.5.3.6.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i3"></a>6.10.5.4. Property `ToolCallLLMWrapper.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./ToolCallLLMWrapper.json                                            |

| Property                                                                      | Pattern | Type        | Deprecated | Definition                                  | Title/Description                                                    |
| ----------------------------------------------------------------------------- | ------- | ----------- | ---------- | ------------------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_implementation )           | No      | const       | No         | -                                           | ToolCallLLMWrapper                                                   |
| - [tool_message_prompt](#apu_anyOf_i0_llm_unit_anyOf_i3_tool_message_prompt ) | No      | string      | No         | -                                           | Tool Message Prompt                                                  |
| - [llm_unit](#apu_anyOf_i0_llm_unit_anyOf_i3_llm_unit )                       | No      | object      | No         | Same as [llm_unit](#apu_anyOf_i0_llm_unit ) | Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i3_model )                             | No      | Combination | No         | -                                           | -                                                                    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_implementation"></a>6.10.5.4.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ToolCallLLMWrapper

Specific value: `"ToolCallLLMWrapper"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_tool_message_prompt"></a>6.10.5.4.2. Property `tool_message_prompt`

**Title:** Tool Message Prompt

|              |                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Required** | No                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Default**  | `"You must follow these instructions:\nYou can select zero or more of the above tools based on the user query\nIf there are multiple tools required, make sure a list of tools are returned in a JSON array.\nIf there is no tool that match the user request or you have already answered the question, you will respond with empty json array for the tools.\nYou can also add any additional notes or explanations in the notes field."` |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_llm_unit"></a>6.10.5.4.3. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Same definition as**    | [llm_unit](#apu_anyOf_i0_llm_unit)                                        |

**Description:** Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model"></a>6.10.5.4.4. Property `model`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                       |
| -------------------------------------------------------------------- |
| [LLMModel Reference](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i1)             |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0"></a>6.10.5.4.4.1. Property `LLMModel Reference`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.llm_unit.LLMModel"`                                  |

| Property                                                                           | Pattern | Type   | Deprecated | Definition | Title/Description |
| ---------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_implementation"></a>6.10.5.4.4.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i1"></a>6.10.5.4.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i9_logic_units"></a>6.10.6. Property `logic_units`

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

| Each item of this array must be                        | Description |
| ------------------------------------------------------ | ----------- |
| [LogicUnit Reference](#apu_anyOf_i9_logic_units_items) | -           |

##### <a name="autogenerated_heading_15"></a>6.10.6.1. LogicUnit Reference

**Title:** LogicUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.logic_unit.LogicUnit"`                               |

| Property                                                            | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i9_logic_units_items_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i9_logic_units_items_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i9_logic_units_items_implementation"></a>6.10.6.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i9_audio_unit"></a>6.10.7. Property `audio_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                           |
| -------------------------------------------------------- |
| [AudioUnit Reference](#apu_anyOf_i9_audio_unit_anyOf_i0) |
| [item 1](#apu_anyOf_i9_audio_unit_anyOf_i1)              |

##### <a name="apu_anyOf_i9_audio_unit_anyOf_i0"></a>6.10.7.1. Property `AudioUnit Reference`

**Title:** AudioUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.audio_unit.AudioUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i9_audio_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i9_audio_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i9_audio_unit_anyOf_i0_implementation"></a>6.10.7.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i9_audio_unit_anyOf_i1"></a>6.10.7.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i9_image_unit"></a>6.10.8. Property `image_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                           |
| -------------------------------------------------------- |
| [ImageUnit Reference](#apu_anyOf_i9_image_unit_anyOf_i0) |
| [item 1](#apu_anyOf_i9_image_unit_anyOf_i1)              |

##### <a name="apu_anyOf_i9_image_unit_anyOf_i0"></a>6.10.8.1. Property `ImageUnit Reference`

**Title:** ImageUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.image_unit.ImageUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i9_image_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i9_image_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i9_image_unit_anyOf_i0_implementation"></a>6.10.8.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i9_image_unit_anyOf_i1"></a>6.10.8.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i9_record_conversation"></a>6.10.9. Property `record_conversation`

**Title:** Record Conversation

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

#### <a name="apu_anyOf_i9_allow_tool_errors"></a>6.10.10. Property `allow_tool_errors`

**Title:** Allow Tool Errors

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

#### <a name="apu_anyOf_i9_document_processor"></a>6.10.11. Property `document_processor`

**Title:** DocumentProcessor Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"DocumentProcessor"`                                                     |

| Property                                                             | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i9_document_processor_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i9_document_processor_additionalProperties )         | No      | object | No         | -          | -                 |

##### <a name="apu_anyOf_i9_document_processor_implementation"></a>6.10.11.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

## <a name="apus"></a>7. Property `apus`

**Title:** Apus

|              |         |
| ------------ | ------- |
| **Type**     | `array` |
| **Required** | No      |
| **Default**  | `[]`    |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be | Description |
| ------------------------------- | ----------- |
| [NamedCPU](#apus_items)         | -           |

### <a name="autogenerated_heading_16"></a>7.1. NamedCPU

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | #/$defs/NamedCPU                                                          |

| Property                                | Pattern | Type        | Deprecated | Definition                   | Title/Description                                                                                                                                                                                                                                                                                                                                                                                   |
| --------------------------------------- | ------- | ----------- | ---------- | ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| - [title](#apus_items_title )           | No      | Combination | No         | -                            | Title                                                                                                                                                                                                                                                                                                                                                                                               |
| - [apu](#apus_items_apu )               | No      | object      | No         | In [APU](/docs/components/apu/overview) | <br />The APU is the main interface for the Agent to interact with the LLM.<br />The APU provides a set of capabilities that encapsulate LLM functionality and creates a clear separation between business logic and the underlying LLM implementation.<br /><br />To learn more, check out our blog article APU: [What is it and how does it work?](https://www.eidolonai.com/what_is_apu/).<br /> |
| - [default](#apus_items_default )       | No      | boolean     | No         | -                            | Default                                                                                                                                                                                                                                                                                                                                                                                             |
| - [](#apus_items_additionalProperties ) | No      | object      | No         | -                            | -                                                                                                                                                                                                                                                                                                                                                                                                   |

#### <a name="apus_items_title"></a>7.1.1. Property `title`

**Title:** Title

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                       |
| ------------------------------------ |
| [item 0](#apus_items_title_anyOf_i0) |
| [item 1](#apus_items_title_anyOf_i1) |

##### <a name="apus_items_title_anyOf_i0"></a>7.1.1.1. Property `item 0`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

##### <a name="apus_items_title_anyOf_i1"></a>7.1.1.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apus_items_apu"></a>7.1.2. Property `apu`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"APU"`                                                                   |
| **Defined in**            | [APU](/docs/components/apu/overview)                                                 |

**Description:** 
The APU is the main interface for the Agent to interact with the LLM.
The APU provides a set of capabilities that encapsulate LLM functionality and creates a clear separation between business logic and the underlying LLM implementation.

To learn more, check out our blog article APU: [What is it and how does it work?](https://www.eidolonai.com/what_is_apu/).

| Any of(Option)                          |
| --------------------------------------- |
| [ClaudeHaiku.json](#apu_anyOf_i0)       |
| [ClaudeOpus.json](#apu_anyOf_i1)        |
| [ClaudeSonnet.json](#apu_anyOf_i2)      |
| [ConversationalAPU.json](#apu_anyOf_i3) |
| [GPT3.5-turbo.json](#apu_anyOf_i4)      |
| [GPT4-turbo.json](#apu_anyOf_i5)        |
| [GPT4o.json](#apu_anyOf_i6)             |
| [MistralLarge.json](#apu_anyOf_i7)      |
| [MistralMedium.json](#apu_anyOf_i8)     |
| [MistralSmall.json](#apu_anyOf_i9)      |

##### <a name="apu_anyOf_i0"></a>7.1.2.1. Property `ClaudeHaiku.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./ClaudeHaiku.json                                                   |

| Property                                                          | Pattern | Type            | Deprecated | Definition                       | Title/Description                                                    |
| ----------------------------------------------------------------- | ------- | --------------- | ---------- | -------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i0_implementation )                 | No      | const           | No         | -                                | ClaudeHaiku                                                          |
| - [max_num_function_calls](#apu_anyOf_i0_max_num_function_calls ) | No      | integer         | No         | -                                | Max Num Function Calls                                               |
| - [io_unit](#apu_anyOf_i0_io_unit )                               | No      | object          | No         | -                                | IOUnit Reference                                                     |
| - [memory_unit](#apu_anyOf_i0_memory_unit )                       | No      | object          | No         | -                                | MemoryUnit Reference                                                 |
| - [llm_unit](#apu_anyOf_i0_llm_unit )                             | No      | object          | No         | In [LLMUnit](/docs/components/llmunit/overview) | Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components |
| - [logic_units](#apu_anyOf_i0_logic_units )                       | No      | array of object | No         | -                                | Logic Units                                                          |
| - [audio_unit](#apu_anyOf_i0_audio_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [image_unit](#apu_anyOf_i0_image_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [record_conversation](#apu_anyOf_i0_record_conversation )       | No      | boolean         | No         | -                                | Record Conversation                                                  |
| - [allow_tool_errors](#apu_anyOf_i0_allow_tool_errors )           | No      | boolean         | No         | -                                | Allow Tool Errors                                                    |
| - [document_processor](#apu_anyOf_i0_document_processor )         | No      | object          | No         | -                                | DocumentProcessor Reference                                          |

###### <a name="apu_anyOf_i0_implementation"></a>7.1.2.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ClaudeHaiku

Specific value: `"ClaudeHaiku"`

###### <a name="apu_anyOf_i0_max_num_function_calls"></a>7.1.2.1.2. Property `max_num_function_calls`

**Title:** Max Num Function Calls

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `10`      |

**Description:** The maximum number of function calls to make in a single request.

###### <a name="apu_anyOf_i0_io_unit"></a>7.1.2.1.3. Property `io_unit`

**Title:** IOUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"IOUnit"`                                                                |

| Property                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_io_unit_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_io_unit_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_io_unit_implementation"></a>7.1.2.1.3.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_memory_unit"></a>7.1.2.1.4. Property `memory_unit`

**Title:** MemoryUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"MemoryUnit"`                                                            |

| Property                                                      | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_memory_unit_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_memory_unit_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_memory_unit_implementation"></a>7.1.2.1.4.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit"></a>7.1.2.1.5. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Defined in**            | [LLMUnit](/docs/components/llmunit/overview)                                             |

**Description:** Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components

| Any of(Option)                                             |
| ---------------------------------------------------------- |
| [AnthropicLLMUnit.json](#apu_anyOf_i0_llm_unit_anyOf_i0)   |
| [MistralGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i1)         |
| [OpenAIGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i2)          |
| [ToolCallLLMWrapper.json](#apu_anyOf_i0_llm_unit_anyOf_i3) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0"></a>7.1.2.1.5.1. Property `AnthropicLLMUnit.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./AnthropicLLMUnit.json                                              |

| Property                                                            | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i0_implementation ) | No      | const       | No         | -          | AnthropicLLMUnit   |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i0_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i0_temperature )       | No      | number      | No         | -          | Temperature        |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_args](#apu_anyOf_i0_llm_unit_anyOf_i0_client_args )       | No      | object      | No         | -          | Client Args        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_implementation"></a>7.1.2.1.5.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AnthropicLLMUnit

Specific value: `"AnthropicLLMUnit"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model"></a>7.1.2.1.5.1.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"claude-3-opus-20240229"`                                                |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i0_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i0_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model_implementation"></a>7.1.2.1.5.1.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_temperature"></a>7.1.2.1.5.1.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens"></a>7.1.2.1.5.1.4. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i0"></a>7.1.2.1.5.1.4.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i1"></a>7.1.2.1.5.1.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_client_args"></a>7.1.2.1.5.1.5. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1"></a>7.1.2.1.5.2. Property `MistralGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./MistralGPT.json                                                    |

| Property                                                            | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i1_implementation ) | No      | const       | No         | -          | MistralGPT         |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i1_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i1_temperature )       | No      | number      | No         | -          | Temperature        |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i1_force_json )         | No      | boolean     | No         | -          | Force Json         |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_args](#apu_anyOf_i0_llm_unit_anyOf_i1_client_args )       | No      | object      | No         | -          | Client Args        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_implementation"></a>7.1.2.1.5.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** MistralGPT

Specific value: `"MistralGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model"></a>7.1.2.1.5.2.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"mistral-large-latest"`                                                  |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i1_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i1_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model_implementation"></a>7.1.2.1.5.2.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_temperature"></a>7.1.2.1.5.2.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_force_json"></a>7.1.2.1.5.2.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens"></a>7.1.2.1.5.2.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i0"></a>7.1.2.1.5.2.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i1"></a>7.1.2.1.5.2.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_client_args"></a>7.1.2.1.5.2.6. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2"></a>7.1.2.1.5.3. Property `OpenAIGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./OpenAIGPT.json                                                     |

| Property                                                                    | Pattern | Type        | Deprecated | Definition | Title/Description                 |
| --------------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | --------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_implementation )         | No      | const       | No         | -          | OpenAIGPT                         |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i2_model )                           | No      | object      | No         | -          | LLMModel Reference                |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i2_temperature )               | No      | number      | No         | -          | Temperature                       |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i2_force_json )                 | No      | boolean     | No         | -          | Force Json                        |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens )                 | No      | Combination | No         | -          | Max Tokens                        |
| - [connection_handler](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler ) | No      | object      | No         | -          | OpenAIConnectionHandler Reference |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_implementation"></a>7.1.2.1.5.3.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OpenAIGPT

Specific value: `"OpenAIGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model"></a>7.1.2.1.5.3.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"gpt-4-turbo"`                                                           |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i2_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation"></a>7.1.2.1.5.3.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_temperature"></a>7.1.2.1.5.3.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_force_json"></a>7.1.2.1.5.3.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens"></a>7.1.2.1.5.3.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i0"></a>7.1.2.1.5.3.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i1"></a>7.1.2.1.5.3.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler"></a>7.1.2.1.5.3.6. Property `connection_handler`

**Title:** OpenAIConnectionHandler Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"OpenAIConnectionHandler"`                                               |

| Property                                                                               | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_implementation"></a>7.1.2.1.5.3.6.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3"></a>7.1.2.1.5.4. Property `ToolCallLLMWrapper.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./ToolCallLLMWrapper.json                                            |

| Property                                                                      | Pattern | Type        | Deprecated | Definition                                  | Title/Description                                                    |
| ----------------------------------------------------------------------------- | ------- | ----------- | ---------- | ------------------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_implementation )           | No      | const       | No         | -                                           | ToolCallLLMWrapper                                                   |
| - [tool_message_prompt](#apu_anyOf_i0_llm_unit_anyOf_i3_tool_message_prompt ) | No      | string      | No         | -                                           | Tool Message Prompt                                                  |
| - [llm_unit](#apu_anyOf_i0_llm_unit_anyOf_i3_llm_unit )                       | No      | object      | No         | Same as [llm_unit](#apu_anyOf_i0_llm_unit ) | Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i3_model )                             | No      | Combination | No         | -                                           | -                                                                    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_implementation"></a>7.1.2.1.5.4.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ToolCallLLMWrapper

Specific value: `"ToolCallLLMWrapper"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_tool_message_prompt"></a>7.1.2.1.5.4.2. Property `tool_message_prompt`

**Title:** Tool Message Prompt

|              |                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Required** | No                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Default**  | `"You must follow these instructions:\nYou can select zero or more of the above tools based on the user query\nIf there are multiple tools required, make sure a list of tools are returned in a JSON array.\nIf there is no tool that match the user request or you have already answered the question, you will respond with empty json array for the tools.\nYou can also add any additional notes or explanations in the notes field."` |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_llm_unit"></a>7.1.2.1.5.4.3. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Same definition as**    | [llm_unit](#apu_anyOf_i0_llm_unit)                                        |

**Description:** Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model"></a>7.1.2.1.5.4.4. Property `model`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                       |
| -------------------------------------------------------------------- |
| [LLMModel Reference](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i1)             |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0"></a>7.1.2.1.5.4.4.1. Property `LLMModel Reference`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.llm_unit.LLMModel"`                                  |

| Property                                                                           | Pattern | Type   | Deprecated | Definition | Title/Description |
| ---------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_implementation"></a>7.1.2.1.5.4.4.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i1"></a>7.1.2.1.5.4.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_logic_units"></a>7.1.2.1.6. Property `logic_units`

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

| Each item of this array must be                        | Description |
| ------------------------------------------------------ | ----------- |
| [LogicUnit Reference](#apu_anyOf_i0_logic_units_items) | -           |

###### <a name="autogenerated_heading_17"></a>7.1.2.1.6.1. LogicUnit Reference

**Title:** LogicUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.logic_unit.LogicUnit"`                               |

| Property                                                            | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_logic_units_items_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_logic_units_items_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_logic_units_items_implementation"></a>7.1.2.1.6.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_audio_unit"></a>7.1.2.1.7. Property `audio_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                           |
| -------------------------------------------------------- |
| [AudioUnit Reference](#apu_anyOf_i0_audio_unit_anyOf_i0) |
| [item 1](#apu_anyOf_i0_audio_unit_anyOf_i1)              |

###### <a name="apu_anyOf_i0_audio_unit_anyOf_i0"></a>7.1.2.1.7.1. Property `AudioUnit Reference`

**Title:** AudioUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.audio_unit.AudioUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_audio_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_audio_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_audio_unit_anyOf_i0_implementation"></a>7.1.2.1.7.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_audio_unit_anyOf_i1"></a>7.1.2.1.7.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_image_unit"></a>7.1.2.1.8. Property `image_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                           |
| -------------------------------------------------------- |
| [ImageUnit Reference](#apu_anyOf_i0_image_unit_anyOf_i0) |
| [item 1](#apu_anyOf_i0_image_unit_anyOf_i1)              |

###### <a name="apu_anyOf_i0_image_unit_anyOf_i0"></a>7.1.2.1.8.1. Property `ImageUnit Reference`

**Title:** ImageUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.image_unit.ImageUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_image_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_image_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_image_unit_anyOf_i0_implementation"></a>7.1.2.1.8.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_image_unit_anyOf_i1"></a>7.1.2.1.8.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_record_conversation"></a>7.1.2.1.9. Property `record_conversation`

**Title:** Record Conversation

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_allow_tool_errors"></a>7.1.2.1.10. Property `allow_tool_errors`

**Title:** Allow Tool Errors

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_document_processor"></a>7.1.2.1.11. Property `document_processor`

**Title:** DocumentProcessor Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"DocumentProcessor"`                                                     |

| Property                                                             | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_document_processor_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_document_processor_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_document_processor_implementation"></a>7.1.2.1.11.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i1"></a>7.1.2.2. Property `ClaudeOpus.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./ClaudeOpus.json                                                    |

| Property                                                          | Pattern | Type            | Deprecated | Definition                       | Title/Description                                                    |
| ----------------------------------------------------------------- | ------- | --------------- | ---------- | -------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i1_implementation )                 | No      | const           | No         | -                                | ClaudeOpus                                                           |
| - [max_num_function_calls](#apu_anyOf_i1_max_num_function_calls ) | No      | integer         | No         | -                                | Max Num Function Calls                                               |
| - [io_unit](#apu_anyOf_i1_io_unit )                               | No      | object          | No         | -                                | IOUnit Reference                                                     |
| - [memory_unit](#apu_anyOf_i1_memory_unit )                       | No      | object          | No         | -                                | MemoryUnit Reference                                                 |
| - [llm_unit](#apu_anyOf_i1_llm_unit )                             | No      | object          | No         | In [LLMUnit](/docs/components/llmunit/overview) | Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components |
| - [logic_units](#apu_anyOf_i1_logic_units )                       | No      | array of object | No         | -                                | Logic Units                                                          |
| - [audio_unit](#apu_anyOf_i1_audio_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [image_unit](#apu_anyOf_i1_image_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [record_conversation](#apu_anyOf_i1_record_conversation )       | No      | boolean         | No         | -                                | Record Conversation                                                  |
| - [allow_tool_errors](#apu_anyOf_i1_allow_tool_errors )           | No      | boolean         | No         | -                                | Allow Tool Errors                                                    |
| - [document_processor](#apu_anyOf_i1_document_processor )         | No      | object          | No         | -                                | DocumentProcessor Reference                                          |

###### <a name="apu_anyOf_i1_implementation"></a>7.1.2.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ClaudeOpus

Specific value: `"ClaudeOpus"`

###### <a name="apu_anyOf_i1_max_num_function_calls"></a>7.1.2.2.2. Property `max_num_function_calls`

**Title:** Max Num Function Calls

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `10`      |

**Description:** The maximum number of function calls to make in a single request.

###### <a name="apu_anyOf_i1_io_unit"></a>7.1.2.2.3. Property `io_unit`

**Title:** IOUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"IOUnit"`                                                                |

| Property                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i1_io_unit_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i1_io_unit_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i1_io_unit_implementation"></a>7.1.2.2.3.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i1_memory_unit"></a>7.1.2.2.4. Property `memory_unit`

**Title:** MemoryUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"MemoryUnit"`                                                            |

| Property                                                      | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i1_memory_unit_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i1_memory_unit_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i1_memory_unit_implementation"></a>7.1.2.2.4.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i1_llm_unit"></a>7.1.2.2.5. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Defined in**            | [LLMUnit](/docs/components/llmunit/overview)                                             |

**Description:** Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components

| Any of(Option)                                             |
| ---------------------------------------------------------- |
| [AnthropicLLMUnit.json](#apu_anyOf_i0_llm_unit_anyOf_i0)   |
| [MistralGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i1)         |
| [OpenAIGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i2)          |
| [ToolCallLLMWrapper.json](#apu_anyOf_i0_llm_unit_anyOf_i3) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0"></a>7.1.2.2.5.1. Property `AnthropicLLMUnit.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./AnthropicLLMUnit.json                                              |

| Property                                                            | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i0_implementation ) | No      | const       | No         | -          | AnthropicLLMUnit   |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i0_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i0_temperature )       | No      | number      | No         | -          | Temperature        |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_args](#apu_anyOf_i0_llm_unit_anyOf_i0_client_args )       | No      | object      | No         | -          | Client Args        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_implementation"></a>7.1.2.2.5.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AnthropicLLMUnit

Specific value: `"AnthropicLLMUnit"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model"></a>7.1.2.2.5.1.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"claude-3-opus-20240229"`                                                |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i0_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i0_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model_implementation"></a>7.1.2.2.5.1.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_temperature"></a>7.1.2.2.5.1.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens"></a>7.1.2.2.5.1.4. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i0"></a>7.1.2.2.5.1.4.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i1"></a>7.1.2.2.5.1.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_client_args"></a>7.1.2.2.5.1.5. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1"></a>7.1.2.2.5.2. Property `MistralGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./MistralGPT.json                                                    |

| Property                                                            | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i1_implementation ) | No      | const       | No         | -          | MistralGPT         |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i1_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i1_temperature )       | No      | number      | No         | -          | Temperature        |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i1_force_json )         | No      | boolean     | No         | -          | Force Json         |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_args](#apu_anyOf_i0_llm_unit_anyOf_i1_client_args )       | No      | object      | No         | -          | Client Args        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_implementation"></a>7.1.2.2.5.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** MistralGPT

Specific value: `"MistralGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model"></a>7.1.2.2.5.2.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"mistral-large-latest"`                                                  |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i1_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i1_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model_implementation"></a>7.1.2.2.5.2.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_temperature"></a>7.1.2.2.5.2.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_force_json"></a>7.1.2.2.5.2.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens"></a>7.1.2.2.5.2.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i0"></a>7.1.2.2.5.2.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i1"></a>7.1.2.2.5.2.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_client_args"></a>7.1.2.2.5.2.6. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2"></a>7.1.2.2.5.3. Property `OpenAIGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./OpenAIGPT.json                                                     |

| Property                                                                    | Pattern | Type        | Deprecated | Definition | Title/Description                 |
| --------------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | --------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_implementation )         | No      | const       | No         | -          | OpenAIGPT                         |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i2_model )                           | No      | object      | No         | -          | LLMModel Reference                |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i2_temperature )               | No      | number      | No         | -          | Temperature                       |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i2_force_json )                 | No      | boolean     | No         | -          | Force Json                        |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens )                 | No      | Combination | No         | -          | Max Tokens                        |
| - [connection_handler](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler ) | No      | object      | No         | -          | OpenAIConnectionHandler Reference |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_implementation"></a>7.1.2.2.5.3.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OpenAIGPT

Specific value: `"OpenAIGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model"></a>7.1.2.2.5.3.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"gpt-4-turbo"`                                                           |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i2_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation"></a>7.1.2.2.5.3.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_temperature"></a>7.1.2.2.5.3.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_force_json"></a>7.1.2.2.5.3.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens"></a>7.1.2.2.5.3.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i0"></a>7.1.2.2.5.3.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i1"></a>7.1.2.2.5.3.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler"></a>7.1.2.2.5.3.6. Property `connection_handler`

**Title:** OpenAIConnectionHandler Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"OpenAIConnectionHandler"`                                               |

| Property                                                                               | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_implementation"></a>7.1.2.2.5.3.6.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3"></a>7.1.2.2.5.4. Property `ToolCallLLMWrapper.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./ToolCallLLMWrapper.json                                            |

| Property                                                                      | Pattern | Type        | Deprecated | Definition                                  | Title/Description                                                    |
| ----------------------------------------------------------------------------- | ------- | ----------- | ---------- | ------------------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_implementation )           | No      | const       | No         | -                                           | ToolCallLLMWrapper                                                   |
| - [tool_message_prompt](#apu_anyOf_i0_llm_unit_anyOf_i3_tool_message_prompt ) | No      | string      | No         | -                                           | Tool Message Prompt                                                  |
| - [llm_unit](#apu_anyOf_i0_llm_unit_anyOf_i3_llm_unit )                       | No      | object      | No         | Same as [llm_unit](#apu_anyOf_i0_llm_unit ) | Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i3_model )                             | No      | Combination | No         | -                                           | -                                                                    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_implementation"></a>7.1.2.2.5.4.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ToolCallLLMWrapper

Specific value: `"ToolCallLLMWrapper"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_tool_message_prompt"></a>7.1.2.2.5.4.2. Property `tool_message_prompt`

**Title:** Tool Message Prompt

|              |                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Required** | No                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Default**  | `"You must follow these instructions:\nYou can select zero or more of the above tools based on the user query\nIf there are multiple tools required, make sure a list of tools are returned in a JSON array.\nIf there is no tool that match the user request or you have already answered the question, you will respond with empty json array for the tools.\nYou can also add any additional notes or explanations in the notes field."` |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_llm_unit"></a>7.1.2.2.5.4.3. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Same definition as**    | [llm_unit](#apu_anyOf_i0_llm_unit)                                        |

**Description:** Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model"></a>7.1.2.2.5.4.4. Property `model`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                       |
| -------------------------------------------------------------------- |
| [LLMModel Reference](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i1)             |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0"></a>7.1.2.2.5.4.4.1. Property `LLMModel Reference`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.llm_unit.LLMModel"`                                  |

| Property                                                                           | Pattern | Type   | Deprecated | Definition | Title/Description |
| ---------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_implementation"></a>7.1.2.2.5.4.4.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i1"></a>7.1.2.2.5.4.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i1_logic_units"></a>7.1.2.2.6. Property `logic_units`

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

| Each item of this array must be                        | Description |
| ------------------------------------------------------ | ----------- |
| [LogicUnit Reference](#apu_anyOf_i1_logic_units_items) | -           |

###### <a name="autogenerated_heading_18"></a>7.1.2.2.6.1. LogicUnit Reference

**Title:** LogicUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.logic_unit.LogicUnit"`                               |

| Property                                                            | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i1_logic_units_items_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i1_logic_units_items_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i1_logic_units_items_implementation"></a>7.1.2.2.6.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i1_audio_unit"></a>7.1.2.2.7. Property `audio_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                           |
| -------------------------------------------------------- |
| [AudioUnit Reference](#apu_anyOf_i1_audio_unit_anyOf_i0) |
| [item 1](#apu_anyOf_i1_audio_unit_anyOf_i1)              |

###### <a name="apu_anyOf_i1_audio_unit_anyOf_i0"></a>7.1.2.2.7.1. Property `AudioUnit Reference`

**Title:** AudioUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.audio_unit.AudioUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i1_audio_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i1_audio_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i1_audio_unit_anyOf_i0_implementation"></a>7.1.2.2.7.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i1_audio_unit_anyOf_i1"></a>7.1.2.2.7.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i1_image_unit"></a>7.1.2.2.8. Property `image_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                           |
| -------------------------------------------------------- |
| [ImageUnit Reference](#apu_anyOf_i1_image_unit_anyOf_i0) |
| [item 1](#apu_anyOf_i1_image_unit_anyOf_i1)              |

###### <a name="apu_anyOf_i1_image_unit_anyOf_i0"></a>7.1.2.2.8.1. Property `ImageUnit Reference`

**Title:** ImageUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.image_unit.ImageUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i1_image_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i1_image_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i1_image_unit_anyOf_i0_implementation"></a>7.1.2.2.8.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i1_image_unit_anyOf_i1"></a>7.1.2.2.8.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i1_record_conversation"></a>7.1.2.2.9. Property `record_conversation`

**Title:** Record Conversation

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i1_allow_tool_errors"></a>7.1.2.2.10. Property `allow_tool_errors`

**Title:** Allow Tool Errors

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i1_document_processor"></a>7.1.2.2.11. Property `document_processor`

**Title:** DocumentProcessor Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"DocumentProcessor"`                                                     |

| Property                                                             | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i1_document_processor_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i1_document_processor_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i1_document_processor_implementation"></a>7.1.2.2.11.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i2"></a>7.1.2.3. Property `ClaudeSonnet.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./ClaudeSonnet.json                                                  |

| Property                                                          | Pattern | Type            | Deprecated | Definition                       | Title/Description                                                    |
| ----------------------------------------------------------------- | ------- | --------------- | ---------- | -------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i2_implementation )                 | No      | const           | No         | -                                | ClaudeSonnet                                                         |
| - [max_num_function_calls](#apu_anyOf_i2_max_num_function_calls ) | No      | integer         | No         | -                                | Max Num Function Calls                                               |
| - [io_unit](#apu_anyOf_i2_io_unit )                               | No      | object          | No         | -                                | IOUnit Reference                                                     |
| - [memory_unit](#apu_anyOf_i2_memory_unit )                       | No      | object          | No         | -                                | MemoryUnit Reference                                                 |
| - [llm_unit](#apu_anyOf_i2_llm_unit )                             | No      | object          | No         | In [LLMUnit](/docs/components/llmunit/overview) | Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components |
| - [logic_units](#apu_anyOf_i2_logic_units )                       | No      | array of object | No         | -                                | Logic Units                                                          |
| - [audio_unit](#apu_anyOf_i2_audio_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [image_unit](#apu_anyOf_i2_image_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [record_conversation](#apu_anyOf_i2_record_conversation )       | No      | boolean         | No         | -                                | Record Conversation                                                  |
| - [allow_tool_errors](#apu_anyOf_i2_allow_tool_errors )           | No      | boolean         | No         | -                                | Allow Tool Errors                                                    |
| - [document_processor](#apu_anyOf_i2_document_processor )         | No      | object          | No         | -                                | DocumentProcessor Reference                                          |

###### <a name="apu_anyOf_i2_implementation"></a>7.1.2.3.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ClaudeSonnet

Specific value: `"ClaudeSonnet"`

###### <a name="apu_anyOf_i2_max_num_function_calls"></a>7.1.2.3.2. Property `max_num_function_calls`

**Title:** Max Num Function Calls

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `10`      |

**Description:** The maximum number of function calls to make in a single request.

###### <a name="apu_anyOf_i2_io_unit"></a>7.1.2.3.3. Property `io_unit`

**Title:** IOUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"IOUnit"`                                                                |

| Property                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i2_io_unit_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i2_io_unit_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i2_io_unit_implementation"></a>7.1.2.3.3.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i2_memory_unit"></a>7.1.2.3.4. Property `memory_unit`

**Title:** MemoryUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"MemoryUnit"`                                                            |

| Property                                                      | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i2_memory_unit_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i2_memory_unit_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i2_memory_unit_implementation"></a>7.1.2.3.4.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i2_llm_unit"></a>7.1.2.3.5. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Defined in**            | [LLMUnit](/docs/components/llmunit/overview)                                             |

**Description:** Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components

| Any of(Option)                                             |
| ---------------------------------------------------------- |
| [AnthropicLLMUnit.json](#apu_anyOf_i0_llm_unit_anyOf_i0)   |
| [MistralGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i1)         |
| [OpenAIGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i2)          |
| [ToolCallLLMWrapper.json](#apu_anyOf_i0_llm_unit_anyOf_i3) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0"></a>7.1.2.3.5.1. Property `AnthropicLLMUnit.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./AnthropicLLMUnit.json                                              |

| Property                                                            | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i0_implementation ) | No      | const       | No         | -          | AnthropicLLMUnit   |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i0_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i0_temperature )       | No      | number      | No         | -          | Temperature        |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_args](#apu_anyOf_i0_llm_unit_anyOf_i0_client_args )       | No      | object      | No         | -          | Client Args        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_implementation"></a>7.1.2.3.5.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AnthropicLLMUnit

Specific value: `"AnthropicLLMUnit"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model"></a>7.1.2.3.5.1.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"claude-3-opus-20240229"`                                                |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i0_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i0_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model_implementation"></a>7.1.2.3.5.1.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_temperature"></a>7.1.2.3.5.1.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens"></a>7.1.2.3.5.1.4. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i0"></a>7.1.2.3.5.1.4.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i1"></a>7.1.2.3.5.1.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_client_args"></a>7.1.2.3.5.1.5. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1"></a>7.1.2.3.5.2. Property `MistralGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./MistralGPT.json                                                    |

| Property                                                            | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i1_implementation ) | No      | const       | No         | -          | MistralGPT         |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i1_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i1_temperature )       | No      | number      | No         | -          | Temperature        |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i1_force_json )         | No      | boolean     | No         | -          | Force Json         |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_args](#apu_anyOf_i0_llm_unit_anyOf_i1_client_args )       | No      | object      | No         | -          | Client Args        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_implementation"></a>7.1.2.3.5.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** MistralGPT

Specific value: `"MistralGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model"></a>7.1.2.3.5.2.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"mistral-large-latest"`                                                  |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i1_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i1_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model_implementation"></a>7.1.2.3.5.2.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_temperature"></a>7.1.2.3.5.2.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_force_json"></a>7.1.2.3.5.2.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens"></a>7.1.2.3.5.2.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i0"></a>7.1.2.3.5.2.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i1"></a>7.1.2.3.5.2.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_client_args"></a>7.1.2.3.5.2.6. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2"></a>7.1.2.3.5.3. Property `OpenAIGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./OpenAIGPT.json                                                     |

| Property                                                                    | Pattern | Type        | Deprecated | Definition | Title/Description                 |
| --------------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | --------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_implementation )         | No      | const       | No         | -          | OpenAIGPT                         |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i2_model )                           | No      | object      | No         | -          | LLMModel Reference                |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i2_temperature )               | No      | number      | No         | -          | Temperature                       |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i2_force_json )                 | No      | boolean     | No         | -          | Force Json                        |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens )                 | No      | Combination | No         | -          | Max Tokens                        |
| - [connection_handler](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler ) | No      | object      | No         | -          | OpenAIConnectionHandler Reference |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_implementation"></a>7.1.2.3.5.3.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OpenAIGPT

Specific value: `"OpenAIGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model"></a>7.1.2.3.5.3.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"gpt-4-turbo"`                                                           |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i2_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation"></a>7.1.2.3.5.3.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_temperature"></a>7.1.2.3.5.3.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_force_json"></a>7.1.2.3.5.3.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens"></a>7.1.2.3.5.3.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i0"></a>7.1.2.3.5.3.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i1"></a>7.1.2.3.5.3.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler"></a>7.1.2.3.5.3.6. Property `connection_handler`

**Title:** OpenAIConnectionHandler Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"OpenAIConnectionHandler"`                                               |

| Property                                                                               | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_implementation"></a>7.1.2.3.5.3.6.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3"></a>7.1.2.3.5.4. Property `ToolCallLLMWrapper.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./ToolCallLLMWrapper.json                                            |

| Property                                                                      | Pattern | Type        | Deprecated | Definition                                  | Title/Description                                                    |
| ----------------------------------------------------------------------------- | ------- | ----------- | ---------- | ------------------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_implementation )           | No      | const       | No         | -                                           | ToolCallLLMWrapper                                                   |
| - [tool_message_prompt](#apu_anyOf_i0_llm_unit_anyOf_i3_tool_message_prompt ) | No      | string      | No         | -                                           | Tool Message Prompt                                                  |
| - [llm_unit](#apu_anyOf_i0_llm_unit_anyOf_i3_llm_unit )                       | No      | object      | No         | Same as [llm_unit](#apu_anyOf_i0_llm_unit ) | Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i3_model )                             | No      | Combination | No         | -                                           | -                                                                    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_implementation"></a>7.1.2.3.5.4.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ToolCallLLMWrapper

Specific value: `"ToolCallLLMWrapper"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_tool_message_prompt"></a>7.1.2.3.5.4.2. Property `tool_message_prompt`

**Title:** Tool Message Prompt

|              |                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Required** | No                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Default**  | `"You must follow these instructions:\nYou can select zero or more of the above tools based on the user query\nIf there are multiple tools required, make sure a list of tools are returned in a JSON array.\nIf there is no tool that match the user request or you have already answered the question, you will respond with empty json array for the tools.\nYou can also add any additional notes or explanations in the notes field."` |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_llm_unit"></a>7.1.2.3.5.4.3. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Same definition as**    | [llm_unit](#apu_anyOf_i0_llm_unit)                                        |

**Description:** Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model"></a>7.1.2.3.5.4.4. Property `model`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                       |
| -------------------------------------------------------------------- |
| [LLMModel Reference](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i1)             |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0"></a>7.1.2.3.5.4.4.1. Property `LLMModel Reference`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.llm_unit.LLMModel"`                                  |

| Property                                                                           | Pattern | Type   | Deprecated | Definition | Title/Description |
| ---------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_implementation"></a>7.1.2.3.5.4.4.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i1"></a>7.1.2.3.5.4.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i2_logic_units"></a>7.1.2.3.6. Property `logic_units`

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

| Each item of this array must be                        | Description |
| ------------------------------------------------------ | ----------- |
| [LogicUnit Reference](#apu_anyOf_i2_logic_units_items) | -           |

###### <a name="autogenerated_heading_19"></a>7.1.2.3.6.1. LogicUnit Reference

**Title:** LogicUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.logic_unit.LogicUnit"`                               |

| Property                                                            | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i2_logic_units_items_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i2_logic_units_items_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i2_logic_units_items_implementation"></a>7.1.2.3.6.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i2_audio_unit"></a>7.1.2.3.7. Property `audio_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                           |
| -------------------------------------------------------- |
| [AudioUnit Reference](#apu_anyOf_i2_audio_unit_anyOf_i0) |
| [item 1](#apu_anyOf_i2_audio_unit_anyOf_i1)              |

###### <a name="apu_anyOf_i2_audio_unit_anyOf_i0"></a>7.1.2.3.7.1. Property `AudioUnit Reference`

**Title:** AudioUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.audio_unit.AudioUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i2_audio_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i2_audio_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i2_audio_unit_anyOf_i0_implementation"></a>7.1.2.3.7.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i2_audio_unit_anyOf_i1"></a>7.1.2.3.7.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i2_image_unit"></a>7.1.2.3.8. Property `image_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                           |
| -------------------------------------------------------- |
| [ImageUnit Reference](#apu_anyOf_i2_image_unit_anyOf_i0) |
| [item 1](#apu_anyOf_i2_image_unit_anyOf_i1)              |

###### <a name="apu_anyOf_i2_image_unit_anyOf_i0"></a>7.1.2.3.8.1. Property `ImageUnit Reference`

**Title:** ImageUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.image_unit.ImageUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i2_image_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i2_image_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i2_image_unit_anyOf_i0_implementation"></a>7.1.2.3.8.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i2_image_unit_anyOf_i1"></a>7.1.2.3.8.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i2_record_conversation"></a>7.1.2.3.9. Property `record_conversation`

**Title:** Record Conversation

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i2_allow_tool_errors"></a>7.1.2.3.10. Property `allow_tool_errors`

**Title:** Allow Tool Errors

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i2_document_processor"></a>7.1.2.3.11. Property `document_processor`

**Title:** DocumentProcessor Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"DocumentProcessor"`                                                     |

| Property                                                             | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i2_document_processor_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i2_document_processor_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i2_document_processor_implementation"></a>7.1.2.3.11.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i3"></a>7.1.2.4. Property `ConversationalAPU.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./ConversationalAPU.json                                             |

| Property                                                          | Pattern | Type            | Deprecated | Definition                       | Title/Description                                                    |
| ----------------------------------------------------------------- | ------- | --------------- | ---------- | -------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i3_implementation )                 | No      | const           | No         | -                                | ConversationalAPU                                                    |
| - [max_num_function_calls](#apu_anyOf_i3_max_num_function_calls ) | No      | integer         | No         | -                                | Max Num Function Calls                                               |
| - [io_unit](#apu_anyOf_i3_io_unit )                               | No      | object          | No         | -                                | IOUnit Reference                                                     |
| - [memory_unit](#apu_anyOf_i3_memory_unit )                       | No      | object          | No         | -                                | MemoryUnit Reference                                                 |
| - [llm_unit](#apu_anyOf_i3_llm_unit )                             | No      | object          | No         | In [LLMUnit](/docs/components/llmunit/overview) | Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components |
| - [logic_units](#apu_anyOf_i3_logic_units )                       | No      | array of object | No         | -                                | Logic Units                                                          |
| - [audio_unit](#apu_anyOf_i3_audio_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [image_unit](#apu_anyOf_i3_image_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [record_conversation](#apu_anyOf_i3_record_conversation )       | No      | boolean         | No         | -                                | Record Conversation                                                  |
| - [allow_tool_errors](#apu_anyOf_i3_allow_tool_errors )           | No      | boolean         | No         | -                                | Allow Tool Errors                                                    |
| - [document_processor](#apu_anyOf_i3_document_processor )         | No      | object          | No         | -                                | DocumentProcessor Reference                                          |

###### <a name="apu_anyOf_i3_implementation"></a>7.1.2.4.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ConversationalAPU

Specific value: `"ConversationalAPU"`

###### <a name="apu_anyOf_i3_max_num_function_calls"></a>7.1.2.4.2. Property `max_num_function_calls`

**Title:** Max Num Function Calls

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `10`      |

**Description:** The maximum number of function calls to make in a single request.

###### <a name="apu_anyOf_i3_io_unit"></a>7.1.2.4.3. Property `io_unit`

**Title:** IOUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"IOUnit"`                                                                |

| Property                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i3_io_unit_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i3_io_unit_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i3_io_unit_implementation"></a>7.1.2.4.3.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i3_memory_unit"></a>7.1.2.4.4. Property `memory_unit`

**Title:** MemoryUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"MemoryUnit"`                                                            |

| Property                                                      | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i3_memory_unit_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i3_memory_unit_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i3_memory_unit_implementation"></a>7.1.2.4.4.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i3_llm_unit"></a>7.1.2.4.5. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Defined in**            | [LLMUnit](/docs/components/llmunit/overview)                                             |

**Description:** Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components

| Any of(Option)                                             |
| ---------------------------------------------------------- |
| [AnthropicLLMUnit.json](#apu_anyOf_i0_llm_unit_anyOf_i0)   |
| [MistralGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i1)         |
| [OpenAIGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i2)          |
| [ToolCallLLMWrapper.json](#apu_anyOf_i0_llm_unit_anyOf_i3) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0"></a>7.1.2.4.5.1. Property `AnthropicLLMUnit.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./AnthropicLLMUnit.json                                              |

| Property                                                            | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i0_implementation ) | No      | const       | No         | -          | AnthropicLLMUnit   |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i0_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i0_temperature )       | No      | number      | No         | -          | Temperature        |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_args](#apu_anyOf_i0_llm_unit_anyOf_i0_client_args )       | No      | object      | No         | -          | Client Args        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_implementation"></a>7.1.2.4.5.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AnthropicLLMUnit

Specific value: `"AnthropicLLMUnit"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model"></a>7.1.2.4.5.1.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"claude-3-opus-20240229"`                                                |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i0_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i0_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model_implementation"></a>7.1.2.4.5.1.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_temperature"></a>7.1.2.4.5.1.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens"></a>7.1.2.4.5.1.4. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i0"></a>7.1.2.4.5.1.4.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i1"></a>7.1.2.4.5.1.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_client_args"></a>7.1.2.4.5.1.5. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1"></a>7.1.2.4.5.2. Property `MistralGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./MistralGPT.json                                                    |

| Property                                                            | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i1_implementation ) | No      | const       | No         | -          | MistralGPT         |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i1_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i1_temperature )       | No      | number      | No         | -          | Temperature        |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i1_force_json )         | No      | boolean     | No         | -          | Force Json         |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_args](#apu_anyOf_i0_llm_unit_anyOf_i1_client_args )       | No      | object      | No         | -          | Client Args        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_implementation"></a>7.1.2.4.5.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** MistralGPT

Specific value: `"MistralGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model"></a>7.1.2.4.5.2.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"mistral-large-latest"`                                                  |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i1_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i1_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model_implementation"></a>7.1.2.4.5.2.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_temperature"></a>7.1.2.4.5.2.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_force_json"></a>7.1.2.4.5.2.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens"></a>7.1.2.4.5.2.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i0"></a>7.1.2.4.5.2.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i1"></a>7.1.2.4.5.2.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_client_args"></a>7.1.2.4.5.2.6. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2"></a>7.1.2.4.5.3. Property `OpenAIGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./OpenAIGPT.json                                                     |

| Property                                                                    | Pattern | Type        | Deprecated | Definition | Title/Description                 |
| --------------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | --------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_implementation )         | No      | const       | No         | -          | OpenAIGPT                         |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i2_model )                           | No      | object      | No         | -          | LLMModel Reference                |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i2_temperature )               | No      | number      | No         | -          | Temperature                       |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i2_force_json )                 | No      | boolean     | No         | -          | Force Json                        |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens )                 | No      | Combination | No         | -          | Max Tokens                        |
| - [connection_handler](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler ) | No      | object      | No         | -          | OpenAIConnectionHandler Reference |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_implementation"></a>7.1.2.4.5.3.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OpenAIGPT

Specific value: `"OpenAIGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model"></a>7.1.2.4.5.3.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"gpt-4-turbo"`                                                           |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i2_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation"></a>7.1.2.4.5.3.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_temperature"></a>7.1.2.4.5.3.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_force_json"></a>7.1.2.4.5.3.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens"></a>7.1.2.4.5.3.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i0"></a>7.1.2.4.5.3.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i1"></a>7.1.2.4.5.3.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler"></a>7.1.2.4.5.3.6. Property `connection_handler`

**Title:** OpenAIConnectionHandler Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"OpenAIConnectionHandler"`                                               |

| Property                                                                               | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_implementation"></a>7.1.2.4.5.3.6.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3"></a>7.1.2.4.5.4. Property `ToolCallLLMWrapper.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./ToolCallLLMWrapper.json                                            |

| Property                                                                      | Pattern | Type        | Deprecated | Definition                                  | Title/Description                                                    |
| ----------------------------------------------------------------------------- | ------- | ----------- | ---------- | ------------------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_implementation )           | No      | const       | No         | -                                           | ToolCallLLMWrapper                                                   |
| - [tool_message_prompt](#apu_anyOf_i0_llm_unit_anyOf_i3_tool_message_prompt ) | No      | string      | No         | -                                           | Tool Message Prompt                                                  |
| - [llm_unit](#apu_anyOf_i0_llm_unit_anyOf_i3_llm_unit )                       | No      | object      | No         | Same as [llm_unit](#apu_anyOf_i0_llm_unit ) | Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i3_model )                             | No      | Combination | No         | -                                           | -                                                                    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_implementation"></a>7.1.2.4.5.4.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ToolCallLLMWrapper

Specific value: `"ToolCallLLMWrapper"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_tool_message_prompt"></a>7.1.2.4.5.4.2. Property `tool_message_prompt`

**Title:** Tool Message Prompt

|              |                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Required** | No                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Default**  | `"You must follow these instructions:\nYou can select zero or more of the above tools based on the user query\nIf there are multiple tools required, make sure a list of tools are returned in a JSON array.\nIf there is no tool that match the user request or you have already answered the question, you will respond with empty json array for the tools.\nYou can also add any additional notes or explanations in the notes field."` |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_llm_unit"></a>7.1.2.4.5.4.3. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Same definition as**    | [llm_unit](#apu_anyOf_i0_llm_unit)                                        |

**Description:** Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model"></a>7.1.2.4.5.4.4. Property `model`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                       |
| -------------------------------------------------------------------- |
| [LLMModel Reference](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i1)             |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0"></a>7.1.2.4.5.4.4.1. Property `LLMModel Reference`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.llm_unit.LLMModel"`                                  |

| Property                                                                           | Pattern | Type   | Deprecated | Definition | Title/Description |
| ---------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_implementation"></a>7.1.2.4.5.4.4.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i1"></a>7.1.2.4.5.4.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i3_logic_units"></a>7.1.2.4.6. Property `logic_units`

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

| Each item of this array must be                        | Description |
| ------------------------------------------------------ | ----------- |
| [LogicUnit Reference](#apu_anyOf_i3_logic_units_items) | -           |

###### <a name="autogenerated_heading_20"></a>7.1.2.4.6.1. LogicUnit Reference

**Title:** LogicUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.logic_unit.LogicUnit"`                               |

| Property                                                            | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i3_logic_units_items_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i3_logic_units_items_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i3_logic_units_items_implementation"></a>7.1.2.4.6.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i3_audio_unit"></a>7.1.2.4.7. Property `audio_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                           |
| -------------------------------------------------------- |
| [AudioUnit Reference](#apu_anyOf_i3_audio_unit_anyOf_i0) |
| [item 1](#apu_anyOf_i3_audio_unit_anyOf_i1)              |

###### <a name="apu_anyOf_i3_audio_unit_anyOf_i0"></a>7.1.2.4.7.1. Property `AudioUnit Reference`

**Title:** AudioUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.audio_unit.AudioUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i3_audio_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i3_audio_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i3_audio_unit_anyOf_i0_implementation"></a>7.1.2.4.7.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i3_audio_unit_anyOf_i1"></a>7.1.2.4.7.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i3_image_unit"></a>7.1.2.4.8. Property `image_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                           |
| -------------------------------------------------------- |
| [ImageUnit Reference](#apu_anyOf_i3_image_unit_anyOf_i0) |
| [item 1](#apu_anyOf_i3_image_unit_anyOf_i1)              |

###### <a name="apu_anyOf_i3_image_unit_anyOf_i0"></a>7.1.2.4.8.1. Property `ImageUnit Reference`

**Title:** ImageUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.image_unit.ImageUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i3_image_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i3_image_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i3_image_unit_anyOf_i0_implementation"></a>7.1.2.4.8.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i3_image_unit_anyOf_i1"></a>7.1.2.4.8.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i3_record_conversation"></a>7.1.2.4.9. Property `record_conversation`

**Title:** Record Conversation

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i3_allow_tool_errors"></a>7.1.2.4.10. Property `allow_tool_errors`

**Title:** Allow Tool Errors

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i3_document_processor"></a>7.1.2.4.11. Property `document_processor`

**Title:** DocumentProcessor Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"DocumentProcessor"`                                                     |

| Property                                                             | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i3_document_processor_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i3_document_processor_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i3_document_processor_implementation"></a>7.1.2.4.11.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i4"></a>7.1.2.5. Property `GPT3.5-turbo.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./GPT3.5-turbo.json                                                  |

| Property                                                          | Pattern | Type            | Deprecated | Definition                       | Title/Description                                                    |
| ----------------------------------------------------------------- | ------- | --------------- | ---------- | -------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i4_implementation )                 | No      | const           | No         | -                                | GPT3.5-turbo                                                         |
| - [max_num_function_calls](#apu_anyOf_i4_max_num_function_calls ) | No      | integer         | No         | -                                | Max Num Function Calls                                               |
| - [io_unit](#apu_anyOf_i4_io_unit )                               | No      | object          | No         | -                                | IOUnit Reference                                                     |
| - [memory_unit](#apu_anyOf_i4_memory_unit )                       | No      | object          | No         | -                                | MemoryUnit Reference                                                 |
| - [llm_unit](#apu_anyOf_i4_llm_unit )                             | No      | object          | No         | In [LLMUnit](/docs/components/llmunit/overview) | Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components |
| - [logic_units](#apu_anyOf_i4_logic_units )                       | No      | array of object | No         | -                                | Logic Units                                                          |
| - [audio_unit](#apu_anyOf_i4_audio_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [image_unit](#apu_anyOf_i4_image_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [record_conversation](#apu_anyOf_i4_record_conversation )       | No      | boolean         | No         | -                                | Record Conversation                                                  |
| - [allow_tool_errors](#apu_anyOf_i4_allow_tool_errors )           | No      | boolean         | No         | -                                | Allow Tool Errors                                                    |
| - [document_processor](#apu_anyOf_i4_document_processor )         | No      | object          | No         | -                                | DocumentProcessor Reference                                          |

###### <a name="apu_anyOf_i4_implementation"></a>7.1.2.5.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** GPT3.5-turbo

Specific value: `"GPT3.5-turbo"`

###### <a name="apu_anyOf_i4_max_num_function_calls"></a>7.1.2.5.2. Property `max_num_function_calls`

**Title:** Max Num Function Calls

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `10`      |

**Description:** The maximum number of function calls to make in a single request.

###### <a name="apu_anyOf_i4_io_unit"></a>7.1.2.5.3. Property `io_unit`

**Title:** IOUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"IOUnit"`                                                                |

| Property                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i4_io_unit_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i4_io_unit_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i4_io_unit_implementation"></a>7.1.2.5.3.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i4_memory_unit"></a>7.1.2.5.4. Property `memory_unit`

**Title:** MemoryUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"MemoryUnit"`                                                            |

| Property                                                      | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i4_memory_unit_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i4_memory_unit_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i4_memory_unit_implementation"></a>7.1.2.5.4.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i4_llm_unit"></a>7.1.2.5.5. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Defined in**            | [LLMUnit](/docs/components/llmunit/overview)                                             |

**Description:** Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components

| Any of(Option)                                             |
| ---------------------------------------------------------- |
| [AnthropicLLMUnit.json](#apu_anyOf_i0_llm_unit_anyOf_i0)   |
| [MistralGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i1)         |
| [OpenAIGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i2)          |
| [ToolCallLLMWrapper.json](#apu_anyOf_i0_llm_unit_anyOf_i3) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0"></a>7.1.2.5.5.1. Property `AnthropicLLMUnit.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./AnthropicLLMUnit.json                                              |

| Property                                                            | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i0_implementation ) | No      | const       | No         | -          | AnthropicLLMUnit   |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i0_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i0_temperature )       | No      | number      | No         | -          | Temperature        |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_args](#apu_anyOf_i0_llm_unit_anyOf_i0_client_args )       | No      | object      | No         | -          | Client Args        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_implementation"></a>7.1.2.5.5.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AnthropicLLMUnit

Specific value: `"AnthropicLLMUnit"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model"></a>7.1.2.5.5.1.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"claude-3-opus-20240229"`                                                |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i0_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i0_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model_implementation"></a>7.1.2.5.5.1.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_temperature"></a>7.1.2.5.5.1.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens"></a>7.1.2.5.5.1.4. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i0"></a>7.1.2.5.5.1.4.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i1"></a>7.1.2.5.5.1.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_client_args"></a>7.1.2.5.5.1.5. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1"></a>7.1.2.5.5.2. Property `MistralGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./MistralGPT.json                                                    |

| Property                                                            | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i1_implementation ) | No      | const       | No         | -          | MistralGPT         |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i1_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i1_temperature )       | No      | number      | No         | -          | Temperature        |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i1_force_json )         | No      | boolean     | No         | -          | Force Json         |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_args](#apu_anyOf_i0_llm_unit_anyOf_i1_client_args )       | No      | object      | No         | -          | Client Args        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_implementation"></a>7.1.2.5.5.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** MistralGPT

Specific value: `"MistralGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model"></a>7.1.2.5.5.2.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"mistral-large-latest"`                                                  |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i1_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i1_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model_implementation"></a>7.1.2.5.5.2.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_temperature"></a>7.1.2.5.5.2.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_force_json"></a>7.1.2.5.5.2.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens"></a>7.1.2.5.5.2.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i0"></a>7.1.2.5.5.2.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i1"></a>7.1.2.5.5.2.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_client_args"></a>7.1.2.5.5.2.6. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2"></a>7.1.2.5.5.3. Property `OpenAIGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./OpenAIGPT.json                                                     |

| Property                                                                    | Pattern | Type        | Deprecated | Definition | Title/Description                 |
| --------------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | --------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_implementation )         | No      | const       | No         | -          | OpenAIGPT                         |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i2_model )                           | No      | object      | No         | -          | LLMModel Reference                |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i2_temperature )               | No      | number      | No         | -          | Temperature                       |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i2_force_json )                 | No      | boolean     | No         | -          | Force Json                        |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens )                 | No      | Combination | No         | -          | Max Tokens                        |
| - [connection_handler](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler ) | No      | object      | No         | -          | OpenAIConnectionHandler Reference |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_implementation"></a>7.1.2.5.5.3.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OpenAIGPT

Specific value: `"OpenAIGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model"></a>7.1.2.5.5.3.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"gpt-4-turbo"`                                                           |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i2_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation"></a>7.1.2.5.5.3.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_temperature"></a>7.1.2.5.5.3.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_force_json"></a>7.1.2.5.5.3.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens"></a>7.1.2.5.5.3.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i0"></a>7.1.2.5.5.3.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i1"></a>7.1.2.5.5.3.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler"></a>7.1.2.5.5.3.6. Property `connection_handler`

**Title:** OpenAIConnectionHandler Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"OpenAIConnectionHandler"`                                               |

| Property                                                                               | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_implementation"></a>7.1.2.5.5.3.6.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3"></a>7.1.2.5.5.4. Property `ToolCallLLMWrapper.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./ToolCallLLMWrapper.json                                            |

| Property                                                                      | Pattern | Type        | Deprecated | Definition                                  | Title/Description                                                    |
| ----------------------------------------------------------------------------- | ------- | ----------- | ---------- | ------------------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_implementation )           | No      | const       | No         | -                                           | ToolCallLLMWrapper                                                   |
| - [tool_message_prompt](#apu_anyOf_i0_llm_unit_anyOf_i3_tool_message_prompt ) | No      | string      | No         | -                                           | Tool Message Prompt                                                  |
| - [llm_unit](#apu_anyOf_i0_llm_unit_anyOf_i3_llm_unit )                       | No      | object      | No         | Same as [llm_unit](#apu_anyOf_i0_llm_unit ) | Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i3_model )                             | No      | Combination | No         | -                                           | -                                                                    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_implementation"></a>7.1.2.5.5.4.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ToolCallLLMWrapper

Specific value: `"ToolCallLLMWrapper"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_tool_message_prompt"></a>7.1.2.5.5.4.2. Property `tool_message_prompt`

**Title:** Tool Message Prompt

|              |                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Required** | No                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Default**  | `"You must follow these instructions:\nYou can select zero or more of the above tools based on the user query\nIf there are multiple tools required, make sure a list of tools are returned in a JSON array.\nIf there is no tool that match the user request or you have already answered the question, you will respond with empty json array for the tools.\nYou can also add any additional notes or explanations in the notes field."` |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_llm_unit"></a>7.1.2.5.5.4.3. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Same definition as**    | [llm_unit](#apu_anyOf_i0_llm_unit)                                        |

**Description:** Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model"></a>7.1.2.5.5.4.4. Property `model`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                       |
| -------------------------------------------------------------------- |
| [LLMModel Reference](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i1)             |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0"></a>7.1.2.5.5.4.4.1. Property `LLMModel Reference`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.llm_unit.LLMModel"`                                  |

| Property                                                                           | Pattern | Type   | Deprecated | Definition | Title/Description |
| ---------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_implementation"></a>7.1.2.5.5.4.4.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i1"></a>7.1.2.5.5.4.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i4_logic_units"></a>7.1.2.5.6. Property `logic_units`

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

| Each item of this array must be                        | Description |
| ------------------------------------------------------ | ----------- |
| [LogicUnit Reference](#apu_anyOf_i4_logic_units_items) | -           |

###### <a name="autogenerated_heading_21"></a>7.1.2.5.6.1. LogicUnit Reference

**Title:** LogicUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.logic_unit.LogicUnit"`                               |

| Property                                                            | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i4_logic_units_items_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i4_logic_units_items_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i4_logic_units_items_implementation"></a>7.1.2.5.6.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i4_audio_unit"></a>7.1.2.5.7. Property `audio_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                           |
| -------------------------------------------------------- |
| [AudioUnit Reference](#apu_anyOf_i4_audio_unit_anyOf_i0) |
| [item 1](#apu_anyOf_i4_audio_unit_anyOf_i1)              |

###### <a name="apu_anyOf_i4_audio_unit_anyOf_i0"></a>7.1.2.5.7.1. Property `AudioUnit Reference`

**Title:** AudioUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.audio_unit.AudioUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i4_audio_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i4_audio_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i4_audio_unit_anyOf_i0_implementation"></a>7.1.2.5.7.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i4_audio_unit_anyOf_i1"></a>7.1.2.5.7.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i4_image_unit"></a>7.1.2.5.8. Property `image_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                           |
| -------------------------------------------------------- |
| [ImageUnit Reference](#apu_anyOf_i4_image_unit_anyOf_i0) |
| [item 1](#apu_anyOf_i4_image_unit_anyOf_i1)              |

###### <a name="apu_anyOf_i4_image_unit_anyOf_i0"></a>7.1.2.5.8.1. Property `ImageUnit Reference`

**Title:** ImageUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.image_unit.ImageUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i4_image_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i4_image_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i4_image_unit_anyOf_i0_implementation"></a>7.1.2.5.8.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i4_image_unit_anyOf_i1"></a>7.1.2.5.8.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i4_record_conversation"></a>7.1.2.5.9. Property `record_conversation`

**Title:** Record Conversation

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i4_allow_tool_errors"></a>7.1.2.5.10. Property `allow_tool_errors`

**Title:** Allow Tool Errors

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i4_document_processor"></a>7.1.2.5.11. Property `document_processor`

**Title:** DocumentProcessor Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"DocumentProcessor"`                                                     |

| Property                                                             | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i4_document_processor_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i4_document_processor_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i4_document_processor_implementation"></a>7.1.2.5.11.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i5"></a>7.1.2.6. Property `GPT4-turbo.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./GPT4-turbo.json                                                    |

| Property                                                          | Pattern | Type            | Deprecated | Definition                       | Title/Description                                                    |
| ----------------------------------------------------------------- | ------- | --------------- | ---------- | -------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i5_implementation )                 | No      | const           | No         | -                                | GPT4-turbo                                                           |
| - [max_num_function_calls](#apu_anyOf_i5_max_num_function_calls ) | No      | integer         | No         | -                                | Max Num Function Calls                                               |
| - [io_unit](#apu_anyOf_i5_io_unit )                               | No      | object          | No         | -                                | IOUnit Reference                                                     |
| - [memory_unit](#apu_anyOf_i5_memory_unit )                       | No      | object          | No         | -                                | MemoryUnit Reference                                                 |
| - [llm_unit](#apu_anyOf_i5_llm_unit )                             | No      | object          | No         | In [LLMUnit](/docs/components/llmunit/overview) | Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components |
| - [logic_units](#apu_anyOf_i5_logic_units )                       | No      | array of object | No         | -                                | Logic Units                                                          |
| - [audio_unit](#apu_anyOf_i5_audio_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [image_unit](#apu_anyOf_i5_image_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [record_conversation](#apu_anyOf_i5_record_conversation )       | No      | boolean         | No         | -                                | Record Conversation                                                  |
| - [allow_tool_errors](#apu_anyOf_i5_allow_tool_errors )           | No      | boolean         | No         | -                                | Allow Tool Errors                                                    |
| - [document_processor](#apu_anyOf_i5_document_processor )         | No      | object          | No         | -                                | DocumentProcessor Reference                                          |

###### <a name="apu_anyOf_i5_implementation"></a>7.1.2.6.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** GPT4-turbo

Specific value: `"GPT4-turbo"`

###### <a name="apu_anyOf_i5_max_num_function_calls"></a>7.1.2.6.2. Property `max_num_function_calls`

**Title:** Max Num Function Calls

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `10`      |

**Description:** The maximum number of function calls to make in a single request.

###### <a name="apu_anyOf_i5_io_unit"></a>7.1.2.6.3. Property `io_unit`

**Title:** IOUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"IOUnit"`                                                                |

| Property                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i5_io_unit_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i5_io_unit_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i5_io_unit_implementation"></a>7.1.2.6.3.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i5_memory_unit"></a>7.1.2.6.4. Property `memory_unit`

**Title:** MemoryUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"MemoryUnit"`                                                            |

| Property                                                      | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i5_memory_unit_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i5_memory_unit_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i5_memory_unit_implementation"></a>7.1.2.6.4.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i5_llm_unit"></a>7.1.2.6.5. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Defined in**            | [LLMUnit](/docs/components/llmunit/overview)                                             |

**Description:** Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components

| Any of(Option)                                             |
| ---------------------------------------------------------- |
| [AnthropicLLMUnit.json](#apu_anyOf_i0_llm_unit_anyOf_i0)   |
| [MistralGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i1)         |
| [OpenAIGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i2)          |
| [ToolCallLLMWrapper.json](#apu_anyOf_i0_llm_unit_anyOf_i3) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0"></a>7.1.2.6.5.1. Property `AnthropicLLMUnit.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./AnthropicLLMUnit.json                                              |

| Property                                                            | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i0_implementation ) | No      | const       | No         | -          | AnthropicLLMUnit   |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i0_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i0_temperature )       | No      | number      | No         | -          | Temperature        |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_args](#apu_anyOf_i0_llm_unit_anyOf_i0_client_args )       | No      | object      | No         | -          | Client Args        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_implementation"></a>7.1.2.6.5.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AnthropicLLMUnit

Specific value: `"AnthropicLLMUnit"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model"></a>7.1.2.6.5.1.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"claude-3-opus-20240229"`                                                |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i0_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i0_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model_implementation"></a>7.1.2.6.5.1.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_temperature"></a>7.1.2.6.5.1.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens"></a>7.1.2.6.5.1.4. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i0"></a>7.1.2.6.5.1.4.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i1"></a>7.1.2.6.5.1.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_client_args"></a>7.1.2.6.5.1.5. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1"></a>7.1.2.6.5.2. Property `MistralGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./MistralGPT.json                                                    |

| Property                                                            | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i1_implementation ) | No      | const       | No         | -          | MistralGPT         |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i1_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i1_temperature )       | No      | number      | No         | -          | Temperature        |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i1_force_json )         | No      | boolean     | No         | -          | Force Json         |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_args](#apu_anyOf_i0_llm_unit_anyOf_i1_client_args )       | No      | object      | No         | -          | Client Args        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_implementation"></a>7.1.2.6.5.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** MistralGPT

Specific value: `"MistralGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model"></a>7.1.2.6.5.2.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"mistral-large-latest"`                                                  |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i1_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i1_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model_implementation"></a>7.1.2.6.5.2.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_temperature"></a>7.1.2.6.5.2.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_force_json"></a>7.1.2.6.5.2.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens"></a>7.1.2.6.5.2.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i0"></a>7.1.2.6.5.2.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i1"></a>7.1.2.6.5.2.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_client_args"></a>7.1.2.6.5.2.6. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2"></a>7.1.2.6.5.3. Property `OpenAIGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./OpenAIGPT.json                                                     |

| Property                                                                    | Pattern | Type        | Deprecated | Definition | Title/Description                 |
| --------------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | --------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_implementation )         | No      | const       | No         | -          | OpenAIGPT                         |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i2_model )                           | No      | object      | No         | -          | LLMModel Reference                |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i2_temperature )               | No      | number      | No         | -          | Temperature                       |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i2_force_json )                 | No      | boolean     | No         | -          | Force Json                        |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens )                 | No      | Combination | No         | -          | Max Tokens                        |
| - [connection_handler](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler ) | No      | object      | No         | -          | OpenAIConnectionHandler Reference |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_implementation"></a>7.1.2.6.5.3.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OpenAIGPT

Specific value: `"OpenAIGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model"></a>7.1.2.6.5.3.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"gpt-4-turbo"`                                                           |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i2_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation"></a>7.1.2.6.5.3.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_temperature"></a>7.1.2.6.5.3.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_force_json"></a>7.1.2.6.5.3.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens"></a>7.1.2.6.5.3.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i0"></a>7.1.2.6.5.3.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i1"></a>7.1.2.6.5.3.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler"></a>7.1.2.6.5.3.6. Property `connection_handler`

**Title:** OpenAIConnectionHandler Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"OpenAIConnectionHandler"`                                               |

| Property                                                                               | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_implementation"></a>7.1.2.6.5.3.6.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3"></a>7.1.2.6.5.4. Property `ToolCallLLMWrapper.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./ToolCallLLMWrapper.json                                            |

| Property                                                                      | Pattern | Type        | Deprecated | Definition                                  | Title/Description                                                    |
| ----------------------------------------------------------------------------- | ------- | ----------- | ---------- | ------------------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_implementation )           | No      | const       | No         | -                                           | ToolCallLLMWrapper                                                   |
| - [tool_message_prompt](#apu_anyOf_i0_llm_unit_anyOf_i3_tool_message_prompt ) | No      | string      | No         | -                                           | Tool Message Prompt                                                  |
| - [llm_unit](#apu_anyOf_i0_llm_unit_anyOf_i3_llm_unit )                       | No      | object      | No         | Same as [llm_unit](#apu_anyOf_i0_llm_unit ) | Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i3_model )                             | No      | Combination | No         | -                                           | -                                                                    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_implementation"></a>7.1.2.6.5.4.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ToolCallLLMWrapper

Specific value: `"ToolCallLLMWrapper"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_tool_message_prompt"></a>7.1.2.6.5.4.2. Property `tool_message_prompt`

**Title:** Tool Message Prompt

|              |                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Required** | No                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Default**  | `"You must follow these instructions:\nYou can select zero or more of the above tools based on the user query\nIf there are multiple tools required, make sure a list of tools are returned in a JSON array.\nIf there is no tool that match the user request or you have already answered the question, you will respond with empty json array for the tools.\nYou can also add any additional notes or explanations in the notes field."` |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_llm_unit"></a>7.1.2.6.5.4.3. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Same definition as**    | [llm_unit](#apu_anyOf_i0_llm_unit)                                        |

**Description:** Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model"></a>7.1.2.6.5.4.4. Property `model`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                       |
| -------------------------------------------------------------------- |
| [LLMModel Reference](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i1)             |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0"></a>7.1.2.6.5.4.4.1. Property `LLMModel Reference`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.llm_unit.LLMModel"`                                  |

| Property                                                                           | Pattern | Type   | Deprecated | Definition | Title/Description |
| ---------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_implementation"></a>7.1.2.6.5.4.4.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i1"></a>7.1.2.6.5.4.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i5_logic_units"></a>7.1.2.6.6. Property `logic_units`

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

| Each item of this array must be                        | Description |
| ------------------------------------------------------ | ----------- |
| [LogicUnit Reference](#apu_anyOf_i5_logic_units_items) | -           |

###### <a name="autogenerated_heading_22"></a>7.1.2.6.6.1. LogicUnit Reference

**Title:** LogicUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.logic_unit.LogicUnit"`                               |

| Property                                                            | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i5_logic_units_items_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i5_logic_units_items_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i5_logic_units_items_implementation"></a>7.1.2.6.6.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i5_audio_unit"></a>7.1.2.6.7. Property `audio_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                           |
| -------------------------------------------------------- |
| [AudioUnit Reference](#apu_anyOf_i5_audio_unit_anyOf_i0) |
| [item 1](#apu_anyOf_i5_audio_unit_anyOf_i1)              |

###### <a name="apu_anyOf_i5_audio_unit_anyOf_i0"></a>7.1.2.6.7.1. Property `AudioUnit Reference`

**Title:** AudioUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.audio_unit.AudioUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i5_audio_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i5_audio_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i5_audio_unit_anyOf_i0_implementation"></a>7.1.2.6.7.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i5_audio_unit_anyOf_i1"></a>7.1.2.6.7.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i5_image_unit"></a>7.1.2.6.8. Property `image_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                           |
| -------------------------------------------------------- |
| [ImageUnit Reference](#apu_anyOf_i5_image_unit_anyOf_i0) |
| [item 1](#apu_anyOf_i5_image_unit_anyOf_i1)              |

###### <a name="apu_anyOf_i5_image_unit_anyOf_i0"></a>7.1.2.6.8.1. Property `ImageUnit Reference`

**Title:** ImageUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.image_unit.ImageUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i5_image_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i5_image_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i5_image_unit_anyOf_i0_implementation"></a>7.1.2.6.8.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i5_image_unit_anyOf_i1"></a>7.1.2.6.8.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i5_record_conversation"></a>7.1.2.6.9. Property `record_conversation`

**Title:** Record Conversation

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i5_allow_tool_errors"></a>7.1.2.6.10. Property `allow_tool_errors`

**Title:** Allow Tool Errors

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i5_document_processor"></a>7.1.2.6.11. Property `document_processor`

**Title:** DocumentProcessor Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"DocumentProcessor"`                                                     |

| Property                                                             | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i5_document_processor_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i5_document_processor_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i5_document_processor_implementation"></a>7.1.2.6.11.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i6"></a>7.1.2.7. Property `GPT4o.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./GPT4o.json                                                         |

| Property                                                          | Pattern | Type            | Deprecated | Definition                       | Title/Description                                                    |
| ----------------------------------------------------------------- | ------- | --------------- | ---------- | -------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i6_implementation )                 | No      | const           | No         | -                                | GPT4o                                                                |
| - [max_num_function_calls](#apu_anyOf_i6_max_num_function_calls ) | No      | integer         | No         | -                                | Max Num Function Calls                                               |
| - [io_unit](#apu_anyOf_i6_io_unit )                               | No      | object          | No         | -                                | IOUnit Reference                                                     |
| - [memory_unit](#apu_anyOf_i6_memory_unit )                       | No      | object          | No         | -                                | MemoryUnit Reference                                                 |
| - [llm_unit](#apu_anyOf_i6_llm_unit )                             | No      | object          | No         | In [LLMUnit](/docs/components/llmunit/overview) | Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components |
| - [logic_units](#apu_anyOf_i6_logic_units )                       | No      | array of object | No         | -                                | Logic Units                                                          |
| - [audio_unit](#apu_anyOf_i6_audio_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [image_unit](#apu_anyOf_i6_image_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [record_conversation](#apu_anyOf_i6_record_conversation )       | No      | boolean         | No         | -                                | Record Conversation                                                  |
| - [allow_tool_errors](#apu_anyOf_i6_allow_tool_errors )           | No      | boolean         | No         | -                                | Allow Tool Errors                                                    |
| - [document_processor](#apu_anyOf_i6_document_processor )         | No      | object          | No         | -                                | DocumentProcessor Reference                                          |

###### <a name="apu_anyOf_i6_implementation"></a>7.1.2.7.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** GPT4o

Specific value: `"GPT4o"`

###### <a name="apu_anyOf_i6_max_num_function_calls"></a>7.1.2.7.2. Property `max_num_function_calls`

**Title:** Max Num Function Calls

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `10`      |

**Description:** The maximum number of function calls to make in a single request.

###### <a name="apu_anyOf_i6_io_unit"></a>7.1.2.7.3. Property `io_unit`

**Title:** IOUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"IOUnit"`                                                                |

| Property                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i6_io_unit_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i6_io_unit_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i6_io_unit_implementation"></a>7.1.2.7.3.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i6_memory_unit"></a>7.1.2.7.4. Property `memory_unit`

**Title:** MemoryUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"MemoryUnit"`                                                            |

| Property                                                      | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i6_memory_unit_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i6_memory_unit_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i6_memory_unit_implementation"></a>7.1.2.7.4.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i6_llm_unit"></a>7.1.2.7.5. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Defined in**            | [LLMUnit](/docs/components/llmunit/overview)                                             |

**Description:** Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components

| Any of(Option)                                             |
| ---------------------------------------------------------- |
| [AnthropicLLMUnit.json](#apu_anyOf_i0_llm_unit_anyOf_i0)   |
| [MistralGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i1)         |
| [OpenAIGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i2)          |
| [ToolCallLLMWrapper.json](#apu_anyOf_i0_llm_unit_anyOf_i3) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0"></a>7.1.2.7.5.1. Property `AnthropicLLMUnit.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./AnthropicLLMUnit.json                                              |

| Property                                                            | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i0_implementation ) | No      | const       | No         | -          | AnthropicLLMUnit   |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i0_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i0_temperature )       | No      | number      | No         | -          | Temperature        |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_args](#apu_anyOf_i0_llm_unit_anyOf_i0_client_args )       | No      | object      | No         | -          | Client Args        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_implementation"></a>7.1.2.7.5.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AnthropicLLMUnit

Specific value: `"AnthropicLLMUnit"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model"></a>7.1.2.7.5.1.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"claude-3-opus-20240229"`                                                |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i0_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i0_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model_implementation"></a>7.1.2.7.5.1.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_temperature"></a>7.1.2.7.5.1.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens"></a>7.1.2.7.5.1.4. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i0"></a>7.1.2.7.5.1.4.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i1"></a>7.1.2.7.5.1.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_client_args"></a>7.1.2.7.5.1.5. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1"></a>7.1.2.7.5.2. Property `MistralGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./MistralGPT.json                                                    |

| Property                                                            | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i1_implementation ) | No      | const       | No         | -          | MistralGPT         |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i1_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i1_temperature )       | No      | number      | No         | -          | Temperature        |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i1_force_json )         | No      | boolean     | No         | -          | Force Json         |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_args](#apu_anyOf_i0_llm_unit_anyOf_i1_client_args )       | No      | object      | No         | -          | Client Args        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_implementation"></a>7.1.2.7.5.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** MistralGPT

Specific value: `"MistralGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model"></a>7.1.2.7.5.2.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"mistral-large-latest"`                                                  |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i1_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i1_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model_implementation"></a>7.1.2.7.5.2.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_temperature"></a>7.1.2.7.5.2.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_force_json"></a>7.1.2.7.5.2.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens"></a>7.1.2.7.5.2.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i0"></a>7.1.2.7.5.2.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i1"></a>7.1.2.7.5.2.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_client_args"></a>7.1.2.7.5.2.6. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2"></a>7.1.2.7.5.3. Property `OpenAIGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./OpenAIGPT.json                                                     |

| Property                                                                    | Pattern | Type        | Deprecated | Definition | Title/Description                 |
| --------------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | --------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_implementation )         | No      | const       | No         | -          | OpenAIGPT                         |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i2_model )                           | No      | object      | No         | -          | LLMModel Reference                |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i2_temperature )               | No      | number      | No         | -          | Temperature                       |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i2_force_json )                 | No      | boolean     | No         | -          | Force Json                        |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens )                 | No      | Combination | No         | -          | Max Tokens                        |
| - [connection_handler](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler ) | No      | object      | No         | -          | OpenAIConnectionHandler Reference |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_implementation"></a>7.1.2.7.5.3.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OpenAIGPT

Specific value: `"OpenAIGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model"></a>7.1.2.7.5.3.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"gpt-4-turbo"`                                                           |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i2_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation"></a>7.1.2.7.5.3.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_temperature"></a>7.1.2.7.5.3.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_force_json"></a>7.1.2.7.5.3.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens"></a>7.1.2.7.5.3.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i0"></a>7.1.2.7.5.3.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i1"></a>7.1.2.7.5.3.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler"></a>7.1.2.7.5.3.6. Property `connection_handler`

**Title:** OpenAIConnectionHandler Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"OpenAIConnectionHandler"`                                               |

| Property                                                                               | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_implementation"></a>7.1.2.7.5.3.6.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3"></a>7.1.2.7.5.4. Property `ToolCallLLMWrapper.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./ToolCallLLMWrapper.json                                            |

| Property                                                                      | Pattern | Type        | Deprecated | Definition                                  | Title/Description                                                    |
| ----------------------------------------------------------------------------- | ------- | ----------- | ---------- | ------------------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_implementation )           | No      | const       | No         | -                                           | ToolCallLLMWrapper                                                   |
| - [tool_message_prompt](#apu_anyOf_i0_llm_unit_anyOf_i3_tool_message_prompt ) | No      | string      | No         | -                                           | Tool Message Prompt                                                  |
| - [llm_unit](#apu_anyOf_i0_llm_unit_anyOf_i3_llm_unit )                       | No      | object      | No         | Same as [llm_unit](#apu_anyOf_i0_llm_unit ) | Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i3_model )                             | No      | Combination | No         | -                                           | -                                                                    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_implementation"></a>7.1.2.7.5.4.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ToolCallLLMWrapper

Specific value: `"ToolCallLLMWrapper"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_tool_message_prompt"></a>7.1.2.7.5.4.2. Property `tool_message_prompt`

**Title:** Tool Message Prompt

|              |                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Required** | No                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Default**  | `"You must follow these instructions:\nYou can select zero or more of the above tools based on the user query\nIf there are multiple tools required, make sure a list of tools are returned in a JSON array.\nIf there is no tool that match the user request or you have already answered the question, you will respond with empty json array for the tools.\nYou can also add any additional notes or explanations in the notes field."` |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_llm_unit"></a>7.1.2.7.5.4.3. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Same definition as**    | [llm_unit](#apu_anyOf_i0_llm_unit)                                        |

**Description:** Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model"></a>7.1.2.7.5.4.4. Property `model`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                       |
| -------------------------------------------------------------------- |
| [LLMModel Reference](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i1)             |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0"></a>7.1.2.7.5.4.4.1. Property `LLMModel Reference`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.llm_unit.LLMModel"`                                  |

| Property                                                                           | Pattern | Type   | Deprecated | Definition | Title/Description |
| ---------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_implementation"></a>7.1.2.7.5.4.4.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i1"></a>7.1.2.7.5.4.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i6_logic_units"></a>7.1.2.7.6. Property `logic_units`

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

| Each item of this array must be                        | Description |
| ------------------------------------------------------ | ----------- |
| [LogicUnit Reference](#apu_anyOf_i6_logic_units_items) | -           |

###### <a name="autogenerated_heading_23"></a>7.1.2.7.6.1. LogicUnit Reference

**Title:** LogicUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.logic_unit.LogicUnit"`                               |

| Property                                                            | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i6_logic_units_items_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i6_logic_units_items_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i6_logic_units_items_implementation"></a>7.1.2.7.6.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i6_audio_unit"></a>7.1.2.7.7. Property `audio_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                           |
| -------------------------------------------------------- |
| [AudioUnit Reference](#apu_anyOf_i6_audio_unit_anyOf_i0) |
| [item 1](#apu_anyOf_i6_audio_unit_anyOf_i1)              |

###### <a name="apu_anyOf_i6_audio_unit_anyOf_i0"></a>7.1.2.7.7.1. Property `AudioUnit Reference`

**Title:** AudioUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.audio_unit.AudioUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i6_audio_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i6_audio_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i6_audio_unit_anyOf_i0_implementation"></a>7.1.2.7.7.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i6_audio_unit_anyOf_i1"></a>7.1.2.7.7.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i6_image_unit"></a>7.1.2.7.8. Property `image_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                           |
| -------------------------------------------------------- |
| [ImageUnit Reference](#apu_anyOf_i6_image_unit_anyOf_i0) |
| [item 1](#apu_anyOf_i6_image_unit_anyOf_i1)              |

###### <a name="apu_anyOf_i6_image_unit_anyOf_i0"></a>7.1.2.7.8.1. Property `ImageUnit Reference`

**Title:** ImageUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.image_unit.ImageUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i6_image_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i6_image_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i6_image_unit_anyOf_i0_implementation"></a>7.1.2.7.8.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i6_image_unit_anyOf_i1"></a>7.1.2.7.8.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i6_record_conversation"></a>7.1.2.7.9. Property `record_conversation`

**Title:** Record Conversation

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i6_allow_tool_errors"></a>7.1.2.7.10. Property `allow_tool_errors`

**Title:** Allow Tool Errors

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i6_document_processor"></a>7.1.2.7.11. Property `document_processor`

**Title:** DocumentProcessor Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"DocumentProcessor"`                                                     |

| Property                                                             | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i6_document_processor_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i6_document_processor_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i6_document_processor_implementation"></a>7.1.2.7.11.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i7"></a>7.1.2.8. Property `MistralLarge.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./MistralLarge.json                                                  |

| Property                                                          | Pattern | Type            | Deprecated | Definition                       | Title/Description                                                    |
| ----------------------------------------------------------------- | ------- | --------------- | ---------- | -------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i7_implementation )                 | No      | const           | No         | -                                | MistralLarge                                                         |
| - [max_num_function_calls](#apu_anyOf_i7_max_num_function_calls ) | No      | integer         | No         | -                                | Max Num Function Calls                                               |
| - [io_unit](#apu_anyOf_i7_io_unit )                               | No      | object          | No         | -                                | IOUnit Reference                                                     |
| - [memory_unit](#apu_anyOf_i7_memory_unit )                       | No      | object          | No         | -                                | MemoryUnit Reference                                                 |
| - [llm_unit](#apu_anyOf_i7_llm_unit )                             | No      | object          | No         | In [LLMUnit](/docs/components/llmunit/overview) | Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components |
| - [logic_units](#apu_anyOf_i7_logic_units )                       | No      | array of object | No         | -                                | Logic Units                                                          |
| - [audio_unit](#apu_anyOf_i7_audio_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [image_unit](#apu_anyOf_i7_image_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [record_conversation](#apu_anyOf_i7_record_conversation )       | No      | boolean         | No         | -                                | Record Conversation                                                  |
| - [allow_tool_errors](#apu_anyOf_i7_allow_tool_errors )           | No      | boolean         | No         | -                                | Allow Tool Errors                                                    |
| - [document_processor](#apu_anyOf_i7_document_processor )         | No      | object          | No         | -                                | DocumentProcessor Reference                                          |

###### <a name="apu_anyOf_i7_implementation"></a>7.1.2.8.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** MistralLarge

Specific value: `"MistralLarge"`

###### <a name="apu_anyOf_i7_max_num_function_calls"></a>7.1.2.8.2. Property `max_num_function_calls`

**Title:** Max Num Function Calls

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `10`      |

**Description:** The maximum number of function calls to make in a single request.

###### <a name="apu_anyOf_i7_io_unit"></a>7.1.2.8.3. Property `io_unit`

**Title:** IOUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"IOUnit"`                                                                |

| Property                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i7_io_unit_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i7_io_unit_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i7_io_unit_implementation"></a>7.1.2.8.3.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i7_memory_unit"></a>7.1.2.8.4. Property `memory_unit`

**Title:** MemoryUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"MemoryUnit"`                                                            |

| Property                                                      | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i7_memory_unit_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i7_memory_unit_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i7_memory_unit_implementation"></a>7.1.2.8.4.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i7_llm_unit"></a>7.1.2.8.5. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Defined in**            | [LLMUnit](/docs/components/llmunit/overview)                                             |

**Description:** Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components

| Any of(Option)                                             |
| ---------------------------------------------------------- |
| [AnthropicLLMUnit.json](#apu_anyOf_i0_llm_unit_anyOf_i0)   |
| [MistralGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i1)         |
| [OpenAIGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i2)          |
| [ToolCallLLMWrapper.json](#apu_anyOf_i0_llm_unit_anyOf_i3) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0"></a>7.1.2.8.5.1. Property `AnthropicLLMUnit.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./AnthropicLLMUnit.json                                              |

| Property                                                            | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i0_implementation ) | No      | const       | No         | -          | AnthropicLLMUnit   |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i0_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i0_temperature )       | No      | number      | No         | -          | Temperature        |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_args](#apu_anyOf_i0_llm_unit_anyOf_i0_client_args )       | No      | object      | No         | -          | Client Args        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_implementation"></a>7.1.2.8.5.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AnthropicLLMUnit

Specific value: `"AnthropicLLMUnit"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model"></a>7.1.2.8.5.1.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"claude-3-opus-20240229"`                                                |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i0_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i0_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model_implementation"></a>7.1.2.8.5.1.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_temperature"></a>7.1.2.8.5.1.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens"></a>7.1.2.8.5.1.4. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i0"></a>7.1.2.8.5.1.4.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i1"></a>7.1.2.8.5.1.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_client_args"></a>7.1.2.8.5.1.5. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1"></a>7.1.2.8.5.2. Property `MistralGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./MistralGPT.json                                                    |

| Property                                                            | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i1_implementation ) | No      | const       | No         | -          | MistralGPT         |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i1_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i1_temperature )       | No      | number      | No         | -          | Temperature        |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i1_force_json )         | No      | boolean     | No         | -          | Force Json         |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_args](#apu_anyOf_i0_llm_unit_anyOf_i1_client_args )       | No      | object      | No         | -          | Client Args        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_implementation"></a>7.1.2.8.5.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** MistralGPT

Specific value: `"MistralGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model"></a>7.1.2.8.5.2.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"mistral-large-latest"`                                                  |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i1_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i1_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model_implementation"></a>7.1.2.8.5.2.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_temperature"></a>7.1.2.8.5.2.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_force_json"></a>7.1.2.8.5.2.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens"></a>7.1.2.8.5.2.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i0"></a>7.1.2.8.5.2.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i1"></a>7.1.2.8.5.2.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_client_args"></a>7.1.2.8.5.2.6. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2"></a>7.1.2.8.5.3. Property `OpenAIGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./OpenAIGPT.json                                                     |

| Property                                                                    | Pattern | Type        | Deprecated | Definition | Title/Description                 |
| --------------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | --------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_implementation )         | No      | const       | No         | -          | OpenAIGPT                         |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i2_model )                           | No      | object      | No         | -          | LLMModel Reference                |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i2_temperature )               | No      | number      | No         | -          | Temperature                       |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i2_force_json )                 | No      | boolean     | No         | -          | Force Json                        |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens )                 | No      | Combination | No         | -          | Max Tokens                        |
| - [connection_handler](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler ) | No      | object      | No         | -          | OpenAIConnectionHandler Reference |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_implementation"></a>7.1.2.8.5.3.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OpenAIGPT

Specific value: `"OpenAIGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model"></a>7.1.2.8.5.3.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"gpt-4-turbo"`                                                           |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i2_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation"></a>7.1.2.8.5.3.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_temperature"></a>7.1.2.8.5.3.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_force_json"></a>7.1.2.8.5.3.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens"></a>7.1.2.8.5.3.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i0"></a>7.1.2.8.5.3.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i1"></a>7.1.2.8.5.3.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler"></a>7.1.2.8.5.3.6. Property `connection_handler`

**Title:** OpenAIConnectionHandler Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"OpenAIConnectionHandler"`                                               |

| Property                                                                               | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_implementation"></a>7.1.2.8.5.3.6.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3"></a>7.1.2.8.5.4. Property `ToolCallLLMWrapper.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./ToolCallLLMWrapper.json                                            |

| Property                                                                      | Pattern | Type        | Deprecated | Definition                                  | Title/Description                                                    |
| ----------------------------------------------------------------------------- | ------- | ----------- | ---------- | ------------------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_implementation )           | No      | const       | No         | -                                           | ToolCallLLMWrapper                                                   |
| - [tool_message_prompt](#apu_anyOf_i0_llm_unit_anyOf_i3_tool_message_prompt ) | No      | string      | No         | -                                           | Tool Message Prompt                                                  |
| - [llm_unit](#apu_anyOf_i0_llm_unit_anyOf_i3_llm_unit )                       | No      | object      | No         | Same as [llm_unit](#apu_anyOf_i0_llm_unit ) | Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i3_model )                             | No      | Combination | No         | -                                           | -                                                                    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_implementation"></a>7.1.2.8.5.4.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ToolCallLLMWrapper

Specific value: `"ToolCallLLMWrapper"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_tool_message_prompt"></a>7.1.2.8.5.4.2. Property `tool_message_prompt`

**Title:** Tool Message Prompt

|              |                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Required** | No                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Default**  | `"You must follow these instructions:\nYou can select zero or more of the above tools based on the user query\nIf there are multiple tools required, make sure a list of tools are returned in a JSON array.\nIf there is no tool that match the user request or you have already answered the question, you will respond with empty json array for the tools.\nYou can also add any additional notes or explanations in the notes field."` |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_llm_unit"></a>7.1.2.8.5.4.3. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Same definition as**    | [llm_unit](#apu_anyOf_i0_llm_unit)                                        |

**Description:** Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model"></a>7.1.2.8.5.4.4. Property `model`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                       |
| -------------------------------------------------------------------- |
| [LLMModel Reference](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i1)             |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0"></a>7.1.2.8.5.4.4.1. Property `LLMModel Reference`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.llm_unit.LLMModel"`                                  |

| Property                                                                           | Pattern | Type   | Deprecated | Definition | Title/Description |
| ---------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_implementation"></a>7.1.2.8.5.4.4.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i1"></a>7.1.2.8.5.4.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i7_logic_units"></a>7.1.2.8.6. Property `logic_units`

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

| Each item of this array must be                        | Description |
| ------------------------------------------------------ | ----------- |
| [LogicUnit Reference](#apu_anyOf_i7_logic_units_items) | -           |

###### <a name="autogenerated_heading_24"></a>7.1.2.8.6.1. LogicUnit Reference

**Title:** LogicUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.logic_unit.LogicUnit"`                               |

| Property                                                            | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i7_logic_units_items_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i7_logic_units_items_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i7_logic_units_items_implementation"></a>7.1.2.8.6.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i7_audio_unit"></a>7.1.2.8.7. Property `audio_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                           |
| -------------------------------------------------------- |
| [AudioUnit Reference](#apu_anyOf_i7_audio_unit_anyOf_i0) |
| [item 1](#apu_anyOf_i7_audio_unit_anyOf_i1)              |

###### <a name="apu_anyOf_i7_audio_unit_anyOf_i0"></a>7.1.2.8.7.1. Property `AudioUnit Reference`

**Title:** AudioUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.audio_unit.AudioUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i7_audio_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i7_audio_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i7_audio_unit_anyOf_i0_implementation"></a>7.1.2.8.7.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i7_audio_unit_anyOf_i1"></a>7.1.2.8.7.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i7_image_unit"></a>7.1.2.8.8. Property `image_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                           |
| -------------------------------------------------------- |
| [ImageUnit Reference](#apu_anyOf_i7_image_unit_anyOf_i0) |
| [item 1](#apu_anyOf_i7_image_unit_anyOf_i1)              |

###### <a name="apu_anyOf_i7_image_unit_anyOf_i0"></a>7.1.2.8.8.1. Property `ImageUnit Reference`

**Title:** ImageUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.image_unit.ImageUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i7_image_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i7_image_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i7_image_unit_anyOf_i0_implementation"></a>7.1.2.8.8.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i7_image_unit_anyOf_i1"></a>7.1.2.8.8.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i7_record_conversation"></a>7.1.2.8.9. Property `record_conversation`

**Title:** Record Conversation

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i7_allow_tool_errors"></a>7.1.2.8.10. Property `allow_tool_errors`

**Title:** Allow Tool Errors

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i7_document_processor"></a>7.1.2.8.11. Property `document_processor`

**Title:** DocumentProcessor Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"DocumentProcessor"`                                                     |

| Property                                                             | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i7_document_processor_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i7_document_processor_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i7_document_processor_implementation"></a>7.1.2.8.11.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i8"></a>7.1.2.9. Property `MistralMedium.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./MistralMedium.json                                                 |

| Property                                                          | Pattern | Type            | Deprecated | Definition                       | Title/Description                                                    |
| ----------------------------------------------------------------- | ------- | --------------- | ---------- | -------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i8_implementation )                 | No      | const           | No         | -                                | MistralMedium                                                        |
| - [max_num_function_calls](#apu_anyOf_i8_max_num_function_calls ) | No      | integer         | No         | -                                | Max Num Function Calls                                               |
| - [io_unit](#apu_anyOf_i8_io_unit )                               | No      | object          | No         | -                                | IOUnit Reference                                                     |
| - [memory_unit](#apu_anyOf_i8_memory_unit )                       | No      | object          | No         | -                                | MemoryUnit Reference                                                 |
| - [llm_unit](#apu_anyOf_i8_llm_unit )                             | No      | object          | No         | In [LLMUnit](/docs/components/llmunit/overview) | Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components |
| - [logic_units](#apu_anyOf_i8_logic_units )                       | No      | array of object | No         | -                                | Logic Units                                                          |
| - [audio_unit](#apu_anyOf_i8_audio_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [image_unit](#apu_anyOf_i8_image_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [record_conversation](#apu_anyOf_i8_record_conversation )       | No      | boolean         | No         | -                                | Record Conversation                                                  |
| - [allow_tool_errors](#apu_anyOf_i8_allow_tool_errors )           | No      | boolean         | No         | -                                | Allow Tool Errors                                                    |
| - [document_processor](#apu_anyOf_i8_document_processor )         | No      | object          | No         | -                                | DocumentProcessor Reference                                          |

###### <a name="apu_anyOf_i8_implementation"></a>7.1.2.9.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** MistralMedium

Specific value: `"MistralMedium"`

###### <a name="apu_anyOf_i8_max_num_function_calls"></a>7.1.2.9.2. Property `max_num_function_calls`

**Title:** Max Num Function Calls

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `10`      |

**Description:** The maximum number of function calls to make in a single request.

###### <a name="apu_anyOf_i8_io_unit"></a>7.1.2.9.3. Property `io_unit`

**Title:** IOUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"IOUnit"`                                                                |

| Property                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i8_io_unit_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i8_io_unit_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i8_io_unit_implementation"></a>7.1.2.9.3.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i8_memory_unit"></a>7.1.2.9.4. Property `memory_unit`

**Title:** MemoryUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"MemoryUnit"`                                                            |

| Property                                                      | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i8_memory_unit_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i8_memory_unit_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i8_memory_unit_implementation"></a>7.1.2.9.4.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i8_llm_unit"></a>7.1.2.9.5. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Defined in**            | [LLMUnit](/docs/components/llmunit/overview)                                             |

**Description:** Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components

| Any of(Option)                                             |
| ---------------------------------------------------------- |
| [AnthropicLLMUnit.json](#apu_anyOf_i0_llm_unit_anyOf_i0)   |
| [MistralGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i1)         |
| [OpenAIGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i2)          |
| [ToolCallLLMWrapper.json](#apu_anyOf_i0_llm_unit_anyOf_i3) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0"></a>7.1.2.9.5.1. Property `AnthropicLLMUnit.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./AnthropicLLMUnit.json                                              |

| Property                                                            | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i0_implementation ) | No      | const       | No         | -          | AnthropicLLMUnit   |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i0_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i0_temperature )       | No      | number      | No         | -          | Temperature        |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_args](#apu_anyOf_i0_llm_unit_anyOf_i0_client_args )       | No      | object      | No         | -          | Client Args        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_implementation"></a>7.1.2.9.5.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AnthropicLLMUnit

Specific value: `"AnthropicLLMUnit"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model"></a>7.1.2.9.5.1.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"claude-3-opus-20240229"`                                                |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i0_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i0_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model_implementation"></a>7.1.2.9.5.1.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_temperature"></a>7.1.2.9.5.1.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens"></a>7.1.2.9.5.1.4. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i0"></a>7.1.2.9.5.1.4.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i1"></a>7.1.2.9.5.1.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_client_args"></a>7.1.2.9.5.1.5. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1"></a>7.1.2.9.5.2. Property `MistralGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./MistralGPT.json                                                    |

| Property                                                            | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i1_implementation ) | No      | const       | No         | -          | MistralGPT         |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i1_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i1_temperature )       | No      | number      | No         | -          | Temperature        |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i1_force_json )         | No      | boolean     | No         | -          | Force Json         |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_args](#apu_anyOf_i0_llm_unit_anyOf_i1_client_args )       | No      | object      | No         | -          | Client Args        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_implementation"></a>7.1.2.9.5.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** MistralGPT

Specific value: `"MistralGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model"></a>7.1.2.9.5.2.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"mistral-large-latest"`                                                  |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i1_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i1_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model_implementation"></a>7.1.2.9.5.2.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_temperature"></a>7.1.2.9.5.2.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_force_json"></a>7.1.2.9.5.2.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens"></a>7.1.2.9.5.2.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i0"></a>7.1.2.9.5.2.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i1"></a>7.1.2.9.5.2.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_client_args"></a>7.1.2.9.5.2.6. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2"></a>7.1.2.9.5.3. Property `OpenAIGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./OpenAIGPT.json                                                     |

| Property                                                                    | Pattern | Type        | Deprecated | Definition | Title/Description                 |
| --------------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | --------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_implementation )         | No      | const       | No         | -          | OpenAIGPT                         |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i2_model )                           | No      | object      | No         | -          | LLMModel Reference                |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i2_temperature )               | No      | number      | No         | -          | Temperature                       |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i2_force_json )                 | No      | boolean     | No         | -          | Force Json                        |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens )                 | No      | Combination | No         | -          | Max Tokens                        |
| - [connection_handler](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler ) | No      | object      | No         | -          | OpenAIConnectionHandler Reference |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_implementation"></a>7.1.2.9.5.3.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OpenAIGPT

Specific value: `"OpenAIGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model"></a>7.1.2.9.5.3.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"gpt-4-turbo"`                                                           |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i2_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation"></a>7.1.2.9.5.3.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_temperature"></a>7.1.2.9.5.3.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_force_json"></a>7.1.2.9.5.3.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens"></a>7.1.2.9.5.3.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i0"></a>7.1.2.9.5.3.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i1"></a>7.1.2.9.5.3.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler"></a>7.1.2.9.5.3.6. Property `connection_handler`

**Title:** OpenAIConnectionHandler Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"OpenAIConnectionHandler"`                                               |

| Property                                                                               | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_implementation"></a>7.1.2.9.5.3.6.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3"></a>7.1.2.9.5.4. Property `ToolCallLLMWrapper.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./ToolCallLLMWrapper.json                                            |

| Property                                                                      | Pattern | Type        | Deprecated | Definition                                  | Title/Description                                                    |
| ----------------------------------------------------------------------------- | ------- | ----------- | ---------- | ------------------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_implementation )           | No      | const       | No         | -                                           | ToolCallLLMWrapper                                                   |
| - [tool_message_prompt](#apu_anyOf_i0_llm_unit_anyOf_i3_tool_message_prompt ) | No      | string      | No         | -                                           | Tool Message Prompt                                                  |
| - [llm_unit](#apu_anyOf_i0_llm_unit_anyOf_i3_llm_unit )                       | No      | object      | No         | Same as [llm_unit](#apu_anyOf_i0_llm_unit ) | Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i3_model )                             | No      | Combination | No         | -                                           | -                                                                    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_implementation"></a>7.1.2.9.5.4.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ToolCallLLMWrapper

Specific value: `"ToolCallLLMWrapper"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_tool_message_prompt"></a>7.1.2.9.5.4.2. Property `tool_message_prompt`

**Title:** Tool Message Prompt

|              |                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Required** | No                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Default**  | `"You must follow these instructions:\nYou can select zero or more of the above tools based on the user query\nIf there are multiple tools required, make sure a list of tools are returned in a JSON array.\nIf there is no tool that match the user request or you have already answered the question, you will respond with empty json array for the tools.\nYou can also add any additional notes or explanations in the notes field."` |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_llm_unit"></a>7.1.2.9.5.4.3. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Same definition as**    | [llm_unit](#apu_anyOf_i0_llm_unit)                                        |

**Description:** Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model"></a>7.1.2.9.5.4.4. Property `model`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                       |
| -------------------------------------------------------------------- |
| [LLMModel Reference](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i1)             |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0"></a>7.1.2.9.5.4.4.1. Property `LLMModel Reference`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.llm_unit.LLMModel"`                                  |

| Property                                                                           | Pattern | Type   | Deprecated | Definition | Title/Description |
| ---------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_implementation"></a>7.1.2.9.5.4.4.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i1"></a>7.1.2.9.5.4.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i8_logic_units"></a>7.1.2.9.6. Property `logic_units`

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

| Each item of this array must be                        | Description |
| ------------------------------------------------------ | ----------- |
| [LogicUnit Reference](#apu_anyOf_i8_logic_units_items) | -           |

###### <a name="autogenerated_heading_25"></a>7.1.2.9.6.1. LogicUnit Reference

**Title:** LogicUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.logic_unit.LogicUnit"`                               |

| Property                                                            | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i8_logic_units_items_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i8_logic_units_items_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i8_logic_units_items_implementation"></a>7.1.2.9.6.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i8_audio_unit"></a>7.1.2.9.7. Property `audio_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                           |
| -------------------------------------------------------- |
| [AudioUnit Reference](#apu_anyOf_i8_audio_unit_anyOf_i0) |
| [item 1](#apu_anyOf_i8_audio_unit_anyOf_i1)              |

###### <a name="apu_anyOf_i8_audio_unit_anyOf_i0"></a>7.1.2.9.7.1. Property `AudioUnit Reference`

**Title:** AudioUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.audio_unit.AudioUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i8_audio_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i8_audio_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i8_audio_unit_anyOf_i0_implementation"></a>7.1.2.9.7.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i8_audio_unit_anyOf_i1"></a>7.1.2.9.7.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i8_image_unit"></a>7.1.2.9.8. Property `image_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                           |
| -------------------------------------------------------- |
| [ImageUnit Reference](#apu_anyOf_i8_image_unit_anyOf_i0) |
| [item 1](#apu_anyOf_i8_image_unit_anyOf_i1)              |

###### <a name="apu_anyOf_i8_image_unit_anyOf_i0"></a>7.1.2.9.8.1. Property `ImageUnit Reference`

**Title:** ImageUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.image_unit.ImageUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i8_image_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i8_image_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i8_image_unit_anyOf_i0_implementation"></a>7.1.2.9.8.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i8_image_unit_anyOf_i1"></a>7.1.2.9.8.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i8_record_conversation"></a>7.1.2.9.9. Property `record_conversation`

**Title:** Record Conversation

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i8_allow_tool_errors"></a>7.1.2.9.10. Property `allow_tool_errors`

**Title:** Allow Tool Errors

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i8_document_processor"></a>7.1.2.9.11. Property `document_processor`

**Title:** DocumentProcessor Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"DocumentProcessor"`                                                     |

| Property                                                             | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i8_document_processor_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i8_document_processor_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i8_document_processor_implementation"></a>7.1.2.9.11.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i9"></a>7.1.2.10. Property `MistralSmall.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./MistralSmall.json                                                  |

| Property                                                          | Pattern | Type            | Deprecated | Definition                       | Title/Description                                                    |
| ----------------------------------------------------------------- | ------- | --------------- | ---------- | -------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i9_implementation )                 | No      | const           | No         | -                                | MistralSmall                                                         |
| - [max_num_function_calls](#apu_anyOf_i9_max_num_function_calls ) | No      | integer         | No         | -                                | Max Num Function Calls                                               |
| - [io_unit](#apu_anyOf_i9_io_unit )                               | No      | object          | No         | -                                | IOUnit Reference                                                     |
| - [memory_unit](#apu_anyOf_i9_memory_unit )                       | No      | object          | No         | -                                | MemoryUnit Reference                                                 |
| - [llm_unit](#apu_anyOf_i9_llm_unit )                             | No      | object          | No         | In [LLMUnit](/docs/components/llmunit/overview) | Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components |
| - [logic_units](#apu_anyOf_i9_logic_units )                       | No      | array of object | No         | -                                | Logic Units                                                          |
| - [audio_unit](#apu_anyOf_i9_audio_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [image_unit](#apu_anyOf_i9_image_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [record_conversation](#apu_anyOf_i9_record_conversation )       | No      | boolean         | No         | -                                | Record Conversation                                                  |
| - [allow_tool_errors](#apu_anyOf_i9_allow_tool_errors )           | No      | boolean         | No         | -                                | Allow Tool Errors                                                    |
| - [document_processor](#apu_anyOf_i9_document_processor )         | No      | object          | No         | -                                | DocumentProcessor Reference                                          |

###### <a name="apu_anyOf_i9_implementation"></a>7.1.2.10.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** MistralSmall

Specific value: `"MistralSmall"`

###### <a name="apu_anyOf_i9_max_num_function_calls"></a>7.1.2.10.2. Property `max_num_function_calls`

**Title:** Max Num Function Calls

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `10`      |

**Description:** The maximum number of function calls to make in a single request.

###### <a name="apu_anyOf_i9_io_unit"></a>7.1.2.10.3. Property `io_unit`

**Title:** IOUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"IOUnit"`                                                                |

| Property                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i9_io_unit_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i9_io_unit_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i9_io_unit_implementation"></a>7.1.2.10.3.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i9_memory_unit"></a>7.1.2.10.4. Property `memory_unit`

**Title:** MemoryUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"MemoryUnit"`                                                            |

| Property                                                      | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i9_memory_unit_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i9_memory_unit_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i9_memory_unit_implementation"></a>7.1.2.10.4.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i9_llm_unit"></a>7.1.2.10.5. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Defined in**            | [LLMUnit](/docs/components/llmunit/overview)                                             |

**Description:** Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components

| Any of(Option)                                             |
| ---------------------------------------------------------- |
| [AnthropicLLMUnit.json](#apu_anyOf_i0_llm_unit_anyOf_i0)   |
| [MistralGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i1)         |
| [OpenAIGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i2)          |
| [ToolCallLLMWrapper.json](#apu_anyOf_i0_llm_unit_anyOf_i3) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0"></a>7.1.2.10.5.1. Property `AnthropicLLMUnit.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./AnthropicLLMUnit.json                                              |

| Property                                                            | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i0_implementation ) | No      | const       | No         | -          | AnthropicLLMUnit   |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i0_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i0_temperature )       | No      | number      | No         | -          | Temperature        |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_args](#apu_anyOf_i0_llm_unit_anyOf_i0_client_args )       | No      | object      | No         | -          | Client Args        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_implementation"></a>7.1.2.10.5.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AnthropicLLMUnit

Specific value: `"AnthropicLLMUnit"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model"></a>7.1.2.10.5.1.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"claude-3-opus-20240229"`                                                |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i0_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i0_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model_implementation"></a>7.1.2.10.5.1.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_temperature"></a>7.1.2.10.5.1.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens"></a>7.1.2.10.5.1.4. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i0"></a>7.1.2.10.5.1.4.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i1"></a>7.1.2.10.5.1.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_client_args"></a>7.1.2.10.5.1.5. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1"></a>7.1.2.10.5.2. Property `MistralGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./MistralGPT.json                                                    |

| Property                                                            | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i1_implementation ) | No      | const       | No         | -          | MistralGPT         |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i1_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i1_temperature )       | No      | number      | No         | -          | Temperature        |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i1_force_json )         | No      | boolean     | No         | -          | Force Json         |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_args](#apu_anyOf_i0_llm_unit_anyOf_i1_client_args )       | No      | object      | No         | -          | Client Args        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_implementation"></a>7.1.2.10.5.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** MistralGPT

Specific value: `"MistralGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model"></a>7.1.2.10.5.2.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"mistral-large-latest"`                                                  |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i1_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i1_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model_implementation"></a>7.1.2.10.5.2.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_temperature"></a>7.1.2.10.5.2.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_force_json"></a>7.1.2.10.5.2.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens"></a>7.1.2.10.5.2.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i0"></a>7.1.2.10.5.2.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i1"></a>7.1.2.10.5.2.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_client_args"></a>7.1.2.10.5.2.6. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2"></a>7.1.2.10.5.3. Property `OpenAIGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./OpenAIGPT.json                                                     |

| Property                                                                    | Pattern | Type        | Deprecated | Definition | Title/Description                 |
| --------------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | --------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_implementation )         | No      | const       | No         | -          | OpenAIGPT                         |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i2_model )                           | No      | object      | No         | -          | LLMModel Reference                |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i2_temperature )               | No      | number      | No         | -          | Temperature                       |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i2_force_json )                 | No      | boolean     | No         | -          | Force Json                        |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens )                 | No      | Combination | No         | -          | Max Tokens                        |
| - [connection_handler](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler ) | No      | object      | No         | -          | OpenAIConnectionHandler Reference |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_implementation"></a>7.1.2.10.5.3.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OpenAIGPT

Specific value: `"OpenAIGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model"></a>7.1.2.10.5.3.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"gpt-4-turbo"`                                                           |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i2_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation"></a>7.1.2.10.5.3.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_temperature"></a>7.1.2.10.5.3.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_force_json"></a>7.1.2.10.5.3.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens"></a>7.1.2.10.5.3.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i0"></a>7.1.2.10.5.3.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i1"></a>7.1.2.10.5.3.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler"></a>7.1.2.10.5.3.6. Property `connection_handler`

**Title:** OpenAIConnectionHandler Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"OpenAIConnectionHandler"`                                               |

| Property                                                                               | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_connection_handler_implementation"></a>7.1.2.10.5.3.6.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3"></a>7.1.2.10.5.4. Property `ToolCallLLMWrapper.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./ToolCallLLMWrapper.json                                            |

| Property                                                                      | Pattern | Type        | Deprecated | Definition                                  | Title/Description                                                    |
| ----------------------------------------------------------------------------- | ------- | ----------- | ---------- | ------------------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_implementation )           | No      | const       | No         | -                                           | ToolCallLLMWrapper                                                   |
| - [tool_message_prompt](#apu_anyOf_i0_llm_unit_anyOf_i3_tool_message_prompt ) | No      | string      | No         | -                                           | Tool Message Prompt                                                  |
| - [llm_unit](#apu_anyOf_i0_llm_unit_anyOf_i3_llm_unit )                       | No      | object      | No         | Same as [llm_unit](#apu_anyOf_i0_llm_unit ) | Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i3_model )                             | No      | Combination | No         | -                                           | -                                                                    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_implementation"></a>7.1.2.10.5.4.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ToolCallLLMWrapper

Specific value: `"ToolCallLLMWrapper"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_tool_message_prompt"></a>7.1.2.10.5.4.2. Property `tool_message_prompt`

**Title:** Tool Message Prompt

|              |                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Required** | No                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Default**  | `"You must follow these instructions:\nYou can select zero or more of the above tools based on the user query\nIf there are multiple tools required, make sure a list of tools are returned in a JSON array.\nIf there is no tool that match the user request or you have already answered the question, you will respond with empty json array for the tools.\nYou can also add any additional notes or explanations in the notes field."` |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_llm_unit"></a>7.1.2.10.5.4.3. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Same definition as**    | [llm_unit](#apu_anyOf_i0_llm_unit)                                        |

**Description:** Overview of <class 'eidolon_ai_sdk.cpu.llm_unit.LLMUnit'> components

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model"></a>7.1.2.10.5.4.4. Property `model`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                       |
| -------------------------------------------------------------------- |
| [LLMModel Reference](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i1)             |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0"></a>7.1.2.10.5.4.4.1. Property `LLMModel Reference`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.llm_unit.LLMModel"`                                  |

| Property                                                                           | Pattern | Type   | Deprecated | Definition | Title/Description |
| ---------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i0_implementation"></a>7.1.2.10.5.4.4.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_anyOf_i1"></a>7.1.2.10.5.4.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i9_logic_units"></a>7.1.2.10.6. Property `logic_units`

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

| Each item of this array must be                        | Description |
| ------------------------------------------------------ | ----------- |
| [LogicUnit Reference](#apu_anyOf_i9_logic_units_items) | -           |

###### <a name="autogenerated_heading_26"></a>7.1.2.10.6.1. LogicUnit Reference

**Title:** LogicUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.logic_unit.LogicUnit"`                               |

| Property                                                            | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i9_logic_units_items_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i9_logic_units_items_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i9_logic_units_items_implementation"></a>7.1.2.10.6.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i9_audio_unit"></a>7.1.2.10.7. Property `audio_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                           |
| -------------------------------------------------------- |
| [AudioUnit Reference](#apu_anyOf_i9_audio_unit_anyOf_i0) |
| [item 1](#apu_anyOf_i9_audio_unit_anyOf_i1)              |

###### <a name="apu_anyOf_i9_audio_unit_anyOf_i0"></a>7.1.2.10.7.1. Property `AudioUnit Reference`

**Title:** AudioUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.audio_unit.AudioUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i9_audio_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i9_audio_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i9_audio_unit_anyOf_i0_implementation"></a>7.1.2.10.7.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i9_audio_unit_anyOf_i1"></a>7.1.2.10.7.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i9_image_unit"></a>7.1.2.10.8. Property `image_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                           |
| -------------------------------------------------------- |
| [ImageUnit Reference](#apu_anyOf_i9_image_unit_anyOf_i0) |
| [item 1](#apu_anyOf_i9_image_unit_anyOf_i1)              |

###### <a name="apu_anyOf_i9_image_unit_anyOf_i0"></a>7.1.2.10.8.1. Property `ImageUnit Reference`

**Title:** ImageUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.cpu.image_unit.ImageUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i9_image_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i9_image_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i9_image_unit_anyOf_i0_implementation"></a>7.1.2.10.8.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i9_image_unit_anyOf_i1"></a>7.1.2.10.8.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i9_record_conversation"></a>7.1.2.10.9. Property `record_conversation`

**Title:** Record Conversation

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i9_allow_tool_errors"></a>7.1.2.10.10. Property `allow_tool_errors`

**Title:** Allow Tool Errors

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i9_document_processor"></a>7.1.2.10.11. Property `document_processor`

**Title:** DocumentProcessor Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"DocumentProcessor"`                                                     |

| Property                                                             | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i9_document_processor_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i9_document_processor_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i9_document_processor_implementation"></a>7.1.2.10.11.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apus_items_default"></a>7.1.3. Property `default`

**Title:** Default

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `false`   |

## <a name="title_generation_mode"></a>8. Property `title_generation_mode`

**Title:** Title Generation Mode

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | No                 |
| **Default**  | `"on_request"`     |

Must be one of:
* "none"
* "on_request"

## <a name="doc_processor"></a>9. Property `doc_processor`

**Title:** DocumentProcessor Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"DocumentProcessor"`                                                     |

| Property                                           | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#doc_processor_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#doc_processor_additionalProperties )         | No      | object | No         | -          | -                 |

### <a name="doc_processor_implementation"></a>9.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

----------------------------------------------------------------------------------------------------------------------------
