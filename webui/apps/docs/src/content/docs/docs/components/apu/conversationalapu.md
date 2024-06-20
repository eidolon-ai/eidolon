---
title: ConversationalAPU
description: Description of ConversationalAPU component
---

| Property                                             | Pattern | Type        | Deprecated | Definition                                 | Title/Description                                                                                                                                                                   |
| ---------------------------------------------------- | ------- | ----------- | ---------- | ------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| - [implementation](#implementation )                 | No      | const       | No         | -                                          | ConversationalAPU                                                                                                                                                                   |
| - [max_num_function_calls](#max_num_function_calls ) | No      | integer     | No         | -                                          | Max Num Function Calls                                                                                                                                                              |
| - [io_unit](#io_unit )                               | No      | object      | No         | In [IOUnit](/docs/components/iounit/overview)            | <br />This is the IO unit for the APU. It is responsible for converting the prompts from the User to the LLM<br /><br />This can be overridden to provide custom IO handling.<br /> |
| - [memory_unit](#memory_unit )                       | No      | object      | No         | In [MemoryUnit](/docs/components/memoryunit/overview)        | Overview of MemoryUnit components                                                                                                                                                   |
| - [llm_unit](#llm_unit )                             | No      | object      | No         | In [LLMUnit](/docs/components/llmunit/overview)           | Overview of LLMUnit components                                                                                                                                                      |
| - [logic_units](#logic_units )                       | No      | array       | No         | -                                          | Logic Units                                                                                                                                                                         |
| - [audio_unit](#audio_unit )                         | No      | Combination | No         | -                                          | -                                                                                                                                                                                   |
| - [image_unit](#image_unit )                         | No      | Combination | No         | -                                          | -                                                                                                                                                                                   |
| - [record_conversation](#record_conversation )       | No      | boolean     | No         | -                                          | Record Conversation                                                                                                                                                                 |
| - [allow_tool_errors](#allow_tool_errors )           | No      | boolean     | No         | -                                          | Allow Tool Errors                                                                                                                                                                   |
| - [document_processor](#document_processor )         | No      | object      | No         | In [DocumentProcessor](/docs/components/documentprocessor/overview) | Overview of DocumentProcessor components                                                                                                                                            |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ConversationalAPU

Specific value: `"ConversationalAPU"`

## <a name="max_num_function_calls"></a>2. Property `max_num_function_calls`

**Title:** Max Num Function Calls

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `10`      |

**Description:** The maximum number of function calls to make in a single request.

## <a name="io_unit"></a>3. Property `io_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{"implementation": "IOUnit"}`                                            |
| **Defined in**            | [IOUnit](/docs/components/iounit/overview)                                              |

**Description:** 
This is the IO unit for the APU. It is responsible for converting the prompts from the User to the LLM

This can be overridden to provide custom IO handling.

| Any of(Option)                   |
| -------------------------------- |
| [IOUnit.json](#io_unit_anyOf_i0) |

### <a name="io_unit_anyOf_i0"></a>3.1. Property `IOUnit.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./IOUnit.json                                                        |

**Description:** 
This is the IO unit for the APU. It is responsible for converting the prompts from the User to the LLM

This can be overridden to provide custom IO handling.

| Property                                              | Pattern | Type  | Deprecated | Definition | Title/Description |
| ----------------------------------------------------- | ------- | ----- | ---------- | ---------- | ----------------- |
| - [implementation](#io_unit_anyOf_i0_implementation ) | No      | const | No         | -          | IOUnit            |

#### <a name="io_unit_anyOf_i0_implementation"></a>3.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** IOUnit

Specific value: `"IOUnit"`

## <a name="memory_unit"></a>4. Property `memory_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{"implementation": "RawMemoryUnit"}`                                     |
| **Defined in**            | [MemoryUnit](/docs/components/memoryunit/overview)                                          |

**Description:** Overview of MemoryUnit components

| Any of(Option)                              |
| ------------------------------------------- |
| [RawMemoryUnit.json](#memory_unit_anyOf_i0) |

### <a name="memory_unit_anyOf_i0"></a>4.1. Property `RawMemoryUnit.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./RawMemoryUnit.json                                                 |

| Property                                                  | Pattern | Type  | Deprecated | Definition | Title/Description |
| --------------------------------------------------------- | ------- | ----- | ---------- | ---------- | ----------------- |
| - [implementation](#memory_unit_anyOf_i0_implementation ) | No      | const | No         | -          | RawMemoryUnit     |

#### <a name="memory_unit_anyOf_i0_implementation"></a>4.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** RawMemoryUnit

Specific value: `"RawMemoryUnit"`

## <a name="llm_unit"></a>5. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{"implementation": "OpenAIGPT"}`                                         |
| **Defined in**            | [LLMUnit](/docs/components/llmunit/overview)                                             |

**Description:** Overview of LLMUnit components

| Any of(Option)                                |
| --------------------------------------------- |
| [AnthropicLLMUnit.json](#llm_unit_anyOf_i0)   |
| [MistralGPT.json](#llm_unit_anyOf_i1)         |
| [OllamaLLMUnit.json](#llm_unit_anyOf_i2)      |
| [OpenAIGPT.json](#llm_unit_anyOf_i3)          |
| [ToolCallLLMWrapper.json](#llm_unit_anyOf_i4) |

### <a name="llm_unit_anyOf_i0"></a>5.1. Property `AnthropicLLMUnit.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./AnthropicLLMUnit.json                                              |

| Property                                               | Pattern | Type        | Deprecated | Definition                        | Title/Description               |
| ------------------------------------------------------ | ------- | ----------- | ---------- | --------------------------------- | ------------------------------- |
| - [implementation](#llm_unit_anyOf_i0_implementation ) | No      | const       | No         | -                                 | AnthropicLLMUnit                |
| - [model](#llm_unit_anyOf_i0_model )                   | No      | object      | No         | In [LLMModel](/docs/components/llmmodel/overview) | Overview of LLMModel components |
| - [temperature](#llm_unit_anyOf_i0_temperature )       | No      | number      | No         | -                                 | Temperature                     |
| - [max_tokens](#llm_unit_anyOf_i0_max_tokens )         | No      | Combination | No         | -                                 | Max Tokens                      |
| - [client_args](#llm_unit_anyOf_i0_client_args )       | No      | object      | No         | -                                 | Client Args                     |

#### <a name="llm_unit_anyOf_i0_implementation"></a>5.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AnthropicLLMUnit

Specific value: `"AnthropicLLMUnit"`

#### <a name="llm_unit_anyOf_i0_model"></a>5.1.2. Property `model`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{"implementation": "LLMModel"}`                                          |
| **Defined in**            | [LLMModel](/docs/components/llmmodel/overview)                                            |

**Description:** Overview of LLMModel components

| Any of(Option)                                                     |
| ------------------------------------------------------------------ |
| [claude-3-haiku-20240307.json](#llm_unit_anyOf_i0_model_anyOf_i0)  |
| [claude-3-opus-20240229.json](#llm_unit_anyOf_i0_model_anyOf_i1)   |
| [claude-3-sonnet-20240229.json](#llm_unit_anyOf_i0_model_anyOf_i2) |
| [gpt-3.5-turbo.json](#llm_unit_anyOf_i0_model_anyOf_i3)            |
| [gpt-4-turbo.json](#llm_unit_anyOf_i0_model_anyOf_i4)              |
| [gpt-4o.json](#llm_unit_anyOf_i0_model_anyOf_i5)                   |
| [llama3-8b.json](#llm_unit_anyOf_i0_model_anyOf_i6)                |
| [mistral-large-latest.json](#llm_unit_anyOf_i0_model_anyOf_i7)     |
| [mistral-medium-latest.json](#llm_unit_anyOf_i0_model_anyOf_i8)    |
| [mistral-small-latest.json](#llm_unit_anyOf_i0_model_anyOf_i9)     |

##### <a name="llm_unit_anyOf_i0_model_anyOf_i0"></a>5.1.2.1. Property `claude-3-haiku-20240307.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./claude-3-haiku-20240307.json                                       |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description       |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | ----------------------- |
| - [implementation](#llm_unit_anyOf_i0_model_anyOf_i0_implementation )             | No      | const   | No         | -          | claude-3-haiku-20240307 |
| + [human_name](#llm_unit_anyOf_i0_model_anyOf_i0_human_name )                     | No      | string  | No         | -          | Human Name              |
| + [name](#llm_unit_anyOf_i0_model_anyOf_i0_name )                                 | No      | string  | No         | -          | Name                    |
| + [input_context_limit](#llm_unit_anyOf_i0_model_anyOf_i0_input_context_limit )   | No      | integer | No         | -          | Input Context Limit     |
| + [output_context_limit](#llm_unit_anyOf_i0_model_anyOf_i0_output_context_limit ) | No      | integer | No         | -          | Output Context Limit    |
| + [supports_tools](#llm_unit_anyOf_i0_model_anyOf_i0_supports_tools )             | No      | boolean | No         | -          | Supports Tools          |
| + [supports_image_input](#llm_unit_anyOf_i0_model_anyOf_i0_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input    |
| + [supports_audio_input](#llm_unit_anyOf_i0_model_anyOf_i0_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input    |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i0_implementation"></a>5.1.2.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** claude-3-haiku-20240307

Specific value: `"claude-3-haiku-20240307"`

###### <a name="llm_unit_anyOf_i0_model_anyOf_i0_human_name"></a>5.1.2.1.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i0_name"></a>5.1.2.1.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i0_input_context_limit"></a>5.1.2.1.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i0_output_context_limit"></a>5.1.2.1.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i0_supports_tools"></a>5.1.2.1.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i0_supports_image_input"></a>5.1.2.1.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i0_supports_audio_input"></a>5.1.2.1.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_anyOf_i0_model_anyOf_i1"></a>5.1.2.2. Property `claude-3-opus-20240229.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./claude-3-opus-20240229.json                                        |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description      |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | ---------------------- |
| - [implementation](#llm_unit_anyOf_i0_model_anyOf_i1_implementation )             | No      | const   | No         | -          | claude-3-opus-20240229 |
| + [human_name](#llm_unit_anyOf_i0_model_anyOf_i1_human_name )                     | No      | string  | No         | -          | Human Name             |
| + [name](#llm_unit_anyOf_i0_model_anyOf_i1_name )                                 | No      | string  | No         | -          | Name                   |
| + [input_context_limit](#llm_unit_anyOf_i0_model_anyOf_i1_input_context_limit )   | No      | integer | No         | -          | Input Context Limit    |
| + [output_context_limit](#llm_unit_anyOf_i0_model_anyOf_i1_output_context_limit ) | No      | integer | No         | -          | Output Context Limit   |
| + [supports_tools](#llm_unit_anyOf_i0_model_anyOf_i1_supports_tools )             | No      | boolean | No         | -          | Supports Tools         |
| + [supports_image_input](#llm_unit_anyOf_i0_model_anyOf_i1_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input   |
| + [supports_audio_input](#llm_unit_anyOf_i0_model_anyOf_i1_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input   |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i1_implementation"></a>5.1.2.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** claude-3-opus-20240229

Specific value: `"claude-3-opus-20240229"`

###### <a name="llm_unit_anyOf_i0_model_anyOf_i1_human_name"></a>5.1.2.2.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i1_name"></a>5.1.2.2.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i1_input_context_limit"></a>5.1.2.2.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i1_output_context_limit"></a>5.1.2.2.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i1_supports_tools"></a>5.1.2.2.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i1_supports_image_input"></a>5.1.2.2.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i1_supports_audio_input"></a>5.1.2.2.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_anyOf_i0_model_anyOf_i2"></a>5.1.2.3. Property `claude-3-sonnet-20240229.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./claude-3-sonnet-20240229.json                                      |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description        |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | ------------------------ |
| - [implementation](#llm_unit_anyOf_i0_model_anyOf_i2_implementation )             | No      | const   | No         | -          | claude-3-sonnet-20240229 |
| + [human_name](#llm_unit_anyOf_i0_model_anyOf_i2_human_name )                     | No      | string  | No         | -          | Human Name               |
| + [name](#llm_unit_anyOf_i0_model_anyOf_i2_name )                                 | No      | string  | No         | -          | Name                     |
| + [input_context_limit](#llm_unit_anyOf_i0_model_anyOf_i2_input_context_limit )   | No      | integer | No         | -          | Input Context Limit      |
| + [output_context_limit](#llm_unit_anyOf_i0_model_anyOf_i2_output_context_limit ) | No      | integer | No         | -          | Output Context Limit     |
| + [supports_tools](#llm_unit_anyOf_i0_model_anyOf_i2_supports_tools )             | No      | boolean | No         | -          | Supports Tools           |
| + [supports_image_input](#llm_unit_anyOf_i0_model_anyOf_i2_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input     |
| + [supports_audio_input](#llm_unit_anyOf_i0_model_anyOf_i2_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input     |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i2_implementation"></a>5.1.2.3.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** claude-3-sonnet-20240229

Specific value: `"claude-3-sonnet-20240229"`

###### <a name="llm_unit_anyOf_i0_model_anyOf_i2_human_name"></a>5.1.2.3.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i2_name"></a>5.1.2.3.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i2_input_context_limit"></a>5.1.2.3.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i2_output_context_limit"></a>5.1.2.3.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i2_supports_tools"></a>5.1.2.3.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i2_supports_image_input"></a>5.1.2.3.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i2_supports_audio_input"></a>5.1.2.3.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_anyOf_i0_model_anyOf_i3"></a>5.1.2.4. Property `gpt-3.5-turbo.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./gpt-3.5-turbo.json                                                 |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_anyOf_i0_model_anyOf_i3_implementation )             | No      | const   | No         | -          | gpt-3.5-turbo        |
| + [human_name](#llm_unit_anyOf_i0_model_anyOf_i3_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_anyOf_i0_model_anyOf_i3_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_anyOf_i0_model_anyOf_i3_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_anyOf_i0_model_anyOf_i3_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_anyOf_i0_model_anyOf_i3_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_anyOf_i0_model_anyOf_i3_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_anyOf_i0_model_anyOf_i3_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i3_implementation"></a>5.1.2.4.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** gpt-3.5-turbo

Specific value: `"gpt-3.5-turbo"`

###### <a name="llm_unit_anyOf_i0_model_anyOf_i3_human_name"></a>5.1.2.4.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i3_name"></a>5.1.2.4.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i3_input_context_limit"></a>5.1.2.4.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i3_output_context_limit"></a>5.1.2.4.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i3_supports_tools"></a>5.1.2.4.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i3_supports_image_input"></a>5.1.2.4.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i3_supports_audio_input"></a>5.1.2.4.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_anyOf_i0_model_anyOf_i4"></a>5.1.2.5. Property `gpt-4-turbo.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./gpt-4-turbo.json                                                   |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_anyOf_i0_model_anyOf_i4_implementation )             | No      | const   | No         | -          | gpt-4-turbo          |
| + [human_name](#llm_unit_anyOf_i0_model_anyOf_i4_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_anyOf_i0_model_anyOf_i4_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_anyOf_i0_model_anyOf_i4_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_anyOf_i0_model_anyOf_i4_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_anyOf_i0_model_anyOf_i4_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_anyOf_i0_model_anyOf_i4_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_anyOf_i0_model_anyOf_i4_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i4_implementation"></a>5.1.2.5.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** gpt-4-turbo

Specific value: `"gpt-4-turbo"`

###### <a name="llm_unit_anyOf_i0_model_anyOf_i4_human_name"></a>5.1.2.5.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i4_name"></a>5.1.2.5.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i4_input_context_limit"></a>5.1.2.5.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i4_output_context_limit"></a>5.1.2.5.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i4_supports_tools"></a>5.1.2.5.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i4_supports_image_input"></a>5.1.2.5.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i4_supports_audio_input"></a>5.1.2.5.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_anyOf_i0_model_anyOf_i5"></a>5.1.2.6. Property `gpt-4o.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./gpt-4o.json                                                        |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_anyOf_i0_model_anyOf_i5_implementation )             | No      | const   | No         | -          | gpt-4o               |
| + [human_name](#llm_unit_anyOf_i0_model_anyOf_i5_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_anyOf_i0_model_anyOf_i5_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_anyOf_i0_model_anyOf_i5_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_anyOf_i0_model_anyOf_i5_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_anyOf_i0_model_anyOf_i5_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_anyOf_i0_model_anyOf_i5_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_anyOf_i0_model_anyOf_i5_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i5_implementation"></a>5.1.2.6.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** gpt-4o

Specific value: `"gpt-4o"`

###### <a name="llm_unit_anyOf_i0_model_anyOf_i5_human_name"></a>5.1.2.6.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i5_name"></a>5.1.2.6.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i5_input_context_limit"></a>5.1.2.6.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i5_output_context_limit"></a>5.1.2.6.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i5_supports_tools"></a>5.1.2.6.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i5_supports_image_input"></a>5.1.2.6.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i5_supports_audio_input"></a>5.1.2.6.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_anyOf_i0_model_anyOf_i6"></a>5.1.2.7. Property `llama3-8b.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./llama3-8b.json                                                     |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_anyOf_i0_model_anyOf_i6_implementation )             | No      | const   | No         | -          | llama3-8b            |
| + [human_name](#llm_unit_anyOf_i0_model_anyOf_i6_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_anyOf_i0_model_anyOf_i6_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_anyOf_i0_model_anyOf_i6_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_anyOf_i0_model_anyOf_i6_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_anyOf_i0_model_anyOf_i6_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_anyOf_i0_model_anyOf_i6_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_anyOf_i0_model_anyOf_i6_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i6_implementation"></a>5.1.2.7.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** llama3-8b

Specific value: `"llama3-8b"`

###### <a name="llm_unit_anyOf_i0_model_anyOf_i6_human_name"></a>5.1.2.7.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i6_name"></a>5.1.2.7.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i6_input_context_limit"></a>5.1.2.7.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i6_output_context_limit"></a>5.1.2.7.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i6_supports_tools"></a>5.1.2.7.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i6_supports_image_input"></a>5.1.2.7.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i6_supports_audio_input"></a>5.1.2.7.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_anyOf_i0_model_anyOf_i7"></a>5.1.2.8. Property `mistral-large-latest.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./mistral-large-latest.json                                          |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_anyOf_i0_model_anyOf_i7_implementation )             | No      | const   | No         | -          | mistral-large-latest |
| + [human_name](#llm_unit_anyOf_i0_model_anyOf_i7_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_anyOf_i0_model_anyOf_i7_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_anyOf_i0_model_anyOf_i7_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_anyOf_i0_model_anyOf_i7_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_anyOf_i0_model_anyOf_i7_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_anyOf_i0_model_anyOf_i7_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_anyOf_i0_model_anyOf_i7_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i7_implementation"></a>5.1.2.8.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** mistral-large-latest

Specific value: `"mistral-large-latest"`

###### <a name="llm_unit_anyOf_i0_model_anyOf_i7_human_name"></a>5.1.2.8.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i7_name"></a>5.1.2.8.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i7_input_context_limit"></a>5.1.2.8.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i7_output_context_limit"></a>5.1.2.8.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i7_supports_tools"></a>5.1.2.8.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i7_supports_image_input"></a>5.1.2.8.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i7_supports_audio_input"></a>5.1.2.8.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_anyOf_i0_model_anyOf_i8"></a>5.1.2.9. Property `mistral-medium-latest.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./mistral-medium-latest.json                                         |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description     |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | --------------------- |
| - [implementation](#llm_unit_anyOf_i0_model_anyOf_i8_implementation )             | No      | const   | No         | -          | mistral-medium-latest |
| + [human_name](#llm_unit_anyOf_i0_model_anyOf_i8_human_name )                     | No      | string  | No         | -          | Human Name            |
| + [name](#llm_unit_anyOf_i0_model_anyOf_i8_name )                                 | No      | string  | No         | -          | Name                  |
| + [input_context_limit](#llm_unit_anyOf_i0_model_anyOf_i8_input_context_limit )   | No      | integer | No         | -          | Input Context Limit   |
| + [output_context_limit](#llm_unit_anyOf_i0_model_anyOf_i8_output_context_limit ) | No      | integer | No         | -          | Output Context Limit  |
| + [supports_tools](#llm_unit_anyOf_i0_model_anyOf_i8_supports_tools )             | No      | boolean | No         | -          | Supports Tools        |
| + [supports_image_input](#llm_unit_anyOf_i0_model_anyOf_i8_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input  |
| + [supports_audio_input](#llm_unit_anyOf_i0_model_anyOf_i8_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input  |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i8_implementation"></a>5.1.2.9.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** mistral-medium-latest

Specific value: `"mistral-medium-latest"`

###### <a name="llm_unit_anyOf_i0_model_anyOf_i8_human_name"></a>5.1.2.9.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i8_name"></a>5.1.2.9.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i8_input_context_limit"></a>5.1.2.9.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i8_output_context_limit"></a>5.1.2.9.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i8_supports_tools"></a>5.1.2.9.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i8_supports_image_input"></a>5.1.2.9.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i8_supports_audio_input"></a>5.1.2.9.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_anyOf_i0_model_anyOf_i9"></a>5.1.2.10. Property `mistral-small-latest.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./mistral-small-latest.json                                          |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_anyOf_i0_model_anyOf_i9_implementation )             | No      | const   | No         | -          | mistral-small-latest |
| + [human_name](#llm_unit_anyOf_i0_model_anyOf_i9_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_anyOf_i0_model_anyOf_i9_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_anyOf_i0_model_anyOf_i9_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_anyOf_i0_model_anyOf_i9_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_anyOf_i0_model_anyOf_i9_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_anyOf_i0_model_anyOf_i9_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_anyOf_i0_model_anyOf_i9_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i9_implementation"></a>5.1.2.10.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** mistral-small-latest

Specific value: `"mistral-small-latest"`

###### <a name="llm_unit_anyOf_i0_model_anyOf_i9_human_name"></a>5.1.2.10.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i9_name"></a>5.1.2.10.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i9_input_context_limit"></a>5.1.2.10.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i9_output_context_limit"></a>5.1.2.10.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i9_supports_tools"></a>5.1.2.10.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i9_supports_image_input"></a>5.1.2.10.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i9_supports_audio_input"></a>5.1.2.10.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

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

| Property                                               | Pattern | Type        | Deprecated | Definition                        | Title/Description               |
| ------------------------------------------------------ | ------- | ----------- | ---------- | --------------------------------- | ------------------------------- |
| - [implementation](#llm_unit_anyOf_i1_implementation ) | No      | const       | No         | -                                 | MistralGPT                      |
| - [model](#llm_unit_anyOf_i1_model )                   | No      | object      | No         | In [LLMModel](/docs/components/llmmodel/overview) | Overview of LLMModel components |
| - [temperature](#llm_unit_anyOf_i1_temperature )       | No      | number      | No         | -                                 | Temperature                     |
| - [force_json](#llm_unit_anyOf_i1_force_json )         | No      | boolean     | No         | -                                 | Force Json                      |
| - [max_tokens](#llm_unit_anyOf_i1_max_tokens )         | No      | Combination | No         | -                                 | Max Tokens                      |
| - [client_args](#llm_unit_anyOf_i1_client_args )       | No      | object      | No         | -                                 | Client Args                     |

#### <a name="llm_unit_anyOf_i1_implementation"></a>5.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** MistralGPT

Specific value: `"MistralGPT"`

#### <a name="llm_unit_anyOf_i1_model"></a>5.2.2. Property `model`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{"implementation": "LLMModel"}`                                          |
| **Defined in**            | [LLMModel](/docs/components/llmmodel/overview)                                            |

**Description:** Overview of LLMModel components

| Any of(Option)                                                     |
| ------------------------------------------------------------------ |
| [claude-3-haiku-20240307.json](#llm_unit_anyOf_i0_model_anyOf_i0)  |
| [claude-3-opus-20240229.json](#llm_unit_anyOf_i0_model_anyOf_i1)   |
| [claude-3-sonnet-20240229.json](#llm_unit_anyOf_i0_model_anyOf_i2) |
| [gpt-3.5-turbo.json](#llm_unit_anyOf_i0_model_anyOf_i3)            |
| [gpt-4-turbo.json](#llm_unit_anyOf_i0_model_anyOf_i4)              |
| [gpt-4o.json](#llm_unit_anyOf_i0_model_anyOf_i5)                   |
| [llama3-8b.json](#llm_unit_anyOf_i0_model_anyOf_i6)                |
| [mistral-large-latest.json](#llm_unit_anyOf_i0_model_anyOf_i7)     |
| [mistral-medium-latest.json](#llm_unit_anyOf_i0_model_anyOf_i8)    |
| [mistral-small-latest.json](#llm_unit_anyOf_i0_model_anyOf_i9)     |

##### <a name="llm_unit_anyOf_i0_model_anyOf_i0"></a>5.2.2.1. Property `claude-3-haiku-20240307.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./claude-3-haiku-20240307.json                                       |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description       |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | ----------------------- |
| - [implementation](#llm_unit_anyOf_i0_model_anyOf_i0_implementation )             | No      | const   | No         | -          | claude-3-haiku-20240307 |
| + [human_name](#llm_unit_anyOf_i0_model_anyOf_i0_human_name )                     | No      | string  | No         | -          | Human Name              |
| + [name](#llm_unit_anyOf_i0_model_anyOf_i0_name )                                 | No      | string  | No         | -          | Name                    |
| + [input_context_limit](#llm_unit_anyOf_i0_model_anyOf_i0_input_context_limit )   | No      | integer | No         | -          | Input Context Limit     |
| + [output_context_limit](#llm_unit_anyOf_i0_model_anyOf_i0_output_context_limit ) | No      | integer | No         | -          | Output Context Limit    |
| + [supports_tools](#llm_unit_anyOf_i0_model_anyOf_i0_supports_tools )             | No      | boolean | No         | -          | Supports Tools          |
| + [supports_image_input](#llm_unit_anyOf_i0_model_anyOf_i0_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input    |
| + [supports_audio_input](#llm_unit_anyOf_i0_model_anyOf_i0_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input    |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i0_implementation"></a>5.2.2.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** claude-3-haiku-20240307

Specific value: `"claude-3-haiku-20240307"`

###### <a name="llm_unit_anyOf_i0_model_anyOf_i0_human_name"></a>5.2.2.1.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i0_name"></a>5.2.2.1.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i0_input_context_limit"></a>5.2.2.1.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i0_output_context_limit"></a>5.2.2.1.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i0_supports_tools"></a>5.2.2.1.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i0_supports_image_input"></a>5.2.2.1.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i0_supports_audio_input"></a>5.2.2.1.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_anyOf_i0_model_anyOf_i1"></a>5.2.2.2. Property `claude-3-opus-20240229.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./claude-3-opus-20240229.json                                        |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description      |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | ---------------------- |
| - [implementation](#llm_unit_anyOf_i0_model_anyOf_i1_implementation )             | No      | const   | No         | -          | claude-3-opus-20240229 |
| + [human_name](#llm_unit_anyOf_i0_model_anyOf_i1_human_name )                     | No      | string  | No         | -          | Human Name             |
| + [name](#llm_unit_anyOf_i0_model_anyOf_i1_name )                                 | No      | string  | No         | -          | Name                   |
| + [input_context_limit](#llm_unit_anyOf_i0_model_anyOf_i1_input_context_limit )   | No      | integer | No         | -          | Input Context Limit    |
| + [output_context_limit](#llm_unit_anyOf_i0_model_anyOf_i1_output_context_limit ) | No      | integer | No         | -          | Output Context Limit   |
| + [supports_tools](#llm_unit_anyOf_i0_model_anyOf_i1_supports_tools )             | No      | boolean | No         | -          | Supports Tools         |
| + [supports_image_input](#llm_unit_anyOf_i0_model_anyOf_i1_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input   |
| + [supports_audio_input](#llm_unit_anyOf_i0_model_anyOf_i1_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input   |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i1_implementation"></a>5.2.2.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** claude-3-opus-20240229

Specific value: `"claude-3-opus-20240229"`

###### <a name="llm_unit_anyOf_i0_model_anyOf_i1_human_name"></a>5.2.2.2.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i1_name"></a>5.2.2.2.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i1_input_context_limit"></a>5.2.2.2.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i1_output_context_limit"></a>5.2.2.2.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i1_supports_tools"></a>5.2.2.2.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i1_supports_image_input"></a>5.2.2.2.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i1_supports_audio_input"></a>5.2.2.2.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_anyOf_i0_model_anyOf_i2"></a>5.2.2.3. Property `claude-3-sonnet-20240229.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./claude-3-sonnet-20240229.json                                      |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description        |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | ------------------------ |
| - [implementation](#llm_unit_anyOf_i0_model_anyOf_i2_implementation )             | No      | const   | No         | -          | claude-3-sonnet-20240229 |
| + [human_name](#llm_unit_anyOf_i0_model_anyOf_i2_human_name )                     | No      | string  | No         | -          | Human Name               |
| + [name](#llm_unit_anyOf_i0_model_anyOf_i2_name )                                 | No      | string  | No         | -          | Name                     |
| + [input_context_limit](#llm_unit_anyOf_i0_model_anyOf_i2_input_context_limit )   | No      | integer | No         | -          | Input Context Limit      |
| + [output_context_limit](#llm_unit_anyOf_i0_model_anyOf_i2_output_context_limit ) | No      | integer | No         | -          | Output Context Limit     |
| + [supports_tools](#llm_unit_anyOf_i0_model_anyOf_i2_supports_tools )             | No      | boolean | No         | -          | Supports Tools           |
| + [supports_image_input](#llm_unit_anyOf_i0_model_anyOf_i2_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input     |
| + [supports_audio_input](#llm_unit_anyOf_i0_model_anyOf_i2_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input     |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i2_implementation"></a>5.2.2.3.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** claude-3-sonnet-20240229

Specific value: `"claude-3-sonnet-20240229"`

###### <a name="llm_unit_anyOf_i0_model_anyOf_i2_human_name"></a>5.2.2.3.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i2_name"></a>5.2.2.3.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i2_input_context_limit"></a>5.2.2.3.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i2_output_context_limit"></a>5.2.2.3.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i2_supports_tools"></a>5.2.2.3.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i2_supports_image_input"></a>5.2.2.3.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i2_supports_audio_input"></a>5.2.2.3.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_anyOf_i0_model_anyOf_i3"></a>5.2.2.4. Property `gpt-3.5-turbo.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./gpt-3.5-turbo.json                                                 |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_anyOf_i0_model_anyOf_i3_implementation )             | No      | const   | No         | -          | gpt-3.5-turbo        |
| + [human_name](#llm_unit_anyOf_i0_model_anyOf_i3_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_anyOf_i0_model_anyOf_i3_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_anyOf_i0_model_anyOf_i3_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_anyOf_i0_model_anyOf_i3_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_anyOf_i0_model_anyOf_i3_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_anyOf_i0_model_anyOf_i3_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_anyOf_i0_model_anyOf_i3_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i3_implementation"></a>5.2.2.4.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** gpt-3.5-turbo

Specific value: `"gpt-3.5-turbo"`

###### <a name="llm_unit_anyOf_i0_model_anyOf_i3_human_name"></a>5.2.2.4.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i3_name"></a>5.2.2.4.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i3_input_context_limit"></a>5.2.2.4.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i3_output_context_limit"></a>5.2.2.4.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i3_supports_tools"></a>5.2.2.4.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i3_supports_image_input"></a>5.2.2.4.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i3_supports_audio_input"></a>5.2.2.4.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_anyOf_i0_model_anyOf_i4"></a>5.2.2.5. Property `gpt-4-turbo.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./gpt-4-turbo.json                                                   |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_anyOf_i0_model_anyOf_i4_implementation )             | No      | const   | No         | -          | gpt-4-turbo          |
| + [human_name](#llm_unit_anyOf_i0_model_anyOf_i4_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_anyOf_i0_model_anyOf_i4_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_anyOf_i0_model_anyOf_i4_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_anyOf_i0_model_anyOf_i4_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_anyOf_i0_model_anyOf_i4_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_anyOf_i0_model_anyOf_i4_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_anyOf_i0_model_anyOf_i4_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i4_implementation"></a>5.2.2.5.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** gpt-4-turbo

Specific value: `"gpt-4-turbo"`

###### <a name="llm_unit_anyOf_i0_model_anyOf_i4_human_name"></a>5.2.2.5.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i4_name"></a>5.2.2.5.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i4_input_context_limit"></a>5.2.2.5.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i4_output_context_limit"></a>5.2.2.5.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i4_supports_tools"></a>5.2.2.5.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i4_supports_image_input"></a>5.2.2.5.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i4_supports_audio_input"></a>5.2.2.5.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_anyOf_i0_model_anyOf_i5"></a>5.2.2.6. Property `gpt-4o.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./gpt-4o.json                                                        |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_anyOf_i0_model_anyOf_i5_implementation )             | No      | const   | No         | -          | gpt-4o               |
| + [human_name](#llm_unit_anyOf_i0_model_anyOf_i5_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_anyOf_i0_model_anyOf_i5_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_anyOf_i0_model_anyOf_i5_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_anyOf_i0_model_anyOf_i5_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_anyOf_i0_model_anyOf_i5_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_anyOf_i0_model_anyOf_i5_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_anyOf_i0_model_anyOf_i5_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i5_implementation"></a>5.2.2.6.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** gpt-4o

Specific value: `"gpt-4o"`

###### <a name="llm_unit_anyOf_i0_model_anyOf_i5_human_name"></a>5.2.2.6.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i5_name"></a>5.2.2.6.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i5_input_context_limit"></a>5.2.2.6.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i5_output_context_limit"></a>5.2.2.6.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i5_supports_tools"></a>5.2.2.6.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i5_supports_image_input"></a>5.2.2.6.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i5_supports_audio_input"></a>5.2.2.6.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_anyOf_i0_model_anyOf_i6"></a>5.2.2.7. Property `llama3-8b.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./llama3-8b.json                                                     |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_anyOf_i0_model_anyOf_i6_implementation )             | No      | const   | No         | -          | llama3-8b            |
| + [human_name](#llm_unit_anyOf_i0_model_anyOf_i6_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_anyOf_i0_model_anyOf_i6_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_anyOf_i0_model_anyOf_i6_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_anyOf_i0_model_anyOf_i6_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_anyOf_i0_model_anyOf_i6_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_anyOf_i0_model_anyOf_i6_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_anyOf_i0_model_anyOf_i6_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i6_implementation"></a>5.2.2.7.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** llama3-8b

Specific value: `"llama3-8b"`

###### <a name="llm_unit_anyOf_i0_model_anyOf_i6_human_name"></a>5.2.2.7.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i6_name"></a>5.2.2.7.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i6_input_context_limit"></a>5.2.2.7.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i6_output_context_limit"></a>5.2.2.7.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i6_supports_tools"></a>5.2.2.7.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i6_supports_image_input"></a>5.2.2.7.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i6_supports_audio_input"></a>5.2.2.7.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_anyOf_i0_model_anyOf_i7"></a>5.2.2.8. Property `mistral-large-latest.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./mistral-large-latest.json                                          |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_anyOf_i0_model_anyOf_i7_implementation )             | No      | const   | No         | -          | mistral-large-latest |
| + [human_name](#llm_unit_anyOf_i0_model_anyOf_i7_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_anyOf_i0_model_anyOf_i7_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_anyOf_i0_model_anyOf_i7_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_anyOf_i0_model_anyOf_i7_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_anyOf_i0_model_anyOf_i7_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_anyOf_i0_model_anyOf_i7_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_anyOf_i0_model_anyOf_i7_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i7_implementation"></a>5.2.2.8.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** mistral-large-latest

Specific value: `"mistral-large-latest"`

###### <a name="llm_unit_anyOf_i0_model_anyOf_i7_human_name"></a>5.2.2.8.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i7_name"></a>5.2.2.8.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i7_input_context_limit"></a>5.2.2.8.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i7_output_context_limit"></a>5.2.2.8.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i7_supports_tools"></a>5.2.2.8.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i7_supports_image_input"></a>5.2.2.8.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i7_supports_audio_input"></a>5.2.2.8.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_anyOf_i0_model_anyOf_i8"></a>5.2.2.9. Property `mistral-medium-latest.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./mistral-medium-latest.json                                         |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description     |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | --------------------- |
| - [implementation](#llm_unit_anyOf_i0_model_anyOf_i8_implementation )             | No      | const   | No         | -          | mistral-medium-latest |
| + [human_name](#llm_unit_anyOf_i0_model_anyOf_i8_human_name )                     | No      | string  | No         | -          | Human Name            |
| + [name](#llm_unit_anyOf_i0_model_anyOf_i8_name )                                 | No      | string  | No         | -          | Name                  |
| + [input_context_limit](#llm_unit_anyOf_i0_model_anyOf_i8_input_context_limit )   | No      | integer | No         | -          | Input Context Limit   |
| + [output_context_limit](#llm_unit_anyOf_i0_model_anyOf_i8_output_context_limit ) | No      | integer | No         | -          | Output Context Limit  |
| + [supports_tools](#llm_unit_anyOf_i0_model_anyOf_i8_supports_tools )             | No      | boolean | No         | -          | Supports Tools        |
| + [supports_image_input](#llm_unit_anyOf_i0_model_anyOf_i8_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input  |
| + [supports_audio_input](#llm_unit_anyOf_i0_model_anyOf_i8_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input  |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i8_implementation"></a>5.2.2.9.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** mistral-medium-latest

Specific value: `"mistral-medium-latest"`

###### <a name="llm_unit_anyOf_i0_model_anyOf_i8_human_name"></a>5.2.2.9.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i8_name"></a>5.2.2.9.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i8_input_context_limit"></a>5.2.2.9.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i8_output_context_limit"></a>5.2.2.9.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i8_supports_tools"></a>5.2.2.9.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i8_supports_image_input"></a>5.2.2.9.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i8_supports_audio_input"></a>5.2.2.9.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_anyOf_i0_model_anyOf_i9"></a>5.2.2.10. Property `mistral-small-latest.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./mistral-small-latest.json                                          |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_anyOf_i0_model_anyOf_i9_implementation )             | No      | const   | No         | -          | mistral-small-latest |
| + [human_name](#llm_unit_anyOf_i0_model_anyOf_i9_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_anyOf_i0_model_anyOf_i9_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_anyOf_i0_model_anyOf_i9_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_anyOf_i0_model_anyOf_i9_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_anyOf_i0_model_anyOf_i9_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_anyOf_i0_model_anyOf_i9_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_anyOf_i0_model_anyOf_i9_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i9_implementation"></a>5.2.2.10.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** mistral-small-latest

Specific value: `"mistral-small-latest"`

###### <a name="llm_unit_anyOf_i0_model_anyOf_i9_human_name"></a>5.2.2.10.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i9_name"></a>5.2.2.10.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i9_input_context_limit"></a>5.2.2.10.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i9_output_context_limit"></a>5.2.2.10.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i9_supports_tools"></a>5.2.2.10.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i9_supports_image_input"></a>5.2.2.10.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i9_supports_audio_input"></a>5.2.2.10.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

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

### <a name="llm_unit_anyOf_i2"></a>5.3. Property `OllamaLLMUnit.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./OllamaLLMUnit.json                                                 |

| Property                                               | Pattern | Type        | Deprecated | Definition                        | Title/Description               |
| ------------------------------------------------------ | ------- | ----------- | ---------- | --------------------------------- | ------------------------------- |
| - [implementation](#llm_unit_anyOf_i2_implementation ) | No      | const       | No         | -                                 | OllamaLLMUnit                   |
| - [model](#llm_unit_anyOf_i2_model )                   | No      | object      | No         | In [LLMModel](/docs/components/llmmodel/overview) | Overview of LLMModel components |
| - [temperature](#llm_unit_anyOf_i2_temperature )       | No      | number      | No         | -                                 | Temperature                     |
| - [force_json](#llm_unit_anyOf_i2_force_json )         | No      | boolean     | No         | -                                 | Force Json                      |
| - [max_tokens](#llm_unit_anyOf_i2_max_tokens )         | No      | Combination | No         | -                                 | Max Tokens                      |
| - [client_options](#llm_unit_anyOf_i2_client_options ) | No      | object      | No         | -                                 | Client Options                  |

#### <a name="llm_unit_anyOf_i2_implementation"></a>5.3.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OllamaLLMUnit

Specific value: `"OllamaLLMUnit"`

#### <a name="llm_unit_anyOf_i2_model"></a>5.3.2. Property `model`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{"implementation": "llama3"}`                                            |
| **Defined in**            | [LLMModel](/docs/components/llmmodel/overview)                                            |

**Description:** Overview of LLMModel components

| Any of(Option)                                                     |
| ------------------------------------------------------------------ |
| [claude-3-haiku-20240307.json](#llm_unit_anyOf_i0_model_anyOf_i0)  |
| [claude-3-opus-20240229.json](#llm_unit_anyOf_i0_model_anyOf_i1)   |
| [claude-3-sonnet-20240229.json](#llm_unit_anyOf_i0_model_anyOf_i2) |
| [gpt-3.5-turbo.json](#llm_unit_anyOf_i0_model_anyOf_i3)            |
| [gpt-4-turbo.json](#llm_unit_anyOf_i0_model_anyOf_i4)              |
| [gpt-4o.json](#llm_unit_anyOf_i0_model_anyOf_i5)                   |
| [llama3-8b.json](#llm_unit_anyOf_i0_model_anyOf_i6)                |
| [mistral-large-latest.json](#llm_unit_anyOf_i0_model_anyOf_i7)     |
| [mistral-medium-latest.json](#llm_unit_anyOf_i0_model_anyOf_i8)    |
| [mistral-small-latest.json](#llm_unit_anyOf_i0_model_anyOf_i9)     |

##### <a name="llm_unit_anyOf_i0_model_anyOf_i0"></a>5.3.2.1. Property `claude-3-haiku-20240307.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./claude-3-haiku-20240307.json                                       |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description       |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | ----------------------- |
| - [implementation](#llm_unit_anyOf_i0_model_anyOf_i0_implementation )             | No      | const   | No         | -          | claude-3-haiku-20240307 |
| + [human_name](#llm_unit_anyOf_i0_model_anyOf_i0_human_name )                     | No      | string  | No         | -          | Human Name              |
| + [name](#llm_unit_anyOf_i0_model_anyOf_i0_name )                                 | No      | string  | No         | -          | Name                    |
| + [input_context_limit](#llm_unit_anyOf_i0_model_anyOf_i0_input_context_limit )   | No      | integer | No         | -          | Input Context Limit     |
| + [output_context_limit](#llm_unit_anyOf_i0_model_anyOf_i0_output_context_limit ) | No      | integer | No         | -          | Output Context Limit    |
| + [supports_tools](#llm_unit_anyOf_i0_model_anyOf_i0_supports_tools )             | No      | boolean | No         | -          | Supports Tools          |
| + [supports_image_input](#llm_unit_anyOf_i0_model_anyOf_i0_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input    |
| + [supports_audio_input](#llm_unit_anyOf_i0_model_anyOf_i0_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input    |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i0_implementation"></a>5.3.2.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** claude-3-haiku-20240307

Specific value: `"claude-3-haiku-20240307"`

###### <a name="llm_unit_anyOf_i0_model_anyOf_i0_human_name"></a>5.3.2.1.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i0_name"></a>5.3.2.1.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i0_input_context_limit"></a>5.3.2.1.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i0_output_context_limit"></a>5.3.2.1.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i0_supports_tools"></a>5.3.2.1.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i0_supports_image_input"></a>5.3.2.1.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i0_supports_audio_input"></a>5.3.2.1.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_anyOf_i0_model_anyOf_i1"></a>5.3.2.2. Property `claude-3-opus-20240229.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./claude-3-opus-20240229.json                                        |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description      |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | ---------------------- |
| - [implementation](#llm_unit_anyOf_i0_model_anyOf_i1_implementation )             | No      | const   | No         | -          | claude-3-opus-20240229 |
| + [human_name](#llm_unit_anyOf_i0_model_anyOf_i1_human_name )                     | No      | string  | No         | -          | Human Name             |
| + [name](#llm_unit_anyOf_i0_model_anyOf_i1_name )                                 | No      | string  | No         | -          | Name                   |
| + [input_context_limit](#llm_unit_anyOf_i0_model_anyOf_i1_input_context_limit )   | No      | integer | No         | -          | Input Context Limit    |
| + [output_context_limit](#llm_unit_anyOf_i0_model_anyOf_i1_output_context_limit ) | No      | integer | No         | -          | Output Context Limit   |
| + [supports_tools](#llm_unit_anyOf_i0_model_anyOf_i1_supports_tools )             | No      | boolean | No         | -          | Supports Tools         |
| + [supports_image_input](#llm_unit_anyOf_i0_model_anyOf_i1_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input   |
| + [supports_audio_input](#llm_unit_anyOf_i0_model_anyOf_i1_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input   |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i1_implementation"></a>5.3.2.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** claude-3-opus-20240229

Specific value: `"claude-3-opus-20240229"`

###### <a name="llm_unit_anyOf_i0_model_anyOf_i1_human_name"></a>5.3.2.2.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i1_name"></a>5.3.2.2.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i1_input_context_limit"></a>5.3.2.2.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i1_output_context_limit"></a>5.3.2.2.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i1_supports_tools"></a>5.3.2.2.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i1_supports_image_input"></a>5.3.2.2.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i1_supports_audio_input"></a>5.3.2.2.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_anyOf_i0_model_anyOf_i2"></a>5.3.2.3. Property `claude-3-sonnet-20240229.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./claude-3-sonnet-20240229.json                                      |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description        |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | ------------------------ |
| - [implementation](#llm_unit_anyOf_i0_model_anyOf_i2_implementation )             | No      | const   | No         | -          | claude-3-sonnet-20240229 |
| + [human_name](#llm_unit_anyOf_i0_model_anyOf_i2_human_name )                     | No      | string  | No         | -          | Human Name               |
| + [name](#llm_unit_anyOf_i0_model_anyOf_i2_name )                                 | No      | string  | No         | -          | Name                     |
| + [input_context_limit](#llm_unit_anyOf_i0_model_anyOf_i2_input_context_limit )   | No      | integer | No         | -          | Input Context Limit      |
| + [output_context_limit](#llm_unit_anyOf_i0_model_anyOf_i2_output_context_limit ) | No      | integer | No         | -          | Output Context Limit     |
| + [supports_tools](#llm_unit_anyOf_i0_model_anyOf_i2_supports_tools )             | No      | boolean | No         | -          | Supports Tools           |
| + [supports_image_input](#llm_unit_anyOf_i0_model_anyOf_i2_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input     |
| + [supports_audio_input](#llm_unit_anyOf_i0_model_anyOf_i2_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input     |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i2_implementation"></a>5.3.2.3.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** claude-3-sonnet-20240229

Specific value: `"claude-3-sonnet-20240229"`

###### <a name="llm_unit_anyOf_i0_model_anyOf_i2_human_name"></a>5.3.2.3.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i2_name"></a>5.3.2.3.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i2_input_context_limit"></a>5.3.2.3.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i2_output_context_limit"></a>5.3.2.3.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i2_supports_tools"></a>5.3.2.3.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i2_supports_image_input"></a>5.3.2.3.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i2_supports_audio_input"></a>5.3.2.3.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_anyOf_i0_model_anyOf_i3"></a>5.3.2.4. Property `gpt-3.5-turbo.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./gpt-3.5-turbo.json                                                 |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_anyOf_i0_model_anyOf_i3_implementation )             | No      | const   | No         | -          | gpt-3.5-turbo        |
| + [human_name](#llm_unit_anyOf_i0_model_anyOf_i3_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_anyOf_i0_model_anyOf_i3_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_anyOf_i0_model_anyOf_i3_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_anyOf_i0_model_anyOf_i3_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_anyOf_i0_model_anyOf_i3_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_anyOf_i0_model_anyOf_i3_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_anyOf_i0_model_anyOf_i3_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i3_implementation"></a>5.3.2.4.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** gpt-3.5-turbo

Specific value: `"gpt-3.5-turbo"`

###### <a name="llm_unit_anyOf_i0_model_anyOf_i3_human_name"></a>5.3.2.4.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i3_name"></a>5.3.2.4.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i3_input_context_limit"></a>5.3.2.4.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i3_output_context_limit"></a>5.3.2.4.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i3_supports_tools"></a>5.3.2.4.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i3_supports_image_input"></a>5.3.2.4.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i3_supports_audio_input"></a>5.3.2.4.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_anyOf_i0_model_anyOf_i4"></a>5.3.2.5. Property `gpt-4-turbo.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./gpt-4-turbo.json                                                   |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_anyOf_i0_model_anyOf_i4_implementation )             | No      | const   | No         | -          | gpt-4-turbo          |
| + [human_name](#llm_unit_anyOf_i0_model_anyOf_i4_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_anyOf_i0_model_anyOf_i4_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_anyOf_i0_model_anyOf_i4_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_anyOf_i0_model_anyOf_i4_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_anyOf_i0_model_anyOf_i4_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_anyOf_i0_model_anyOf_i4_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_anyOf_i0_model_anyOf_i4_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i4_implementation"></a>5.3.2.5.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** gpt-4-turbo

Specific value: `"gpt-4-turbo"`

###### <a name="llm_unit_anyOf_i0_model_anyOf_i4_human_name"></a>5.3.2.5.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i4_name"></a>5.3.2.5.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i4_input_context_limit"></a>5.3.2.5.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i4_output_context_limit"></a>5.3.2.5.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i4_supports_tools"></a>5.3.2.5.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i4_supports_image_input"></a>5.3.2.5.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i4_supports_audio_input"></a>5.3.2.5.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_anyOf_i0_model_anyOf_i5"></a>5.3.2.6. Property `gpt-4o.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./gpt-4o.json                                                        |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_anyOf_i0_model_anyOf_i5_implementation )             | No      | const   | No         | -          | gpt-4o               |
| + [human_name](#llm_unit_anyOf_i0_model_anyOf_i5_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_anyOf_i0_model_anyOf_i5_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_anyOf_i0_model_anyOf_i5_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_anyOf_i0_model_anyOf_i5_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_anyOf_i0_model_anyOf_i5_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_anyOf_i0_model_anyOf_i5_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_anyOf_i0_model_anyOf_i5_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i5_implementation"></a>5.3.2.6.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** gpt-4o

Specific value: `"gpt-4o"`

###### <a name="llm_unit_anyOf_i0_model_anyOf_i5_human_name"></a>5.3.2.6.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i5_name"></a>5.3.2.6.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i5_input_context_limit"></a>5.3.2.6.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i5_output_context_limit"></a>5.3.2.6.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i5_supports_tools"></a>5.3.2.6.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i5_supports_image_input"></a>5.3.2.6.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i5_supports_audio_input"></a>5.3.2.6.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_anyOf_i0_model_anyOf_i6"></a>5.3.2.7. Property `llama3-8b.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./llama3-8b.json                                                     |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_anyOf_i0_model_anyOf_i6_implementation )             | No      | const   | No         | -          | llama3-8b            |
| + [human_name](#llm_unit_anyOf_i0_model_anyOf_i6_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_anyOf_i0_model_anyOf_i6_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_anyOf_i0_model_anyOf_i6_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_anyOf_i0_model_anyOf_i6_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_anyOf_i0_model_anyOf_i6_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_anyOf_i0_model_anyOf_i6_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_anyOf_i0_model_anyOf_i6_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i6_implementation"></a>5.3.2.7.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** llama3-8b

Specific value: `"llama3-8b"`

###### <a name="llm_unit_anyOf_i0_model_anyOf_i6_human_name"></a>5.3.2.7.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i6_name"></a>5.3.2.7.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i6_input_context_limit"></a>5.3.2.7.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i6_output_context_limit"></a>5.3.2.7.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i6_supports_tools"></a>5.3.2.7.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i6_supports_image_input"></a>5.3.2.7.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i6_supports_audio_input"></a>5.3.2.7.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_anyOf_i0_model_anyOf_i7"></a>5.3.2.8. Property `mistral-large-latest.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./mistral-large-latest.json                                          |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_anyOf_i0_model_anyOf_i7_implementation )             | No      | const   | No         | -          | mistral-large-latest |
| + [human_name](#llm_unit_anyOf_i0_model_anyOf_i7_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_anyOf_i0_model_anyOf_i7_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_anyOf_i0_model_anyOf_i7_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_anyOf_i0_model_anyOf_i7_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_anyOf_i0_model_anyOf_i7_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_anyOf_i0_model_anyOf_i7_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_anyOf_i0_model_anyOf_i7_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i7_implementation"></a>5.3.2.8.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** mistral-large-latest

Specific value: `"mistral-large-latest"`

###### <a name="llm_unit_anyOf_i0_model_anyOf_i7_human_name"></a>5.3.2.8.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i7_name"></a>5.3.2.8.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i7_input_context_limit"></a>5.3.2.8.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i7_output_context_limit"></a>5.3.2.8.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i7_supports_tools"></a>5.3.2.8.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i7_supports_image_input"></a>5.3.2.8.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i7_supports_audio_input"></a>5.3.2.8.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_anyOf_i0_model_anyOf_i8"></a>5.3.2.9. Property `mistral-medium-latest.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./mistral-medium-latest.json                                         |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description     |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | --------------------- |
| - [implementation](#llm_unit_anyOf_i0_model_anyOf_i8_implementation )             | No      | const   | No         | -          | mistral-medium-latest |
| + [human_name](#llm_unit_anyOf_i0_model_anyOf_i8_human_name )                     | No      | string  | No         | -          | Human Name            |
| + [name](#llm_unit_anyOf_i0_model_anyOf_i8_name )                                 | No      | string  | No         | -          | Name                  |
| + [input_context_limit](#llm_unit_anyOf_i0_model_anyOf_i8_input_context_limit )   | No      | integer | No         | -          | Input Context Limit   |
| + [output_context_limit](#llm_unit_anyOf_i0_model_anyOf_i8_output_context_limit ) | No      | integer | No         | -          | Output Context Limit  |
| + [supports_tools](#llm_unit_anyOf_i0_model_anyOf_i8_supports_tools )             | No      | boolean | No         | -          | Supports Tools        |
| + [supports_image_input](#llm_unit_anyOf_i0_model_anyOf_i8_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input  |
| + [supports_audio_input](#llm_unit_anyOf_i0_model_anyOf_i8_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input  |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i8_implementation"></a>5.3.2.9.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** mistral-medium-latest

Specific value: `"mistral-medium-latest"`

###### <a name="llm_unit_anyOf_i0_model_anyOf_i8_human_name"></a>5.3.2.9.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i8_name"></a>5.3.2.9.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i8_input_context_limit"></a>5.3.2.9.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i8_output_context_limit"></a>5.3.2.9.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i8_supports_tools"></a>5.3.2.9.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i8_supports_image_input"></a>5.3.2.9.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i8_supports_audio_input"></a>5.3.2.9.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_anyOf_i0_model_anyOf_i9"></a>5.3.2.10. Property `mistral-small-latest.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./mistral-small-latest.json                                          |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_anyOf_i0_model_anyOf_i9_implementation )             | No      | const   | No         | -          | mistral-small-latest |
| + [human_name](#llm_unit_anyOf_i0_model_anyOf_i9_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_anyOf_i0_model_anyOf_i9_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_anyOf_i0_model_anyOf_i9_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_anyOf_i0_model_anyOf_i9_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_anyOf_i0_model_anyOf_i9_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_anyOf_i0_model_anyOf_i9_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_anyOf_i0_model_anyOf_i9_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i9_implementation"></a>5.3.2.10.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** mistral-small-latest

Specific value: `"mistral-small-latest"`

###### <a name="llm_unit_anyOf_i0_model_anyOf_i9_human_name"></a>5.3.2.10.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i9_name"></a>5.3.2.10.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i9_input_context_limit"></a>5.3.2.10.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i9_output_context_limit"></a>5.3.2.10.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i9_supports_tools"></a>5.3.2.10.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i9_supports_image_input"></a>5.3.2.10.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i9_supports_audio_input"></a>5.3.2.10.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

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

#### <a name="llm_unit_anyOf_i2_client_options"></a>5.3.6. Property `client_options`

**Title:** Client Options

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

### <a name="llm_unit_anyOf_i3"></a>5.4. Property `OpenAIGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./OpenAIGPT.json                                                     |

| Property                                                       | Pattern | Type        | Deprecated | Definition                                       | Title/Description                              |
| -------------------------------------------------------------- | ------- | ----------- | ---------- | ------------------------------------------------ | ---------------------------------------------- |
| - [implementation](#llm_unit_anyOf_i3_implementation )         | No      | const       | No         | -                                                | OpenAIGPT                                      |
| - [model](#llm_unit_anyOf_i3_model )                           | No      | object      | No         | In [LLMModel](/docs/components/llmmodel/overview)                | Overview of LLMModel components                |
| - [temperature](#llm_unit_anyOf_i3_temperature )               | No      | number      | No         | -                                                | Temperature                                    |
| - [force_json](#llm_unit_anyOf_i3_force_json )                 | No      | boolean     | No         | -                                                | Force Json                                     |
| - [max_tokens](#llm_unit_anyOf_i3_max_tokens )                 | No      | Combination | No         | -                                                | Max Tokens                                     |
| - [connection_handler](#llm_unit_anyOf_i3_connection_handler ) | No      | object      | No         | In [OpenAIConnectionHandler](/docs/components/openaiconnectionhandler/overview) | Overview of OpenAIConnectionHandler components |

#### <a name="llm_unit_anyOf_i3_implementation"></a>5.4.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OpenAIGPT

Specific value: `"OpenAIGPT"`

#### <a name="llm_unit_anyOf_i3_model"></a>5.4.2. Property `model`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{"implementation": "LLMModel"}`                                          |
| **Defined in**            | [LLMModel](/docs/components/llmmodel/overview)                                            |

**Description:** Overview of LLMModel components

| Any of(Option)                                                     |
| ------------------------------------------------------------------ |
| [claude-3-haiku-20240307.json](#llm_unit_anyOf_i0_model_anyOf_i0)  |
| [claude-3-opus-20240229.json](#llm_unit_anyOf_i0_model_anyOf_i1)   |
| [claude-3-sonnet-20240229.json](#llm_unit_anyOf_i0_model_anyOf_i2) |
| [gpt-3.5-turbo.json](#llm_unit_anyOf_i0_model_anyOf_i3)            |
| [gpt-4-turbo.json](#llm_unit_anyOf_i0_model_anyOf_i4)              |
| [gpt-4o.json](#llm_unit_anyOf_i0_model_anyOf_i5)                   |
| [llama3-8b.json](#llm_unit_anyOf_i0_model_anyOf_i6)                |
| [mistral-large-latest.json](#llm_unit_anyOf_i0_model_anyOf_i7)     |
| [mistral-medium-latest.json](#llm_unit_anyOf_i0_model_anyOf_i8)    |
| [mistral-small-latest.json](#llm_unit_anyOf_i0_model_anyOf_i9)     |

##### <a name="llm_unit_anyOf_i0_model_anyOf_i0"></a>5.4.2.1. Property `claude-3-haiku-20240307.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./claude-3-haiku-20240307.json                                       |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description       |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | ----------------------- |
| - [implementation](#llm_unit_anyOf_i0_model_anyOf_i0_implementation )             | No      | const   | No         | -          | claude-3-haiku-20240307 |
| + [human_name](#llm_unit_anyOf_i0_model_anyOf_i0_human_name )                     | No      | string  | No         | -          | Human Name              |
| + [name](#llm_unit_anyOf_i0_model_anyOf_i0_name )                                 | No      | string  | No         | -          | Name                    |
| + [input_context_limit](#llm_unit_anyOf_i0_model_anyOf_i0_input_context_limit )   | No      | integer | No         | -          | Input Context Limit     |
| + [output_context_limit](#llm_unit_anyOf_i0_model_anyOf_i0_output_context_limit ) | No      | integer | No         | -          | Output Context Limit    |
| + [supports_tools](#llm_unit_anyOf_i0_model_anyOf_i0_supports_tools )             | No      | boolean | No         | -          | Supports Tools          |
| + [supports_image_input](#llm_unit_anyOf_i0_model_anyOf_i0_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input    |
| + [supports_audio_input](#llm_unit_anyOf_i0_model_anyOf_i0_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input    |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i0_implementation"></a>5.4.2.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** claude-3-haiku-20240307

Specific value: `"claude-3-haiku-20240307"`

###### <a name="llm_unit_anyOf_i0_model_anyOf_i0_human_name"></a>5.4.2.1.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i0_name"></a>5.4.2.1.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i0_input_context_limit"></a>5.4.2.1.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i0_output_context_limit"></a>5.4.2.1.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i0_supports_tools"></a>5.4.2.1.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i0_supports_image_input"></a>5.4.2.1.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i0_supports_audio_input"></a>5.4.2.1.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_anyOf_i0_model_anyOf_i1"></a>5.4.2.2. Property `claude-3-opus-20240229.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./claude-3-opus-20240229.json                                        |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description      |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | ---------------------- |
| - [implementation](#llm_unit_anyOf_i0_model_anyOf_i1_implementation )             | No      | const   | No         | -          | claude-3-opus-20240229 |
| + [human_name](#llm_unit_anyOf_i0_model_anyOf_i1_human_name )                     | No      | string  | No         | -          | Human Name             |
| + [name](#llm_unit_anyOf_i0_model_anyOf_i1_name )                                 | No      | string  | No         | -          | Name                   |
| + [input_context_limit](#llm_unit_anyOf_i0_model_anyOf_i1_input_context_limit )   | No      | integer | No         | -          | Input Context Limit    |
| + [output_context_limit](#llm_unit_anyOf_i0_model_anyOf_i1_output_context_limit ) | No      | integer | No         | -          | Output Context Limit   |
| + [supports_tools](#llm_unit_anyOf_i0_model_anyOf_i1_supports_tools )             | No      | boolean | No         | -          | Supports Tools         |
| + [supports_image_input](#llm_unit_anyOf_i0_model_anyOf_i1_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input   |
| + [supports_audio_input](#llm_unit_anyOf_i0_model_anyOf_i1_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input   |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i1_implementation"></a>5.4.2.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** claude-3-opus-20240229

Specific value: `"claude-3-opus-20240229"`

###### <a name="llm_unit_anyOf_i0_model_anyOf_i1_human_name"></a>5.4.2.2.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i1_name"></a>5.4.2.2.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i1_input_context_limit"></a>5.4.2.2.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i1_output_context_limit"></a>5.4.2.2.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i1_supports_tools"></a>5.4.2.2.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i1_supports_image_input"></a>5.4.2.2.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i1_supports_audio_input"></a>5.4.2.2.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_anyOf_i0_model_anyOf_i2"></a>5.4.2.3. Property `claude-3-sonnet-20240229.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./claude-3-sonnet-20240229.json                                      |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description        |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | ------------------------ |
| - [implementation](#llm_unit_anyOf_i0_model_anyOf_i2_implementation )             | No      | const   | No         | -          | claude-3-sonnet-20240229 |
| + [human_name](#llm_unit_anyOf_i0_model_anyOf_i2_human_name )                     | No      | string  | No         | -          | Human Name               |
| + [name](#llm_unit_anyOf_i0_model_anyOf_i2_name )                                 | No      | string  | No         | -          | Name                     |
| + [input_context_limit](#llm_unit_anyOf_i0_model_anyOf_i2_input_context_limit )   | No      | integer | No         | -          | Input Context Limit      |
| + [output_context_limit](#llm_unit_anyOf_i0_model_anyOf_i2_output_context_limit ) | No      | integer | No         | -          | Output Context Limit     |
| + [supports_tools](#llm_unit_anyOf_i0_model_anyOf_i2_supports_tools )             | No      | boolean | No         | -          | Supports Tools           |
| + [supports_image_input](#llm_unit_anyOf_i0_model_anyOf_i2_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input     |
| + [supports_audio_input](#llm_unit_anyOf_i0_model_anyOf_i2_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input     |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i2_implementation"></a>5.4.2.3.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** claude-3-sonnet-20240229

Specific value: `"claude-3-sonnet-20240229"`

###### <a name="llm_unit_anyOf_i0_model_anyOf_i2_human_name"></a>5.4.2.3.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i2_name"></a>5.4.2.3.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i2_input_context_limit"></a>5.4.2.3.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i2_output_context_limit"></a>5.4.2.3.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i2_supports_tools"></a>5.4.2.3.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i2_supports_image_input"></a>5.4.2.3.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i2_supports_audio_input"></a>5.4.2.3.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_anyOf_i0_model_anyOf_i3"></a>5.4.2.4. Property `gpt-3.5-turbo.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./gpt-3.5-turbo.json                                                 |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_anyOf_i0_model_anyOf_i3_implementation )             | No      | const   | No         | -          | gpt-3.5-turbo        |
| + [human_name](#llm_unit_anyOf_i0_model_anyOf_i3_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_anyOf_i0_model_anyOf_i3_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_anyOf_i0_model_anyOf_i3_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_anyOf_i0_model_anyOf_i3_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_anyOf_i0_model_anyOf_i3_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_anyOf_i0_model_anyOf_i3_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_anyOf_i0_model_anyOf_i3_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i3_implementation"></a>5.4.2.4.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** gpt-3.5-turbo

Specific value: `"gpt-3.5-turbo"`

###### <a name="llm_unit_anyOf_i0_model_anyOf_i3_human_name"></a>5.4.2.4.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i3_name"></a>5.4.2.4.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i3_input_context_limit"></a>5.4.2.4.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i3_output_context_limit"></a>5.4.2.4.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i3_supports_tools"></a>5.4.2.4.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i3_supports_image_input"></a>5.4.2.4.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i3_supports_audio_input"></a>5.4.2.4.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_anyOf_i0_model_anyOf_i4"></a>5.4.2.5. Property `gpt-4-turbo.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./gpt-4-turbo.json                                                   |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_anyOf_i0_model_anyOf_i4_implementation )             | No      | const   | No         | -          | gpt-4-turbo          |
| + [human_name](#llm_unit_anyOf_i0_model_anyOf_i4_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_anyOf_i0_model_anyOf_i4_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_anyOf_i0_model_anyOf_i4_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_anyOf_i0_model_anyOf_i4_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_anyOf_i0_model_anyOf_i4_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_anyOf_i0_model_anyOf_i4_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_anyOf_i0_model_anyOf_i4_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i4_implementation"></a>5.4.2.5.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** gpt-4-turbo

Specific value: `"gpt-4-turbo"`

###### <a name="llm_unit_anyOf_i0_model_anyOf_i4_human_name"></a>5.4.2.5.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i4_name"></a>5.4.2.5.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i4_input_context_limit"></a>5.4.2.5.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i4_output_context_limit"></a>5.4.2.5.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i4_supports_tools"></a>5.4.2.5.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i4_supports_image_input"></a>5.4.2.5.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i4_supports_audio_input"></a>5.4.2.5.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_anyOf_i0_model_anyOf_i5"></a>5.4.2.6. Property `gpt-4o.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./gpt-4o.json                                                        |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_anyOf_i0_model_anyOf_i5_implementation )             | No      | const   | No         | -          | gpt-4o               |
| + [human_name](#llm_unit_anyOf_i0_model_anyOf_i5_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_anyOf_i0_model_anyOf_i5_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_anyOf_i0_model_anyOf_i5_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_anyOf_i0_model_anyOf_i5_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_anyOf_i0_model_anyOf_i5_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_anyOf_i0_model_anyOf_i5_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_anyOf_i0_model_anyOf_i5_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i5_implementation"></a>5.4.2.6.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** gpt-4o

Specific value: `"gpt-4o"`

###### <a name="llm_unit_anyOf_i0_model_anyOf_i5_human_name"></a>5.4.2.6.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i5_name"></a>5.4.2.6.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i5_input_context_limit"></a>5.4.2.6.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i5_output_context_limit"></a>5.4.2.6.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i5_supports_tools"></a>5.4.2.6.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i5_supports_image_input"></a>5.4.2.6.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i5_supports_audio_input"></a>5.4.2.6.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_anyOf_i0_model_anyOf_i6"></a>5.4.2.7. Property `llama3-8b.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./llama3-8b.json                                                     |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_anyOf_i0_model_anyOf_i6_implementation )             | No      | const   | No         | -          | llama3-8b            |
| + [human_name](#llm_unit_anyOf_i0_model_anyOf_i6_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_anyOf_i0_model_anyOf_i6_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_anyOf_i0_model_anyOf_i6_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_anyOf_i0_model_anyOf_i6_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_anyOf_i0_model_anyOf_i6_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_anyOf_i0_model_anyOf_i6_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_anyOf_i0_model_anyOf_i6_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i6_implementation"></a>5.4.2.7.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** llama3-8b

Specific value: `"llama3-8b"`

###### <a name="llm_unit_anyOf_i0_model_anyOf_i6_human_name"></a>5.4.2.7.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i6_name"></a>5.4.2.7.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i6_input_context_limit"></a>5.4.2.7.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i6_output_context_limit"></a>5.4.2.7.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i6_supports_tools"></a>5.4.2.7.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i6_supports_image_input"></a>5.4.2.7.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i6_supports_audio_input"></a>5.4.2.7.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_anyOf_i0_model_anyOf_i7"></a>5.4.2.8. Property `mistral-large-latest.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./mistral-large-latest.json                                          |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_anyOf_i0_model_anyOf_i7_implementation )             | No      | const   | No         | -          | mistral-large-latest |
| + [human_name](#llm_unit_anyOf_i0_model_anyOf_i7_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_anyOf_i0_model_anyOf_i7_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_anyOf_i0_model_anyOf_i7_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_anyOf_i0_model_anyOf_i7_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_anyOf_i0_model_anyOf_i7_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_anyOf_i0_model_anyOf_i7_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_anyOf_i0_model_anyOf_i7_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i7_implementation"></a>5.4.2.8.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** mistral-large-latest

Specific value: `"mistral-large-latest"`

###### <a name="llm_unit_anyOf_i0_model_anyOf_i7_human_name"></a>5.4.2.8.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i7_name"></a>5.4.2.8.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i7_input_context_limit"></a>5.4.2.8.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i7_output_context_limit"></a>5.4.2.8.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i7_supports_tools"></a>5.4.2.8.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i7_supports_image_input"></a>5.4.2.8.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i7_supports_audio_input"></a>5.4.2.8.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_anyOf_i0_model_anyOf_i8"></a>5.4.2.9. Property `mistral-medium-latest.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./mistral-medium-latest.json                                         |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description     |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | --------------------- |
| - [implementation](#llm_unit_anyOf_i0_model_anyOf_i8_implementation )             | No      | const   | No         | -          | mistral-medium-latest |
| + [human_name](#llm_unit_anyOf_i0_model_anyOf_i8_human_name )                     | No      | string  | No         | -          | Human Name            |
| + [name](#llm_unit_anyOf_i0_model_anyOf_i8_name )                                 | No      | string  | No         | -          | Name                  |
| + [input_context_limit](#llm_unit_anyOf_i0_model_anyOf_i8_input_context_limit )   | No      | integer | No         | -          | Input Context Limit   |
| + [output_context_limit](#llm_unit_anyOf_i0_model_anyOf_i8_output_context_limit ) | No      | integer | No         | -          | Output Context Limit  |
| + [supports_tools](#llm_unit_anyOf_i0_model_anyOf_i8_supports_tools )             | No      | boolean | No         | -          | Supports Tools        |
| + [supports_image_input](#llm_unit_anyOf_i0_model_anyOf_i8_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input  |
| + [supports_audio_input](#llm_unit_anyOf_i0_model_anyOf_i8_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input  |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i8_implementation"></a>5.4.2.9.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** mistral-medium-latest

Specific value: `"mistral-medium-latest"`

###### <a name="llm_unit_anyOf_i0_model_anyOf_i8_human_name"></a>5.4.2.9.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i8_name"></a>5.4.2.9.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i8_input_context_limit"></a>5.4.2.9.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i8_output_context_limit"></a>5.4.2.9.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i8_supports_tools"></a>5.4.2.9.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i8_supports_image_input"></a>5.4.2.9.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i8_supports_audio_input"></a>5.4.2.9.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

##### <a name="llm_unit_anyOf_i0_model_anyOf_i9"></a>5.4.2.10. Property `mistral-small-latest.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./mistral-small-latest.json                                          |

| Property                                                                          | Pattern | Type    | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#llm_unit_anyOf_i0_model_anyOf_i9_implementation )             | No      | const   | No         | -          | mistral-small-latest |
| + [human_name](#llm_unit_anyOf_i0_model_anyOf_i9_human_name )                     | No      | string  | No         | -          | Human Name           |
| + [name](#llm_unit_anyOf_i0_model_anyOf_i9_name )                                 | No      | string  | No         | -          | Name                 |
| + [input_context_limit](#llm_unit_anyOf_i0_model_anyOf_i9_input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| + [output_context_limit](#llm_unit_anyOf_i0_model_anyOf_i9_output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| + [supports_tools](#llm_unit_anyOf_i0_model_anyOf_i9_supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| + [supports_image_input](#llm_unit_anyOf_i0_model_anyOf_i9_supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| + [supports_audio_input](#llm_unit_anyOf_i0_model_anyOf_i9_supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i9_implementation"></a>5.4.2.10.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** mistral-small-latest

Specific value: `"mistral-small-latest"`

###### <a name="llm_unit_anyOf_i0_model_anyOf_i9_human_name"></a>5.4.2.10.2. Property `human_name`

**Title:** Human Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i9_name"></a>5.4.2.10.3. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i9_input_context_limit"></a>5.4.2.10.4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i9_output_context_limit"></a>5.4.2.10.5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i9_supports_tools"></a>5.4.2.10.6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i9_supports_image_input"></a>5.4.2.10.7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

###### <a name="llm_unit_anyOf_i0_model_anyOf_i9_supports_audio_input"></a>5.4.2.10.8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

#### <a name="llm_unit_anyOf_i3_temperature"></a>5.4.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

#### <a name="llm_unit_anyOf_i3_force_json"></a>5.4.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

#### <a name="llm_unit_anyOf_i3_max_tokens"></a>5.4.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                   |
| ------------------------------------------------ |
| [item 0](#llm_unit_anyOf_i3_max_tokens_anyOf_i0) |
| [item 1](#llm_unit_anyOf_i3_max_tokens_anyOf_i1) |

##### <a name="llm_unit_anyOf_i3_max_tokens_anyOf_i0"></a>5.4.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

##### <a name="llm_unit_anyOf_i3_max_tokens_anyOf_i1"></a>5.4.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="llm_unit_anyOf_i3_connection_handler"></a>5.4.6. Property `connection_handler`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{"implementation": "OpenAIConnectionHandler"}`                           |
| **Defined in**            | [OpenAIConnectionHandler](/docs/components/openaiconnectionhandler/overview)                             |

**Description:** Overview of OpenAIConnectionHandler components

| Any of(Option)                                                                      |
| ----------------------------------------------------------------------------------- |
| [AzureOpenAIConnectionHandler.json](#llm_unit_anyOf_i3_connection_handler_anyOf_i0) |

##### <a name="llm_unit_anyOf_i3_connection_handler_anyOf_i0"></a>5.4.6.1. Property `AzureOpenAIConnectionHandler.json`

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

| Property                                                                                             | Pattern | Type            | Deprecated | Definition | Title/Description            |
| ---------------------------------------------------------------------------------------------------- | ------- | --------------- | ---------- | ---------- | ---------------------------- |
| - [implementation](#llm_unit_anyOf_i3_connection_handler_anyOf_i0_implementation )                   | No      | const           | No         | -          | AzureOpenAIConnectionHandler |
| - [azure_ad_token_provider](#llm_unit_anyOf_i3_connection_handler_anyOf_i0_azure_ad_token_provider ) | No      | Combination     | No         | -          | -                            |
| - [token_provider_scopes](#llm_unit_anyOf_i3_connection_handler_anyOf_i0_token_provider_scopes )     | No      | array of string | No         | -          | Token Provider Scopes        |
| - [api_version](#llm_unit_anyOf_i3_connection_handler_anyOf_i0_api_version )                         | No      | string          | No         | -          | Api Version                  |
| - [](#llm_unit_anyOf_i3_connection_handler_anyOf_i0_additionalProperties )                           | No      | object          | No         | -          | -                            |

###### <a name="llm_unit_anyOf_i3_connection_handler_anyOf_i0_implementation"></a>5.4.6.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AzureOpenAIConnectionHandler

Specific value: `"AzureOpenAIConnectionHandler"`

###### <a name="llm_unit_anyOf_i3_connection_handler_anyOf_i0_azure_ad_token_provider"></a>5.4.6.1.2. Property `azure_ad_token_provider`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

| Any of(Option)                                                                               |
| -------------------------------------------------------------------------------------------- |
| [Reference](#llm_unit_anyOf_i3_connection_handler_anyOf_i0_azure_ad_token_provider_anyOf_i0) |
| [item 1](#llm_unit_anyOf_i3_connection_handler_anyOf_i0_azure_ad_token_provider_anyOf_i1)    |

###### <a name="llm_unit_anyOf_i3_connection_handler_anyOf_i0_azure_ad_token_provider_anyOf_i0"></a>5.4.6.1.2.1. Property `Reference`

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

| Property                                                                                                            | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#llm_unit_anyOf_i3_connection_handler_anyOf_i0_azure_ad_token_provider_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#llm_unit_anyOf_i3_connection_handler_anyOf_i0_azure_ad_token_provider_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="llm_unit_anyOf_i3_connection_handler_anyOf_i0_azure_ad_token_provider_anyOf_i0_implementation"></a>5.4.6.1.2.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="llm_unit_anyOf_i3_connection_handler_anyOf_i0_azure_ad_token_provider_anyOf_i1"></a>5.4.6.1.2.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="llm_unit_anyOf_i3_connection_handler_anyOf_i0_token_provider_scopes"></a>5.4.6.1.3. Property `token_provider_scopes`

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

| Each item of this array must be                                                                           | Description |
| --------------------------------------------------------------------------------------------------------- | ----------- |
| [token_provider_scopes items](#llm_unit_anyOf_i3_connection_handler_anyOf_i0_token_provider_scopes_items) | -           |

###### <a name="autogenerated_heading_2"></a>5.4.6.1.3.1. token_provider_scopes items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

###### <a name="llm_unit_anyOf_i3_connection_handler_anyOf_i0_api_version"></a>5.4.6.1.4. Property `api_version`

**Title:** Api Version

|              |                |
| ------------ | -------------- |
| **Type**     | `string`       |
| **Required** | No             |
| **Default**  | `"2024-02-01"` |

### <a name="llm_unit_anyOf_i4"></a>5.5. Property `ToolCallLLMWrapper.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./ToolCallLLMWrapper.json                                            |

| Property                                                         | Pattern | Type        | Deprecated | Definition                     | Title/Description              |
| ---------------------------------------------------------------- | ------- | ----------- | ---------- | ------------------------------ | ------------------------------ |
| - [implementation](#llm_unit_anyOf_i4_implementation )           | No      | const       | No         | -                              | ToolCallLLMWrapper             |
| - [tool_message_prompt](#llm_unit_anyOf_i4_tool_message_prompt ) | No      | string      | No         | -                              | Tool Message Prompt            |
| - [llm_unit](#llm_unit_anyOf_i4_llm_unit )                       | No      | object      | No         | Same as [llm_unit](#llm_unit ) | Overview of LLMUnit components |
| - [model](#llm_unit_anyOf_i4_model )                             | No      | Combination | No         | -                              | -                              |

#### <a name="llm_unit_anyOf_i4_implementation"></a>5.5.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ToolCallLLMWrapper

Specific value: `"ToolCallLLMWrapper"`

#### <a name="llm_unit_anyOf_i4_tool_message_prompt"></a>5.5.2. Property `tool_message_prompt`

**Title:** Tool Message Prompt

|              |                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Required** | No                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Default**  | `"You must follow these instructions:\nYou can select zero or more of the above tools based on the user query\nIf there are multiple tools required, make sure a list of tools are returned in a JSON array.\nIf there is no tool that match the user request or you have already answered the question, you will respond with empty json array for the tools.\nYou can also add any additional notes or explanations in the notes field."` |

#### <a name="llm_unit_anyOf_i4_llm_unit"></a>5.5.3. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{"implementation": "OpenAIGPT"}`                                         |
| **Same definition as**    | [llm_unit](#llm_unit)                                                     |

**Description:** Overview of LLMUnit components

#### <a name="llm_unit_anyOf_i4_model"></a>5.5.4. Property `model`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                     |
| -------------------------------------------------- |
| [overview.json](#llm_unit_anyOf_i4_model_anyOf_i0) |
| [item 1](#llm_unit_anyOf_i4_model_anyOf_i1)        |

##### <a name="llm_unit_anyOf_i4_model_anyOf_i0"></a>5.5.4.1. Property `overview.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Same definition as**    | [model](#llm_unit_anyOf_i0_model)                                         |

**Description:** Overview of LLMModel components

##### <a name="llm_unit_anyOf_i4_model_anyOf_i1"></a>5.5.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

## <a name="logic_units"></a>6. Property `logic_units`

**Title:** Logic Units

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

| Each item of this array must be     | Description                      |
| ----------------------------------- | -------------------------------- |
| [overview.json](#logic_units_items) | Overview of LogicUnit components |

### <a name="autogenerated_heading_3"></a>6.1. overview.json

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | [LogicUnit](/docs/components/logicunit/overview)                                           |

**Description:** Overview of LogicUnit components

| Any of(Option)                                      |
| --------------------------------------------------- |
| [ApiLogicUnit.json](#logic_units_items_anyOf_i0)    |
| [AudioUnit.json](#logic_units_items_anyOf_i1)       |
| [Browser.json](#logic_units_items_anyOf_i2)         |
| [OpenAIImageUnit.json](#logic_units_items_anyOf_i3) |
| [OpenAiSpeech.json](#logic_units_items_anyOf_i4)    |
| [Search.json](#logic_units_items_anyOf_i5)          |
| [WebSearch.json](#logic_units_items_anyOf_i6)       |

#### <a name="logic_units_items_anyOf_i0"></a>6.1.1. Property `ApiLogicUnit.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./ApiLogicUnit.json                                                  |

| Property                                                                    | Pattern | Type   | Deprecated | Definition | Title/Description    |
| --------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | -------------------- |
| - [implementation](#logic_units_items_anyOf_i0_implementation )             | No      | const  | No         | -          | ApiLogicUnit         |
| + [title](#logic_units_items_anyOf_i0_title )                               | No      | string | No         | -          | Title                |
| + [root_call_url](#logic_units_items_anyOf_i0_root_call_url )               | No      | string | No         | -          | Root Call Url        |
| + [open_api_location](#logic_units_items_anyOf_i0_open_api_location )       | No      | string | No         | -          | Open Api Location    |
| + [operations_to_expose](#logic_units_items_anyOf_i0_operations_to_expose ) | No      | array  | No         | -          | Operations To Expose |
| - [extra_header_params](#logic_units_items_anyOf_i0_extra_header_params )   | No      | object | No         | -          | Extra Header Params  |
| - [extra_query_params](#logic_units_items_anyOf_i0_extra_query_params )     | No      | object | No         | -          | Extra Query Params   |

##### <a name="logic_units_items_anyOf_i0_implementation"></a>6.1.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ApiLogicUnit

Specific value: `"ApiLogicUnit"`

##### <a name="logic_units_items_anyOf_i0_title"></a>6.1.1.2. Property `title`

**Title:** Title

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Title of the API

##### <a name="logic_units_items_anyOf_i0_root_call_url"></a>6.1.1.3. Property `root_call_url`

**Title:** Root Call Url

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Root URL of the API to call

##### <a name="logic_units_items_anyOf_i0_open_api_location"></a>6.1.1.4. Property `open_api_location`

**Title:** Open Api Location

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Location of the OpenAPI schema

##### <a name="logic_units_items_anyOf_i0_operations_to_expose"></a>6.1.1.5. Property `operations_to_expose`

**Title:** Operations To Expose

|              |         |
| ------------ | ------- |
| **Type**     | `array` |
| **Required** | Yes     |

**Description:** Operations to expose

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                                     | Description |
| ------------------------------------------------------------------- | ----------- |
| [Operation](#logic_units_items_anyOf_i0_operations_to_expose_items) | -           |

###### <a name="autogenerated_heading_4"></a>6.1.1.5.1. Operation

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | #/$defs/Operation                                                         |

| Property                                                                                   | Pattern | Type        | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------------------------ | ------- | ----------- | ---------- | ---------- | ----------------- |
| + [name](#logic_units_items_anyOf_i0_operations_to_expose_items_name )                     | No      | string      | No         | -          | Name              |
| - [description](#logic_units_items_anyOf_i0_operations_to_expose_items_description )       | No      | Combination | No         | -          | Description       |
| + [path](#logic_units_items_anyOf_i0_operations_to_expose_items_path )                     | No      | string      | No         | -          | Path              |
| + [method](#logic_units_items_anyOf_i0_operations_to_expose_items_method )                 | No      | string      | No         | -          | Method            |
| - [result_filters](#logic_units_items_anyOf_i0_operations_to_expose_items_result_filters ) | No      | Combination | No         | -          | Result Filters    |

###### <a name="logic_units_items_anyOf_i0_operations_to_expose_items_name"></a>6.1.1.5.1.1. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Name of the operation

###### <a name="logic_units_items_anyOf_i0_operations_to_expose_items_description"></a>6.1.1.5.1.2. Property `description`

**Title:** Description

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

**Description:** Description of the operation

| Any of(Option)                                                                        |
| ------------------------------------------------------------------------------------- |
| [item 0](#logic_units_items_anyOf_i0_operations_to_expose_items_description_anyOf_i0) |
| [item 1](#logic_units_items_anyOf_i0_operations_to_expose_items_description_anyOf_i1) |

###### <a name="logic_units_items_anyOf_i0_operations_to_expose_items_description_anyOf_i0"></a>6.1.1.5.1.2.1. Property `item 0`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

###### <a name="logic_units_items_anyOf_i0_operations_to_expose_items_description_anyOf_i1"></a>6.1.1.5.1.2.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="logic_units_items_anyOf_i0_operations_to_expose_items_path"></a>6.1.1.5.1.3. Property `path`

**Title:** Path

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Path of the operation. Must match exactly including path parameters

###### <a name="logic_units_items_anyOf_i0_operations_to_expose_items_method"></a>6.1.1.5.1.4. Property `method`

**Title:** Method

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** HTTP method of the operation.  get and post are supported

###### <a name="logic_units_items_anyOf_i0_operations_to_expose_items_result_filters"></a>6.1.1.5.1.5. Property `result_filters`

**Title:** Result Filters

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

**Description:** Filters to apply to the result of the operation per json ref spec

| Any of(Option)                                                                           |
| ---------------------------------------------------------------------------------------- |
| [item 0](#logic_units_items_anyOf_i0_operations_to_expose_items_result_filters_anyOf_i0) |
| [item 1](#logic_units_items_anyOf_i0_operations_to_expose_items_result_filters_anyOf_i1) |

###### <a name="logic_units_items_anyOf_i0_operations_to_expose_items_result_filters_anyOf_i0"></a>6.1.1.5.1.5.1. Property `item 0`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of string` |
| **Required** | No                |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                                                                      | Description |
| ---------------------------------------------------------------------------------------------------- | ----------- |
| [item 0 items](#logic_units_items_anyOf_i0_operations_to_expose_items_result_filters_anyOf_i0_items) | -           |

###### <a name="autogenerated_heading_5"></a>6.1.1.5.1.5.1.1. item 0 items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

###### <a name="logic_units_items_anyOf_i0_operations_to_expose_items_result_filters_anyOf_i1"></a>6.1.1.5.1.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

##### <a name="logic_units_items_anyOf_i0_extra_header_params"></a>6.1.1.6. Property `extra_header_params`

**Title:** Extra Header Params

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

**Description:** Extra header parameters to add to every call. This can be a jinja template where the variables in the template are ENV variables (matching case)

##### <a name="logic_units_items_anyOf_i0_extra_query_params"></a>6.1.1.7. Property `extra_query_params`

**Title:** Extra Query Params

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

**Description:** Extra query parameters to add to every call. This can be a jinja template where the variables in the template are ENV variables (matching case)

#### <a name="logic_units_items_anyOf_i1"></a>6.1.2. Property `AudioUnit.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./AudioUnit.json                                                     |

| Property                                                                                | Pattern | Type             | Deprecated | Definition | Title/Description          |
| --------------------------------------------------------------------------------------- | ------- | ---------------- | ---------- | ---------- | -------------------------- |
| - [implementation](#logic_units_items_anyOf_i1_implementation )                         | No      | const            | No         | -          | AudioUnit                  |
| - [text_to_speech_model](#logic_units_items_anyOf_i1_text_to_speech_model )             | No      | enum (of string) | No         | -          | Text To Speech Model       |
| - [text_to_speech_voice](#logic_units_items_anyOf_i1_text_to_speech_voice )             | No      | enum (of string) | No         | -          | Text To Speech Voice       |
| - [speech_to_text_model](#logic_units_items_anyOf_i1_speech_to_text_model )             | No      | const            | No         | -          | Speech To Text Model       |
| - [speech_to_text_temperature](#logic_units_items_anyOf_i1_speech_to_text_temperature ) | No      | number           | No         | -          | Speech To Text Temperature |

##### <a name="logic_units_items_anyOf_i1_implementation"></a>6.1.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AudioUnit

Specific value: `"AudioUnit"`

##### <a name="logic_units_items_anyOf_i1_text_to_speech_model"></a>6.1.2.2. Property `text_to_speech_model`

**Title:** Text To Speech Model

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | No                 |
| **Default**  | `"tts-1-hd"`       |

**Description:** The model to use for text to speech.

Must be one of:
* "tts-1"
* "tts-1-hd"

##### <a name="logic_units_items_anyOf_i1_text_to_speech_voice"></a>6.1.2.3. Property `text_to_speech_voice`

**Title:** Text To Speech Voice

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | No                 |
| **Default**  | `"alloy"`          |

**Description:** The voice to use for text to speech.

Must be one of:
* "alloy"
* "echo"
* "fable"
* "onyx"
* "nova"
* "shimmer"

##### <a name="logic_units_items_anyOf_i1_speech_to_text_model"></a>6.1.2.4. Property `speech_to_text_model`

**Title:** Speech To Text Model

|              |               |
| ------------ | ------------- |
| **Type**     | `const`       |
| **Required** | No            |
| **Default**  | `"whisper-1"` |

**Description:** The model to use for speech to text.

Must be one of:
* "whisper-1"
Specific value: `"whisper-1"`

##### <a name="logic_units_items_anyOf_i1_speech_to_text_temperature"></a>6.1.2.5. Property `speech_to_text_temperature`

**Title:** Speech To Text Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

**Description:** The sampling temperature, between 0 and 1. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. If set to 0, the model will use log probability to automatically increase the temperature until certain thresholds are hit.

#### <a name="logic_units_items_anyOf_i2"></a>6.1.3. Property `Browser.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./Browser.json                                                       |

| Property                                                        | Pattern | Type             | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------- | ------- | ---------------- | ---------- | ---------- | ----------------- |
| - [implementation](#logic_units_items_anyOf_i2_implementation ) | No      | const            | No         | -          | Browser           |
| - [summarizer](#logic_units_items_anyOf_i2_summarizer )         | No      | enum (of string) | No         | -          | Summarizer        |

##### <a name="logic_units_items_anyOf_i2_implementation"></a>6.1.3.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** Browser

Specific value: `"Browser"`

##### <a name="logic_units_items_anyOf_i2_summarizer"></a>6.1.3.2. Property `summarizer`

**Title:** Summarizer

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | No                 |
| **Default**  | `"BeautifulSoup"`  |

Must be one of:
* "BeautifulSoup"
* "noop"

#### <a name="logic_units_items_anyOf_i3"></a>6.1.4. Property `OpenAIImageUnit.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./OpenAIImageUnit.json                                               |

| Property                                                                                  | Pattern | Type   | Deprecated | Definition                                       | Title/Description                              |
| ----------------------------------------------------------------------------------------- | ------- | ------ | ---------- | ------------------------------------------------ | ---------------------------------------------- |
| - [implementation](#logic_units_items_anyOf_i3_implementation )                           | No      | const  | No         | -                                                | OpenAIImageUnit                                |
| - [image_to_text_prompt](#logic_units_items_anyOf_i3_image_to_text_prompt )               | No      | string | No         | -                                                | Image To Text Prompt                           |
| - [text_to_image_prompt](#logic_units_items_anyOf_i3_text_to_image_prompt )               | No      | string | No         | -                                                | Text To Image Prompt                           |
| - [connection_handler](#logic_units_items_anyOf_i3_connection_handler )                   | No      | object | No         | In [OpenAIConnectionHandler](/docs/components/openaiconnectionhandler/overview) | Overview of OpenAIConnectionHandler components |
| - [image_to_text_model](#logic_units_items_anyOf_i3_image_to_text_model )                 | No      | string | No         | -                                                | Image To Text Model                            |
| - [text_to_image_model](#logic_units_items_anyOf_i3_text_to_image_model )                 | No      | string | No         | -                                                | Text To Image Model                            |
| - [temperature](#logic_units_items_anyOf_i3_temperature )                                 | No      | number | No         | -                                                | Temperature                                    |
| - [image_to_text_system_prompt](#logic_units_items_anyOf_i3_image_to_text_system_prompt ) | No      | string | No         | -                                                | Image To Text System Prompt                    |

##### <a name="logic_units_items_anyOf_i3_implementation"></a>6.1.4.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OpenAIImageUnit

Specific value: `"OpenAIImageUnit"`

##### <a name="logic_units_items_anyOf_i3_image_to_text_prompt"></a>6.1.4.2. Property `image_to_text_prompt`

**Title:** Image To Text Prompt

|              |                                                     |
| ------------ | --------------------------------------------------- |
| **Type**     | `string`                                            |
| **Required** | No                                                  |
| **Default**  | `"Use the following prompt to describe the image:"` |

**Description:** The prompt to use for the conversion. The text should be very verbose and detailed.

##### <a name="logic_units_items_anyOf_i3_text_to_image_prompt"></a>6.1.4.3. Property `text_to_image_prompt`

**Title:** Text To Image Prompt

|              |                                               |
| ------------ | --------------------------------------------- |
| **Type**     | `string`                                      |
| **Required** | No                                            |
| **Default**  | `"Use the provided text to create an image:"` |

**Description:** The prompt to use for the conversion. The text should be very verbose and detailed.

##### <a name="logic_units_items_anyOf_i3_connection_handler"></a>6.1.4.4. Property `connection_handler`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{"implementation": "OpenAIConnectionHandler"}`                           |
| **Defined in**            | [OpenAIConnectionHandler](/docs/components/openaiconnectionhandler/overview)                             |

**Description:** Overview of OpenAIConnectionHandler components

| Any of(Option)                                                                      |
| ----------------------------------------------------------------------------------- |
| [AzureOpenAIConnectionHandler.json](#llm_unit_anyOf_i3_connection_handler_anyOf_i0) |

###### <a name="llm_unit_anyOf_i3_connection_handler_anyOf_i0"></a>6.1.4.4.1. Property `AzureOpenAIConnectionHandler.json`

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

| Property                                                                                             | Pattern | Type            | Deprecated | Definition | Title/Description            |
| ---------------------------------------------------------------------------------------------------- | ------- | --------------- | ---------- | ---------- | ---------------------------- |
| - [implementation](#llm_unit_anyOf_i3_connection_handler_anyOf_i0_implementation )                   | No      | const           | No         | -          | AzureOpenAIConnectionHandler |
| - [azure_ad_token_provider](#llm_unit_anyOf_i3_connection_handler_anyOf_i0_azure_ad_token_provider ) | No      | Combination     | No         | -          | -                            |
| - [token_provider_scopes](#llm_unit_anyOf_i3_connection_handler_anyOf_i0_token_provider_scopes )     | No      | array of string | No         | -          | Token Provider Scopes        |
| - [api_version](#llm_unit_anyOf_i3_connection_handler_anyOf_i0_api_version )                         | No      | string          | No         | -          | Api Version                  |
| - [](#llm_unit_anyOf_i3_connection_handler_anyOf_i0_additionalProperties )                           | No      | object          | No         | -          | -                            |

###### <a name="llm_unit_anyOf_i3_connection_handler_anyOf_i0_implementation"></a>6.1.4.4.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AzureOpenAIConnectionHandler

Specific value: `"AzureOpenAIConnectionHandler"`

###### <a name="llm_unit_anyOf_i3_connection_handler_anyOf_i0_azure_ad_token_provider"></a>6.1.4.4.1.2. Property `azure_ad_token_provider`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

| Any of(Option)                                                                               |
| -------------------------------------------------------------------------------------------- |
| [Reference](#llm_unit_anyOf_i3_connection_handler_anyOf_i0_azure_ad_token_provider_anyOf_i0) |
| [item 1](#llm_unit_anyOf_i3_connection_handler_anyOf_i0_azure_ad_token_provider_anyOf_i1)    |

###### <a name="llm_unit_anyOf_i3_connection_handler_anyOf_i0_azure_ad_token_provider_anyOf_i0"></a>6.1.4.4.1.2.1. Property `Reference`

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

| Property                                                                                                            | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#llm_unit_anyOf_i3_connection_handler_anyOf_i0_azure_ad_token_provider_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#llm_unit_anyOf_i3_connection_handler_anyOf_i0_azure_ad_token_provider_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="llm_unit_anyOf_i3_connection_handler_anyOf_i0_azure_ad_token_provider_anyOf_i0_implementation"></a>6.1.4.4.1.2.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="llm_unit_anyOf_i3_connection_handler_anyOf_i0_azure_ad_token_provider_anyOf_i1"></a>6.1.4.4.1.2.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="llm_unit_anyOf_i3_connection_handler_anyOf_i0_token_provider_scopes"></a>6.1.4.4.1.3. Property `token_provider_scopes`

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

| Each item of this array must be                                                                           | Description |
| --------------------------------------------------------------------------------------------------------- | ----------- |
| [token_provider_scopes items](#llm_unit_anyOf_i3_connection_handler_anyOf_i0_token_provider_scopes_items) | -           |

###### <a name="autogenerated_heading_6"></a>6.1.4.4.1.3.1. token_provider_scopes items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

###### <a name="llm_unit_anyOf_i3_connection_handler_anyOf_i0_api_version"></a>6.1.4.4.1.4. Property `api_version`

**Title:** Api Version

|              |                |
| ------------ | -------------- |
| **Type**     | `string`       |
| **Required** | No             |
| **Default**  | `"2024-02-01"` |

##### <a name="logic_units_items_anyOf_i3_image_to_text_model"></a>6.1.4.5. Property `image_to_text_model`

**Title:** Image To Text Model

|              |                 |
| ------------ | --------------- |
| **Type**     | `string`        |
| **Required** | No              |
| **Default**  | `"gpt-4-turbo"` |

**Description:** The model to use for the vision LLM.

##### <a name="logic_units_items_anyOf_i3_text_to_image_model"></a>6.1.4.6. Property `text_to_image_model`

**Title:** Text To Image Model

|              |              |
| ------------ | ------------ |
| **Type**     | `string`     |
| **Required** | No           |
| **Default**  | `"dall-e-3"` |

**Description:** The model to use for the vision LLM.

##### <a name="logic_units_items_anyOf_i3_temperature"></a>6.1.4.7. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

##### <a name="logic_units_items_anyOf_i3_image_to_text_system_prompt"></a>6.1.4.8. Property `image_to_text_system_prompt`

**Title:** Image To Text System Prompt

|              |                                                                                                                                                                               |
| ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                                                                                      |
| **Required** | No                                                                                                                                                                            |
| **Default**  | `"You are an expert at answering questions about images. You are presented with an image and a question and must answer the question based on the information in the image."` |

**Description:** The system prompt to use for text to image.

#### <a name="logic_units_items_anyOf_i4"></a>6.1.5. Property `OpenAiSpeech.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./OpenAiSpeech.json                                                  |

| Property                                                                                | Pattern | Type             | Deprecated | Definition | Title/Description          |
| --------------------------------------------------------------------------------------- | ------- | ---------------- | ---------- | ---------- | -------------------------- |
| - [implementation](#logic_units_items_anyOf_i4_implementation )                         | No      | const            | No         | -          | OpenAiSpeech               |
| - [text_to_speech_model](#logic_units_items_anyOf_i4_text_to_speech_model )             | No      | enum (of string) | No         | -          | Text To Speech Model       |
| - [text_to_speech_voice](#logic_units_items_anyOf_i4_text_to_speech_voice )             | No      | enum (of string) | No         | -          | Text To Speech Voice       |
| - [speech_to_text_model](#logic_units_items_anyOf_i4_speech_to_text_model )             | No      | const            | No         | -          | Speech To Text Model       |
| - [speech_to_text_temperature](#logic_units_items_anyOf_i4_speech_to_text_temperature ) | No      | number           | No         | -          | Speech To Text Temperature |

##### <a name="logic_units_items_anyOf_i4_implementation"></a>6.1.5.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OpenAiSpeech

Specific value: `"OpenAiSpeech"`

##### <a name="logic_units_items_anyOf_i4_text_to_speech_model"></a>6.1.5.2. Property `text_to_speech_model`

**Title:** Text To Speech Model

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | No                 |
| **Default**  | `"tts-1-hd"`       |

**Description:** The model to use for text to speech.

Must be one of:
* "tts-1"
* "tts-1-hd"

##### <a name="logic_units_items_anyOf_i4_text_to_speech_voice"></a>6.1.5.3. Property `text_to_speech_voice`

**Title:** Text To Speech Voice

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | No                 |
| **Default**  | `"alloy"`          |

**Description:** The voice to use for text to speech.

Must be one of:
* "alloy"
* "echo"
* "fable"
* "onyx"
* "nova"
* "shimmer"

##### <a name="logic_units_items_anyOf_i4_speech_to_text_model"></a>6.1.5.4. Property `speech_to_text_model`

**Title:** Speech To Text Model

|              |               |
| ------------ | ------------- |
| **Type**     | `const`       |
| **Required** | No            |
| **Default**  | `"whisper-1"` |

**Description:** The model to use for speech to text.

Must be one of:
* "whisper-1"
Specific value: `"whisper-1"`

##### <a name="logic_units_items_anyOf_i4_speech_to_text_temperature"></a>6.1.5.5. Property `speech_to_text_temperature`

**Title:** Speech To Text Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

**Description:** The sampling temperature, between 0 and 1. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. If set to 0, the model will use log probability to automatically increase the temperature until certain thresholds are hit.

#### <a name="logic_units_items_anyOf_i5"></a>6.1.6. Property `Search.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./Search.json                                                        |

| Property                                                                  | Pattern | Type        | Deprecated | Definition | Title/Description   |
| ------------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------- |
| - [implementation](#logic_units_items_anyOf_i5_implementation )           | No      | const       | No         | -          | Search              |
| - [cse_id](#logic_units_items_anyOf_i5_cse_id )                           | No      | string      | No         | -          | Cse Id              |
| - [cse_token](#logic_units_items_anyOf_i5_cse_token )                     | No      | string      | No         | -          | Cse Token           |
| - [name](#logic_units_items_anyOf_i5_name )                               | No      | string      | No         | -          | Name                |
| - [description](#logic_units_items_anyOf_i5_description )                 | No      | string      | No         | -          | Description         |
| - [defaultDateRestrict](#logic_units_items_anyOf_i5_defaultDateRestrict ) | No      | Combination | No         | -          | Defaultdaterestrict |
| - [params](#logic_units_items_anyOf_i5_params )                           | No      | Combination | No         | -          | Params              |

##### <a name="logic_units_items_anyOf_i5_implementation"></a>6.1.6.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** Search

Specific value: `"Search"`

##### <a name="logic_units_items_anyOf_i5_cse_id"></a>6.1.6.2. Property `cse_id`

**Title:** Cse Id

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

##### <a name="logic_units_items_anyOf_i5_cse_token"></a>6.1.6.3. Property `cse_token`

**Title:** Cse Token

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

##### <a name="logic_units_items_anyOf_i5_name"></a>6.1.6.4. Property `name`

**Title:** Name

|              |            |
| ------------ | ---------- |
| **Type**     | `string`   |
| **Required** | No         |
| **Default**  | `"search"` |

##### <a name="logic_units_items_anyOf_i5_description"></a>6.1.6.5. Property `description`

**Title:** Description

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="logic_units_items_anyOf_i5_defaultDateRestrict"></a>6.1.6.6. Property `defaultDateRestrict`

**Title:** Defaultdaterestrict

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                     |
| ------------------------------------------------------------------ |
| [item 0](#logic_units_items_anyOf_i5_defaultDateRestrict_anyOf_i0) |
| [item 1](#logic_units_items_anyOf_i5_defaultDateRestrict_anyOf_i1) |

###### <a name="logic_units_items_anyOf_i5_defaultDateRestrict_anyOf_i0"></a>6.1.6.6.1. Property `item 0`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

###### <a name="logic_units_items_anyOf_i5_defaultDateRestrict_anyOf_i1"></a>6.1.6.6.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

##### <a name="logic_units_items_anyOf_i5_params"></a>6.1.6.7. Property `params`

**Title:** Params

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

| Any of(Option)                                        |
| ----------------------------------------------------- |
| [item 0](#logic_units_items_anyOf_i5_params_anyOf_i0) |
| [item 1](#logic_units_items_anyOf_i5_params_anyOf_i1) |

###### <a name="logic_units_items_anyOf_i5_params_anyOf_i0"></a>6.1.6.7.1. Property `item 0`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

###### <a name="logic_units_items_anyOf_i5_params_anyOf_i1"></a>6.1.6.7.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="logic_units_items_anyOf_i6"></a>6.1.7. Property `WebSearch.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./WebSearch.json                                                     |

| Property                                                                  | Pattern | Type             | Deprecated | Definition | Title/Description   |
| ------------------------------------------------------------------------- | ------- | ---------------- | ---------- | ---------- | ------------------- |
| - [implementation](#logic_units_items_anyOf_i6_implementation )           | No      | const            | No         | -          | WebSearch           |
| - [summarizer](#logic_units_items_anyOf_i6_summarizer )                   | No      | enum (of string) | No         | -          | Summarizer          |
| - [cse_id](#logic_units_items_anyOf_i6_cse_id )                           | No      | string           | No         | -          | Cse Id              |
| - [cse_token](#logic_units_items_anyOf_i6_cse_token )                     | No      | string           | No         | -          | Cse Token           |
| - [name](#logic_units_items_anyOf_i6_name )                               | No      | string           | No         | -          | Name                |
| - [description](#logic_units_items_anyOf_i6_description )                 | No      | string           | No         | -          | Description         |
| - [defaultDateRestrict](#logic_units_items_anyOf_i6_defaultDateRestrict ) | No      | Combination      | No         | -          | Defaultdaterestrict |
| - [params](#logic_units_items_anyOf_i6_params )                           | No      | Combination      | No         | -          | Params              |

##### <a name="logic_units_items_anyOf_i6_implementation"></a>6.1.7.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** WebSearch

Specific value: `"WebSearch"`

##### <a name="logic_units_items_anyOf_i6_summarizer"></a>6.1.7.2. Property `summarizer`

**Title:** Summarizer

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | No                 |
| **Default**  | `"BeautifulSoup"`  |

Must be one of:
* "BeautifulSoup"
* "noop"

##### <a name="logic_units_items_anyOf_i6_cse_id"></a>6.1.7.3. Property `cse_id`

**Title:** Cse Id

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

##### <a name="logic_units_items_anyOf_i6_cse_token"></a>6.1.7.4. Property `cse_token`

**Title:** Cse Token

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

##### <a name="logic_units_items_anyOf_i6_name"></a>6.1.7.5. Property `name`

**Title:** Name

|              |            |
| ------------ | ---------- |
| **Type**     | `string`   |
| **Required** | No         |
| **Default**  | `"search"` |

##### <a name="logic_units_items_anyOf_i6_description"></a>6.1.7.6. Property `description`

**Title:** Description

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="logic_units_items_anyOf_i6_defaultDateRestrict"></a>6.1.7.7. Property `defaultDateRestrict`

**Title:** Defaultdaterestrict

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                     |
| ------------------------------------------------------------------ |
| [item 0](#logic_units_items_anyOf_i6_defaultDateRestrict_anyOf_i0) |
| [item 1](#logic_units_items_anyOf_i6_defaultDateRestrict_anyOf_i1) |

###### <a name="logic_units_items_anyOf_i6_defaultDateRestrict_anyOf_i0"></a>6.1.7.7.1. Property `item 0`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

###### <a name="logic_units_items_anyOf_i6_defaultDateRestrict_anyOf_i1"></a>6.1.7.7.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

##### <a name="logic_units_items_anyOf_i6_params"></a>6.1.7.8. Property `params`

**Title:** Params

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

| Any of(Option)                                        |
| ----------------------------------------------------- |
| [item 0](#logic_units_items_anyOf_i6_params_anyOf_i0) |
| [item 1](#logic_units_items_anyOf_i6_params_anyOf_i1) |

###### <a name="logic_units_items_anyOf_i6_params_anyOf_i0"></a>6.1.7.8.1. Property `item 0`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

###### <a name="logic_units_items_anyOf_i6_params_anyOf_i1"></a>6.1.7.8.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

## <a name="audio_unit"></a>7. Property `audio_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                        |
| ------------------------------------- |
| [overview.json](#audio_unit_anyOf_i0) |
| [item 1](#audio_unit_anyOf_i1)        |

### <a name="audio_unit_anyOf_i0"></a>7.1. Property `overview.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | [AudioUnit](/docs/components/audiounit/overview)                                           |

**Description:** Overview of AudioUnit components

| Any of(Option)                                     |
| -------------------------------------------------- |
| [OpenAiSpeech.json](#audio_unit_anyOf_i0_anyOf_i0) |

#### <a name="audio_unit_anyOf_i0_anyOf_i0"></a>7.1.1. Property `OpenAiSpeech.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./OpenAiSpeech.json                                                  |

| Property                                                                                  | Pattern | Type             | Deprecated | Definition | Title/Description          |
| ----------------------------------------------------------------------------------------- | ------- | ---------------- | ---------- | ---------- | -------------------------- |
| - [implementation](#audio_unit_anyOf_i0_anyOf_i0_implementation )                         | No      | const            | No         | -          | OpenAiSpeech               |
| - [text_to_speech_model](#audio_unit_anyOf_i0_anyOf_i0_text_to_speech_model )             | No      | enum (of string) | No         | -          | Text To Speech Model       |
| - [text_to_speech_voice](#audio_unit_anyOf_i0_anyOf_i0_text_to_speech_voice )             | No      | enum (of string) | No         | -          | Text To Speech Voice       |
| - [speech_to_text_model](#audio_unit_anyOf_i0_anyOf_i0_speech_to_text_model )             | No      | const            | No         | -          | Speech To Text Model       |
| - [speech_to_text_temperature](#audio_unit_anyOf_i0_anyOf_i0_speech_to_text_temperature ) | No      | number           | No         | -          | Speech To Text Temperature |

##### <a name="audio_unit_anyOf_i0_anyOf_i0_implementation"></a>7.1.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OpenAiSpeech

Specific value: `"OpenAiSpeech"`

##### <a name="audio_unit_anyOf_i0_anyOf_i0_text_to_speech_model"></a>7.1.1.2. Property `text_to_speech_model`

**Title:** Text To Speech Model

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | No                 |
| **Default**  | `"tts-1-hd"`       |

**Description:** The model to use for text to speech.

Must be one of:
* "tts-1"
* "tts-1-hd"

##### <a name="audio_unit_anyOf_i0_anyOf_i0_text_to_speech_voice"></a>7.1.1.3. Property `text_to_speech_voice`

**Title:** Text To Speech Voice

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | No                 |
| **Default**  | `"alloy"`          |

**Description:** The voice to use for text to speech.

Must be one of:
* "alloy"
* "echo"
* "fable"
* "onyx"
* "nova"
* "shimmer"

##### <a name="audio_unit_anyOf_i0_anyOf_i0_speech_to_text_model"></a>7.1.1.4. Property `speech_to_text_model`

**Title:** Speech To Text Model

|              |               |
| ------------ | ------------- |
| **Type**     | `const`       |
| **Required** | No            |
| **Default**  | `"whisper-1"` |

**Description:** The model to use for speech to text.

Must be one of:
* "whisper-1"
Specific value: `"whisper-1"`

##### <a name="audio_unit_anyOf_i0_anyOf_i0_speech_to_text_temperature"></a>7.1.1.5. Property `speech_to_text_temperature`

**Title:** Speech To Text Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

**Description:** The sampling temperature, between 0 and 1. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. If set to 0, the model will use log probability to automatically increase the temperature until certain thresholds are hit.

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

| Property                                                 | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#image_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#image_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

#### <a name="image_unit_anyOf_i0_implementation"></a>8.1.1. Property `implementation`

**Title:** Implementation

|              |               |
| ------------ | ------------- |
| **Type**     | `string`      |
| **Required** | No            |
| **Default**  | `"ImageUnit"` |

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

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{"implementation": "DocumentProcessor"}`                                 |
| **Defined in**            | [DocumentProcessor](/docs/components/documentprocessor/overview)                                   |

**Description:** Overview of DocumentProcessor components

| Any of(Option)                                         |
| ------------------------------------------------------ |
| [DocumentProcessor.json](#document_processor_anyOf_i0) |

### <a name="document_processor_anyOf_i0"></a>11.1. Property `DocumentProcessor.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./DocumentProcessor.json                                             |

| Property                                                         | Pattern | Type   | Deprecated | Definition                                   | Title/Description                          |
| ---------------------------------------------------------------- | ------- | ------ | ---------- | -------------------------------------------- | ------------------------------------------ |
| - [implementation](#document_processor_anyOf_i0_implementation ) | No      | const  | No         | -                                            | DocumentProcessor                          |
| - [parser](#document_processor_anyOf_i0_parser )                 | No      | object | No         | In [DocumentParser](/docs/components/documentparser/overview)      | Overview of DocumentParser components      |
| - [splitter](#document_processor_anyOf_i0_splitter )             | No      | object | No         | In [DocumentTransformer](/docs/components/documenttransformer/overview) | Overview of DocumentTransformer components |

#### <a name="document_processor_anyOf_i0_implementation"></a>11.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** DocumentProcessor

Specific value: `"DocumentProcessor"`

#### <a name="document_processor_anyOf_i0_parser"></a>11.1.2. Property `parser`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{"implementation": "AutoParser"}`                                        |
| **Defined in**            | [DocumentParser](/docs/components/documentparser/overview)                                      |

**Description:** Overview of DocumentParser components

| Any of(Option)                                                  |
| --------------------------------------------------------------- |
| [AutoParser.json](#document_processor_anyOf_i0_parser_anyOf_i0) |

##### <a name="document_processor_anyOf_i0_parser_anyOf_i0"></a>11.1.2.1. Property `AutoParser.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./AutoParser.json                                                    |

| Property                                                                         | Pattern | Type  | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------------------- | ------- | ----- | ---------- | ---------- | ----------------- |
| - [implementation](#document_processor_anyOf_i0_parser_anyOf_i0_implementation ) | No      | const | No         | -          | AutoParser        |

###### <a name="document_processor_anyOf_i0_parser_anyOf_i0_implementation"></a>11.1.2.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AutoParser

Specific value: `"AutoParser"`

#### <a name="document_processor_anyOf_i0_splitter"></a>11.1.3. Property `splitter`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{"implementation": "AutoTransformer"}`                                   |
| **Defined in**            | [DocumentTransformer](/docs/components/documenttransformer/overview)                                 |

**Description:** Overview of DocumentTransformer components

| Any of(Option)                                                         |
| ---------------------------------------------------------------------- |
| [AutoTransformer.json](#document_processor_anyOf_i0_splitter_anyOf_i0) |

##### <a name="document_processor_anyOf_i0_splitter_anyOf_i0"></a>11.1.3.1. Property `AutoTransformer.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./AutoTransformer.json                                               |

| Property                                                                           | Pattern | Type  | Deprecated | Definition | Title/Description |
| ---------------------------------------------------------------------------------- | ------- | ----- | ---------- | ---------- | ----------------- |
| - [implementation](#document_processor_anyOf_i0_splitter_anyOf_i0_implementation ) | No      | const | No         | -          | AutoTransformer   |

###### <a name="document_processor_anyOf_i0_splitter_anyOf_i0_implementation"></a>11.1.3.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AutoTransformer

Specific value: `"AutoTransformer"`

----------------------------------------------------------------------------------------------------------------------------
