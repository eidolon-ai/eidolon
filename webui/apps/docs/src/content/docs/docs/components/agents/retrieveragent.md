---
title: RetrieverAgent
description: Description of RetrieverAgent component
---

**Description:** A RetrieverAgent is an agent that will take a query, rewrite it for better similarity vector search, and then perform the vector search on the document store.
The agent will dynamically load and embed files, so it is not performant for loading large bodies of files, but performs very well for small to medium-sized document stores (hundreds to thousands of documents) which are updating frequently.

| Property                                         | Pattern | Type        | Deprecated | Definition | Title/Description                           |
| ------------------------------------------------ | ------- | ----------- | ---------- | ---------- | ------------------------------------------- |
| - [implementation](#implementation )             | No      | const       | No         | -          | RetrieverAgent                              |
| - [max_num_results](#max_num_results )           | No      | integer     | No         | -          | Max Num Results                             |
| - [question_transformer](#question_transformer ) | No      | object      | No         | -          | QuestionTransformer Reference               |
| - [document_retriever](#document_retriever )     | No      | object      | No         | -          | DocumentRetriever Reference                 |
| - [document_reranker](#document_reranker )       | No      | object      | No         | -          | DocumentReranker Reference                  |
| - [result_summarizer](#result_summarizer )       | No      | object      | No         | -          | ResultSummarizer Reference                  |
| + [name](#name )                                 | No      | string      | No         | -          | Name                                        |
| + [description](#description )                   | No      | string      | No         | -          | Description                                 |
| - [loader_root_location](#loader_root_location ) | No      | Combination | No         | -          | Loader Root Location                        |
| - [loader_pattern](#loader_pattern )             | No      | Combination | No         | -          | Loader Pattern                              |
| - [document_manager](#document_manager )         | No      | Combination | No         | -          | -                                           |
| - [apu](#apu )                                   | No      | object      | No         | In         | The APU to use for question transformation. |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** RetrieverAgent

Specific value: `"RetrieverAgent"`

## <a name="max_num_results"></a>2. Property `max_num_results`

**Title:** Max Num Results

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `10`      |

**Description:** The maximum number of results to consider.

## <a name="question_transformer"></a>3. Property `question_transformer`

**Title:** QuestionTransformer Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"QuestionTransformer"`                                                   |

| Property                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#question_transformer_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#question_transformer_additionalProperties )         | No      | object | No         | -          | -                 |

### <a name="question_transformer_implementation"></a>3.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

## <a name="document_retriever"></a>4. Property `document_retriever`

**Title:** DocumentRetriever Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"DocumentRetriever"`                                                     |

| Property                                                | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#document_retriever_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#document_retriever_additionalProperties )         | No      | object | No         | -          | -                 |

### <a name="document_retriever_implementation"></a>4.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

## <a name="document_reranker"></a>5. Property `document_reranker`

**Title:** DocumentReranker Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"DocumentReranker"`                                                      |

| Property                                               | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------ | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#document_reranker_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#document_reranker_additionalProperties )         | No      | object | No         | -          | -                 |

### <a name="document_reranker_implementation"></a>5.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

## <a name="result_summarizer"></a>6. Property `result_summarizer`

**Title:** ResultSummarizer Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"ResultSummarizer"`                                                      |

| Property                                               | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------ | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#result_summarizer_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#result_summarizer_additionalProperties )         | No      | object | No         | -          | -                 |

### <a name="result_summarizer_implementation"></a>6.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

## <a name="name"></a>7. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** The name of the document store to use.

## <a name="description"></a>8. Property `description`

**Title:** Description

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** A detailed description of the the retriever including all necessary information for the calling agent to decide to call this agent, i.e. file type or location or etc...

## <a name="loader_root_location"></a>9. Property `loader_root_location`

**Title:** Loader Root Location

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

**Description:** A URL specifying the root location of the loader.

| Any of(Option)                           |
| ---------------------------------------- |
| [item 0](#loader_root_location_anyOf_i0) |
| [item 1](#loader_root_location_anyOf_i1) |

### <a name="loader_root_location_anyOf_i0"></a>9.1. Property `item 0`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

### <a name="loader_root_location_anyOf_i1"></a>9.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

## <a name="loader_pattern"></a>10. Property `loader_pattern`

**Title:** Loader Pattern

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"**/*"`                                                                  |

**Description:** The search pattern to use when loading files.

| Any of(Option)                     |
| ---------------------------------- |
| [item 0](#loader_pattern_anyOf_i0) |
| [item 1](#loader_pattern_anyOf_i1) |

### <a name="loader_pattern_anyOf_i0"></a>10.1. Property `item 0`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

### <a name="loader_pattern_anyOf_i1"></a>10.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

## <a name="document_manager"></a>11. Property `document_manager`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                          |
| ------------------------------------------------------- |
| [DocumentManager Reference](#document_manager_anyOf_i0) |
| [item 1](#document_manager_anyOf_i1)                    |

### <a name="document_manager_anyOf_i0"></a>11.1. Property `DocumentManager Reference`

**Title:** DocumentManager Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.agent.doc_manager.document_manager.DocumentManager"`     |

| Property                                                       | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#document_manager_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#document_manager_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

#### <a name="document_manager_anyOf_i0_implementation"></a>11.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

### <a name="document_manager_anyOf_i1"></a>11.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

## <a name="apu"></a>12. Property `apu`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"APU"`                                                                   |
| **Defined in**            |                                                                           |

**Description:** The APU to use for question transformation.

| Any of(Option)                          |
| --------------------------------------- |
| [ClaudeHaiku.json](#apu_anyOf_i0)       |
| [ClaudeOpus.json](#apu_anyOf_i1)        |
| [ClaudeSonnet.json](#apu_anyOf_i2)      |
| [ConversationalAPU.json](#apu_anyOf_i3) |
| [GPT3.5-turbo.json](#apu_anyOf_i4)      |
| [GPT4-turbo.json](#apu_anyOf_i5)        |
| [GPT4o.json](#apu_anyOf_i6)             |
| [Llamma3-8b.json](#apu_anyOf_i7)        |
| [MistralLarge.json](#apu_anyOf_i8)      |
| [MistralMedium.json](#apu_anyOf_i9)     |
| [MistralSmall.json](#apu_anyOf_i10)     |

### <a name="apu_anyOf_i0"></a>12.1. Property `ClaudeHaiku.json`

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
| - [llm_unit](#apu_anyOf_i0_llm_unit )                             | No      | object          | No         | In [LLMUnit](/docs/components/llmunit/overview) | Overview of <class 'eidolon_ai_sdk.apu.llm_unit.LLMUnit'> components |
| - [logic_units](#apu_anyOf_i0_logic_units )                       | No      | array of object | No         | -                                | Logic Units                                                          |
| - [audio_unit](#apu_anyOf_i0_audio_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [image_unit](#apu_anyOf_i0_image_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [record_conversation](#apu_anyOf_i0_record_conversation )       | No      | boolean         | No         | -                                | Record Conversation                                                  |
| - [allow_tool_errors](#apu_anyOf_i0_allow_tool_errors )           | No      | boolean         | No         | -                                | Allow Tool Errors                                                    |
| - [document_processor](#apu_anyOf_i0_document_processor )         | No      | object          | No         | -                                | DocumentProcessor Reference                                          |
| - [retriever](#apu_anyOf_i0_retriever )                           | No      | object          | No         | -                                | Retriever Reference                                                  |
| - [retriever_apu](#apu_anyOf_i0_retriever_apu )                   | No      | Combination     | No         | -                                | -                                                                    |

#### <a name="apu_anyOf_i0_implementation"></a>12.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ClaudeHaiku

Specific value: `"ClaudeHaiku"`

#### <a name="apu_anyOf_i0_max_num_function_calls"></a>12.1.2. Property `max_num_function_calls`

**Title:** Max Num Function Calls

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `10`      |

**Description:** The maximum number of function calls to make in a single request.

#### <a name="apu_anyOf_i0_io_unit"></a>12.1.3. Property `io_unit`

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

##### <a name="apu_anyOf_i0_io_unit_implementation"></a>12.1.3.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i0_memory_unit"></a>12.1.4. Property `memory_unit`

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

##### <a name="apu_anyOf_i0_memory_unit_implementation"></a>12.1.4.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i0_llm_unit"></a>12.1.5. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Defined in**            | [LLMUnit](/docs/components/llmunit/overview)                                             |

**Description:** Overview of <class 'eidolon_ai_sdk.apu.llm_unit.LLMUnit'> components

| Any of(Option)                                             |
| ---------------------------------------------------------- |
| [AnthropicLLMUnit.json](#apu_anyOf_i0_llm_unit_anyOf_i0)   |
| [MistralGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i1)         |
| [OllamaLLMUnit.json](#apu_anyOf_i0_llm_unit_anyOf_i2)      |
| [OpenAIGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i3)          |
| [ToolCallLLMWrapper.json](#apu_anyOf_i0_llm_unit_anyOf_i4) |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i0"></a>12.1.5.1. Property `AnthropicLLMUnit.json`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_implementation"></a>12.1.5.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AnthropicLLMUnit

Specific value: `"AnthropicLLMUnit"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model"></a>12.1.5.1.2. Property `model`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model_implementation"></a>12.1.5.1.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_temperature"></a>12.1.5.1.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens"></a>12.1.5.1.4. Property `max_tokens`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i0"></a>12.1.5.1.4.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i1"></a>12.1.5.1.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_client_args"></a>12.1.5.1.5. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i1"></a>12.1.5.2. Property `MistralGPT.json`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_implementation"></a>12.1.5.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** MistralGPT

Specific value: `"MistralGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model"></a>12.1.5.2.2. Property `model`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model_implementation"></a>12.1.5.2.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_temperature"></a>12.1.5.2.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_force_json"></a>12.1.5.2.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens"></a>12.1.5.2.5. Property `max_tokens`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i0"></a>12.1.5.2.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i1"></a>12.1.5.2.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_client_args"></a>12.1.5.2.6. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i2"></a>12.1.5.3. Property `OllamaLLMUnit.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./OllamaLLMUnit.json                                                 |

| Property                                                            | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_implementation ) | No      | const       | No         | -          | OllamaLLMUnit      |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i2_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i2_temperature )       | No      | number      | No         | -          | Temperature        |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i2_force_json )         | No      | boolean     | No         | -          | Force Json         |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_options](#apu_anyOf_i0_llm_unit_anyOf_i2_client_options ) | No      | object      | No         | -          | Client Options     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_implementation"></a>12.1.5.3.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OllamaLLMUnit

Specific value: `"OllamaLLMUnit"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model"></a>12.1.5.3.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"llama3"`                                                                |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i2_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation"></a>12.1.5.3.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_temperature"></a>12.1.5.3.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_force_json"></a>12.1.5.3.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens"></a>12.1.5.3.5. Property `max_tokens`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i0"></a>12.1.5.3.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i1"></a>12.1.5.3.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_client_options"></a>12.1.5.3.6. Property `client_options`

**Title:** Client Options

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i3"></a>12.1.5.4. Property `OpenAIGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./OpenAIGPT.json                                                     |

| Property                                                                    | Pattern | Type        | Deprecated | Definition | Title/Description                 |
| --------------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | --------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_implementation )         | No      | const       | No         | -          | OpenAIGPT                         |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i3_model )                           | No      | object      | No         | -          | LLMModel Reference                |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i3_temperature )               | No      | number      | No         | -          | Temperature                       |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i3_force_json )                 | No      | boolean     | No         | -          | Force Json                        |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens )                 | No      | Combination | No         | -          | Max Tokens                        |
| - [connection_handler](#apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler ) | No      | object      | No         | -          | OpenAIConnectionHandler Reference |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_implementation"></a>12.1.5.4.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OpenAIGPT

Specific value: `"OpenAIGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model"></a>12.1.5.4.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"gpt-4-turbo"`                                                           |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i3_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_implementation"></a>12.1.5.4.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_temperature"></a>12.1.5.4.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_force_json"></a>12.1.5.4.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens"></a>12.1.5.4.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens_anyOf_i0"></a>12.1.5.4.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens_anyOf_i1"></a>12.1.5.4.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler"></a>12.1.5.4.6. Property `connection_handler`

**Title:** OpenAIConnectionHandler Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"OpenAIConnectionHandler"`                                               |

| Property                                                                               | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler_implementation"></a>12.1.5.4.6.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i4"></a>12.1.5.5. Property `ToolCallLLMWrapper.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./ToolCallLLMWrapper.json                                            |

| Property                                                                      | Pattern | Type        | Deprecated | Definition                                  | Title/Description                                                    |
| ----------------------------------------------------------------------------- | ------- | ----------- | ---------- | ------------------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i4_implementation )           | No      | const       | No         | -                                           | ToolCallLLMWrapper                                                   |
| - [tool_message_prompt](#apu_anyOf_i0_llm_unit_anyOf_i4_tool_message_prompt ) | No      | string      | No         | -                                           | Tool Message Prompt                                                  |
| - [llm_unit](#apu_anyOf_i0_llm_unit_anyOf_i4_llm_unit )                       | No      | object      | No         | Same as [llm_unit](#apu_anyOf_i0_llm_unit ) | Overview of <class 'eidolon_ai_sdk.apu.llm_unit.LLMUnit'> components |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i4_model )                             | No      | Combination | No         | -                                           | -                                                                    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_implementation"></a>12.1.5.5.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ToolCallLLMWrapper

Specific value: `"ToolCallLLMWrapper"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_tool_message_prompt"></a>12.1.5.5.2. Property `tool_message_prompt`

**Title:** Tool Message Prompt

|              |                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Required** | No                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Default**  | `"You must follow these instructions:\nYou can select zero or more of the above tools based on the user query\nIf there are multiple tools required, make sure a list of tools are returned in a JSON array.\nIf there is no tool that match the user request or you have already answered the question, you will respond with empty json array for the tools.\nYou can also add any additional notes or explanations in the notes field."` |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_llm_unit"></a>12.1.5.5.3. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Same definition as**    | [llm_unit](#apu_anyOf_i0_llm_unit)                                        |

**Description:** Overview of <class 'eidolon_ai_sdk.apu.llm_unit.LLMUnit'> components

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_model"></a>12.1.5.5.4. Property `model`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                       |
| -------------------------------------------------------------------- |
| [LLMModel Reference](#apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i1)             |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0"></a>12.1.5.5.4.1. Property `LLMModel Reference`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.llm_unit.LLMModel"`                                  |

| Property                                                                           | Pattern | Type   | Deprecated | Definition | Title/Description |
| ---------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0_implementation"></a>12.1.5.5.4.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i1"></a>12.1.5.5.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i0_logic_units"></a>12.1.6. Property `logic_units`

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

##### <a name="autogenerated_heading_2"></a>12.1.6.1. LogicUnit Reference

**Title:** LogicUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.logic_unit.LogicUnit"`                               |

| Property                                                            | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_logic_units_items_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_logic_units_items_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_logic_units_items_implementation"></a>12.1.6.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i0_audio_unit"></a>12.1.7. Property `audio_unit`

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

##### <a name="apu_anyOf_i0_audio_unit_anyOf_i0"></a>12.1.7.1. Property `AudioUnit Reference`

**Title:** AudioUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.audio_unit.AudioUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_audio_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_audio_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_audio_unit_anyOf_i0_implementation"></a>12.1.7.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i0_audio_unit_anyOf_i1"></a>12.1.7.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i0_image_unit"></a>12.1.8. Property `image_unit`

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

##### <a name="apu_anyOf_i0_image_unit_anyOf_i0"></a>12.1.8.1. Property `ImageUnit Reference`

**Title:** ImageUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.image_unit.ImageUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_image_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_image_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_image_unit_anyOf_i0_implementation"></a>12.1.8.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i0_image_unit_anyOf_i1"></a>12.1.8.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i0_record_conversation"></a>12.1.9. Property `record_conversation`

**Title:** Record Conversation

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

#### <a name="apu_anyOf_i0_allow_tool_errors"></a>12.1.10. Property `allow_tool_errors`

**Title:** Allow Tool Errors

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

#### <a name="apu_anyOf_i0_document_processor"></a>12.1.11. Property `document_processor`

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

##### <a name="apu_anyOf_i0_document_processor_implementation"></a>12.1.11.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i0_retriever"></a>12.1.12. Property `retriever`

**Title:** Retriever Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"Retriever"`                                                             |

| Property                                                    | Pattern | Type   | Deprecated | Definition | Title/Description |
| ----------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_retriever_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_retriever_additionalProperties )         | No      | object | No         | -          | -                 |

##### <a name="apu_anyOf_i0_retriever_implementation"></a>12.1.12.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i0_retriever_apu"></a>12.1.13. Property `retriever_apu`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                        |
| ----------------------------------------------------- |
| [APU Reference](#apu_anyOf_i0_retriever_apu_anyOf_i0) |
| [item 1](#apu_anyOf_i0_retriever_apu_anyOf_i1)        |

##### <a name="apu_anyOf_i0_retriever_apu_anyOf_i0"></a>12.1.13.1. Property `APU Reference`

**Title:** APU Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.apu.APU"`                                            |

| Property                                                                 | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------ | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_retriever_apu_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_retriever_apu_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_retriever_apu_anyOf_i0_implementation"></a>12.1.13.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i0_retriever_apu_anyOf_i1"></a>12.1.13.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

### <a name="apu_anyOf_i1"></a>12.2. Property `ClaudeOpus.json`

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
| - [llm_unit](#apu_anyOf_i1_llm_unit )                             | No      | object          | No         | In [LLMUnit](/docs/components/llmunit/overview) | Overview of <class 'eidolon_ai_sdk.apu.llm_unit.LLMUnit'> components |
| - [logic_units](#apu_anyOf_i1_logic_units )                       | No      | array of object | No         | -                                | Logic Units                                                          |
| - [audio_unit](#apu_anyOf_i1_audio_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [image_unit](#apu_anyOf_i1_image_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [record_conversation](#apu_anyOf_i1_record_conversation )       | No      | boolean         | No         | -                                | Record Conversation                                                  |
| - [allow_tool_errors](#apu_anyOf_i1_allow_tool_errors )           | No      | boolean         | No         | -                                | Allow Tool Errors                                                    |
| - [document_processor](#apu_anyOf_i1_document_processor )         | No      | object          | No         | -                                | DocumentProcessor Reference                                          |
| - [retriever](#apu_anyOf_i1_retriever )                           | No      | object          | No         | -                                | Retriever Reference                                                  |
| - [retriever_apu](#apu_anyOf_i1_retriever_apu )                   | No      | Combination     | No         | -                                | -                                                                    |

#### <a name="apu_anyOf_i1_implementation"></a>12.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ClaudeOpus

Specific value: `"ClaudeOpus"`

#### <a name="apu_anyOf_i1_max_num_function_calls"></a>12.2.2. Property `max_num_function_calls`

**Title:** Max Num Function Calls

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `10`      |

**Description:** The maximum number of function calls to make in a single request.

#### <a name="apu_anyOf_i1_io_unit"></a>12.2.3. Property `io_unit`

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

##### <a name="apu_anyOf_i1_io_unit_implementation"></a>12.2.3.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i1_memory_unit"></a>12.2.4. Property `memory_unit`

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

##### <a name="apu_anyOf_i1_memory_unit_implementation"></a>12.2.4.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i1_llm_unit"></a>12.2.5. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Defined in**            | [LLMUnit](/docs/components/llmunit/overview)                                             |

**Description:** Overview of <class 'eidolon_ai_sdk.apu.llm_unit.LLMUnit'> components

| Any of(Option)                                             |
| ---------------------------------------------------------- |
| [AnthropicLLMUnit.json](#apu_anyOf_i0_llm_unit_anyOf_i0)   |
| [MistralGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i1)         |
| [OllamaLLMUnit.json](#apu_anyOf_i0_llm_unit_anyOf_i2)      |
| [OpenAIGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i3)          |
| [ToolCallLLMWrapper.json](#apu_anyOf_i0_llm_unit_anyOf_i4) |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i0"></a>12.2.5.1. Property `AnthropicLLMUnit.json`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_implementation"></a>12.2.5.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AnthropicLLMUnit

Specific value: `"AnthropicLLMUnit"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model"></a>12.2.5.1.2. Property `model`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model_implementation"></a>12.2.5.1.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_temperature"></a>12.2.5.1.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens"></a>12.2.5.1.4. Property `max_tokens`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i0"></a>12.2.5.1.4.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i1"></a>12.2.5.1.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_client_args"></a>12.2.5.1.5. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i1"></a>12.2.5.2. Property `MistralGPT.json`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_implementation"></a>12.2.5.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** MistralGPT

Specific value: `"MistralGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model"></a>12.2.5.2.2. Property `model`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model_implementation"></a>12.2.5.2.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_temperature"></a>12.2.5.2.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_force_json"></a>12.2.5.2.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens"></a>12.2.5.2.5. Property `max_tokens`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i0"></a>12.2.5.2.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i1"></a>12.2.5.2.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_client_args"></a>12.2.5.2.6. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i2"></a>12.2.5.3. Property `OllamaLLMUnit.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./OllamaLLMUnit.json                                                 |

| Property                                                            | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_implementation ) | No      | const       | No         | -          | OllamaLLMUnit      |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i2_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i2_temperature )       | No      | number      | No         | -          | Temperature        |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i2_force_json )         | No      | boolean     | No         | -          | Force Json         |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_options](#apu_anyOf_i0_llm_unit_anyOf_i2_client_options ) | No      | object      | No         | -          | Client Options     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_implementation"></a>12.2.5.3.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OllamaLLMUnit

Specific value: `"OllamaLLMUnit"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model"></a>12.2.5.3.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"llama3"`                                                                |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i2_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation"></a>12.2.5.3.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_temperature"></a>12.2.5.3.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_force_json"></a>12.2.5.3.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens"></a>12.2.5.3.5. Property `max_tokens`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i0"></a>12.2.5.3.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i1"></a>12.2.5.3.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_client_options"></a>12.2.5.3.6. Property `client_options`

**Title:** Client Options

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i3"></a>12.2.5.4. Property `OpenAIGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./OpenAIGPT.json                                                     |

| Property                                                                    | Pattern | Type        | Deprecated | Definition | Title/Description                 |
| --------------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | --------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_implementation )         | No      | const       | No         | -          | OpenAIGPT                         |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i3_model )                           | No      | object      | No         | -          | LLMModel Reference                |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i3_temperature )               | No      | number      | No         | -          | Temperature                       |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i3_force_json )                 | No      | boolean     | No         | -          | Force Json                        |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens )                 | No      | Combination | No         | -          | Max Tokens                        |
| - [connection_handler](#apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler ) | No      | object      | No         | -          | OpenAIConnectionHandler Reference |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_implementation"></a>12.2.5.4.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OpenAIGPT

Specific value: `"OpenAIGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model"></a>12.2.5.4.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"gpt-4-turbo"`                                                           |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i3_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_implementation"></a>12.2.5.4.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_temperature"></a>12.2.5.4.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_force_json"></a>12.2.5.4.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens"></a>12.2.5.4.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens_anyOf_i0"></a>12.2.5.4.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens_anyOf_i1"></a>12.2.5.4.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler"></a>12.2.5.4.6. Property `connection_handler`

**Title:** OpenAIConnectionHandler Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"OpenAIConnectionHandler"`                                               |

| Property                                                                               | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler_implementation"></a>12.2.5.4.6.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i4"></a>12.2.5.5. Property `ToolCallLLMWrapper.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./ToolCallLLMWrapper.json                                            |

| Property                                                                      | Pattern | Type        | Deprecated | Definition                                  | Title/Description                                                    |
| ----------------------------------------------------------------------------- | ------- | ----------- | ---------- | ------------------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i4_implementation )           | No      | const       | No         | -                                           | ToolCallLLMWrapper                                                   |
| - [tool_message_prompt](#apu_anyOf_i0_llm_unit_anyOf_i4_tool_message_prompt ) | No      | string      | No         | -                                           | Tool Message Prompt                                                  |
| - [llm_unit](#apu_anyOf_i0_llm_unit_anyOf_i4_llm_unit )                       | No      | object      | No         | Same as [llm_unit](#apu_anyOf_i0_llm_unit ) | Overview of <class 'eidolon_ai_sdk.apu.llm_unit.LLMUnit'> components |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i4_model )                             | No      | Combination | No         | -                                           | -                                                                    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_implementation"></a>12.2.5.5.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ToolCallLLMWrapper

Specific value: `"ToolCallLLMWrapper"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_tool_message_prompt"></a>12.2.5.5.2. Property `tool_message_prompt`

**Title:** Tool Message Prompt

|              |                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Required** | No                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Default**  | `"You must follow these instructions:\nYou can select zero or more of the above tools based on the user query\nIf there are multiple tools required, make sure a list of tools are returned in a JSON array.\nIf there is no tool that match the user request or you have already answered the question, you will respond with empty json array for the tools.\nYou can also add any additional notes or explanations in the notes field."` |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_llm_unit"></a>12.2.5.5.3. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Same definition as**    | [llm_unit](#apu_anyOf_i0_llm_unit)                                        |

**Description:** Overview of <class 'eidolon_ai_sdk.apu.llm_unit.LLMUnit'> components

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_model"></a>12.2.5.5.4. Property `model`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                       |
| -------------------------------------------------------------------- |
| [LLMModel Reference](#apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i1)             |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0"></a>12.2.5.5.4.1. Property `LLMModel Reference`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.llm_unit.LLMModel"`                                  |

| Property                                                                           | Pattern | Type   | Deprecated | Definition | Title/Description |
| ---------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0_implementation"></a>12.2.5.5.4.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i1"></a>12.2.5.5.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i1_logic_units"></a>12.2.6. Property `logic_units`

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

##### <a name="autogenerated_heading_3"></a>12.2.6.1. LogicUnit Reference

**Title:** LogicUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.logic_unit.LogicUnit"`                               |

| Property                                                            | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i1_logic_units_items_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i1_logic_units_items_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i1_logic_units_items_implementation"></a>12.2.6.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i1_audio_unit"></a>12.2.7. Property `audio_unit`

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

##### <a name="apu_anyOf_i1_audio_unit_anyOf_i0"></a>12.2.7.1. Property `AudioUnit Reference`

**Title:** AudioUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.audio_unit.AudioUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i1_audio_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i1_audio_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i1_audio_unit_anyOf_i0_implementation"></a>12.2.7.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i1_audio_unit_anyOf_i1"></a>12.2.7.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i1_image_unit"></a>12.2.8. Property `image_unit`

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

##### <a name="apu_anyOf_i1_image_unit_anyOf_i0"></a>12.2.8.1. Property `ImageUnit Reference`

**Title:** ImageUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.image_unit.ImageUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i1_image_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i1_image_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i1_image_unit_anyOf_i0_implementation"></a>12.2.8.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i1_image_unit_anyOf_i1"></a>12.2.8.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i1_record_conversation"></a>12.2.9. Property `record_conversation`

**Title:** Record Conversation

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

#### <a name="apu_anyOf_i1_allow_tool_errors"></a>12.2.10. Property `allow_tool_errors`

**Title:** Allow Tool Errors

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

#### <a name="apu_anyOf_i1_document_processor"></a>12.2.11. Property `document_processor`

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

##### <a name="apu_anyOf_i1_document_processor_implementation"></a>12.2.11.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i1_retriever"></a>12.2.12. Property `retriever`

**Title:** Retriever Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"Retriever"`                                                             |

| Property                                                    | Pattern | Type   | Deprecated | Definition | Title/Description |
| ----------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i1_retriever_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i1_retriever_additionalProperties )         | No      | object | No         | -          | -                 |

##### <a name="apu_anyOf_i1_retriever_implementation"></a>12.2.12.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i1_retriever_apu"></a>12.2.13. Property `retriever_apu`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                        |
| ----------------------------------------------------- |
| [APU Reference](#apu_anyOf_i1_retriever_apu_anyOf_i0) |
| [item 1](#apu_anyOf_i1_retriever_apu_anyOf_i1)        |

##### <a name="apu_anyOf_i1_retriever_apu_anyOf_i0"></a>12.2.13.1. Property `APU Reference`

**Title:** APU Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.apu.APU"`                                            |

| Property                                                                 | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------ | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i1_retriever_apu_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i1_retriever_apu_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i1_retriever_apu_anyOf_i0_implementation"></a>12.2.13.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i1_retriever_apu_anyOf_i1"></a>12.2.13.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

### <a name="apu_anyOf_i2"></a>12.3. Property `ClaudeSonnet.json`

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
| - [llm_unit](#apu_anyOf_i2_llm_unit )                             | No      | object          | No         | In [LLMUnit](/docs/components/llmunit/overview) | Overview of <class 'eidolon_ai_sdk.apu.llm_unit.LLMUnit'> components |
| - [logic_units](#apu_anyOf_i2_logic_units )                       | No      | array of object | No         | -                                | Logic Units                                                          |
| - [audio_unit](#apu_anyOf_i2_audio_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [image_unit](#apu_anyOf_i2_image_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [record_conversation](#apu_anyOf_i2_record_conversation )       | No      | boolean         | No         | -                                | Record Conversation                                                  |
| - [allow_tool_errors](#apu_anyOf_i2_allow_tool_errors )           | No      | boolean         | No         | -                                | Allow Tool Errors                                                    |
| - [document_processor](#apu_anyOf_i2_document_processor )         | No      | object          | No         | -                                | DocumentProcessor Reference                                          |
| - [retriever](#apu_anyOf_i2_retriever )                           | No      | object          | No         | -                                | Retriever Reference                                                  |
| - [retriever_apu](#apu_anyOf_i2_retriever_apu )                   | No      | Combination     | No         | -                                | -                                                                    |

#### <a name="apu_anyOf_i2_implementation"></a>12.3.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ClaudeSonnet

Specific value: `"ClaudeSonnet"`

#### <a name="apu_anyOf_i2_max_num_function_calls"></a>12.3.2. Property `max_num_function_calls`

**Title:** Max Num Function Calls

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `10`      |

**Description:** The maximum number of function calls to make in a single request.

#### <a name="apu_anyOf_i2_io_unit"></a>12.3.3. Property `io_unit`

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

##### <a name="apu_anyOf_i2_io_unit_implementation"></a>12.3.3.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i2_memory_unit"></a>12.3.4. Property `memory_unit`

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

##### <a name="apu_anyOf_i2_memory_unit_implementation"></a>12.3.4.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i2_llm_unit"></a>12.3.5. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Defined in**            | [LLMUnit](/docs/components/llmunit/overview)                                             |

**Description:** Overview of <class 'eidolon_ai_sdk.apu.llm_unit.LLMUnit'> components

| Any of(Option)                                             |
| ---------------------------------------------------------- |
| [AnthropicLLMUnit.json](#apu_anyOf_i0_llm_unit_anyOf_i0)   |
| [MistralGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i1)         |
| [OllamaLLMUnit.json](#apu_anyOf_i0_llm_unit_anyOf_i2)      |
| [OpenAIGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i3)          |
| [ToolCallLLMWrapper.json](#apu_anyOf_i0_llm_unit_anyOf_i4) |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i0"></a>12.3.5.1. Property `AnthropicLLMUnit.json`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_implementation"></a>12.3.5.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AnthropicLLMUnit

Specific value: `"AnthropicLLMUnit"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model"></a>12.3.5.1.2. Property `model`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model_implementation"></a>12.3.5.1.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_temperature"></a>12.3.5.1.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens"></a>12.3.5.1.4. Property `max_tokens`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i0"></a>12.3.5.1.4.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i1"></a>12.3.5.1.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_client_args"></a>12.3.5.1.5. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i1"></a>12.3.5.2. Property `MistralGPT.json`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_implementation"></a>12.3.5.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** MistralGPT

Specific value: `"MistralGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model"></a>12.3.5.2.2. Property `model`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model_implementation"></a>12.3.5.2.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_temperature"></a>12.3.5.2.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_force_json"></a>12.3.5.2.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens"></a>12.3.5.2.5. Property `max_tokens`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i0"></a>12.3.5.2.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i1"></a>12.3.5.2.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_client_args"></a>12.3.5.2.6. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i2"></a>12.3.5.3. Property `OllamaLLMUnit.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./OllamaLLMUnit.json                                                 |

| Property                                                            | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_implementation ) | No      | const       | No         | -          | OllamaLLMUnit      |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i2_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i2_temperature )       | No      | number      | No         | -          | Temperature        |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i2_force_json )         | No      | boolean     | No         | -          | Force Json         |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_options](#apu_anyOf_i0_llm_unit_anyOf_i2_client_options ) | No      | object      | No         | -          | Client Options     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_implementation"></a>12.3.5.3.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OllamaLLMUnit

Specific value: `"OllamaLLMUnit"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model"></a>12.3.5.3.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"llama3"`                                                                |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i2_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation"></a>12.3.5.3.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_temperature"></a>12.3.5.3.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_force_json"></a>12.3.5.3.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens"></a>12.3.5.3.5. Property `max_tokens`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i0"></a>12.3.5.3.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i1"></a>12.3.5.3.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_client_options"></a>12.3.5.3.6. Property `client_options`

**Title:** Client Options

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i3"></a>12.3.5.4. Property `OpenAIGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./OpenAIGPT.json                                                     |

| Property                                                                    | Pattern | Type        | Deprecated | Definition | Title/Description                 |
| --------------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | --------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_implementation )         | No      | const       | No         | -          | OpenAIGPT                         |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i3_model )                           | No      | object      | No         | -          | LLMModel Reference                |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i3_temperature )               | No      | number      | No         | -          | Temperature                       |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i3_force_json )                 | No      | boolean     | No         | -          | Force Json                        |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens )                 | No      | Combination | No         | -          | Max Tokens                        |
| - [connection_handler](#apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler ) | No      | object      | No         | -          | OpenAIConnectionHandler Reference |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_implementation"></a>12.3.5.4.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OpenAIGPT

Specific value: `"OpenAIGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model"></a>12.3.5.4.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"gpt-4-turbo"`                                                           |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i3_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_implementation"></a>12.3.5.4.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_temperature"></a>12.3.5.4.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_force_json"></a>12.3.5.4.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens"></a>12.3.5.4.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens_anyOf_i0"></a>12.3.5.4.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens_anyOf_i1"></a>12.3.5.4.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler"></a>12.3.5.4.6. Property `connection_handler`

**Title:** OpenAIConnectionHandler Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"OpenAIConnectionHandler"`                                               |

| Property                                                                               | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler_implementation"></a>12.3.5.4.6.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i4"></a>12.3.5.5. Property `ToolCallLLMWrapper.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./ToolCallLLMWrapper.json                                            |

| Property                                                                      | Pattern | Type        | Deprecated | Definition                                  | Title/Description                                                    |
| ----------------------------------------------------------------------------- | ------- | ----------- | ---------- | ------------------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i4_implementation )           | No      | const       | No         | -                                           | ToolCallLLMWrapper                                                   |
| - [tool_message_prompt](#apu_anyOf_i0_llm_unit_anyOf_i4_tool_message_prompt ) | No      | string      | No         | -                                           | Tool Message Prompt                                                  |
| - [llm_unit](#apu_anyOf_i0_llm_unit_anyOf_i4_llm_unit )                       | No      | object      | No         | Same as [llm_unit](#apu_anyOf_i0_llm_unit ) | Overview of <class 'eidolon_ai_sdk.apu.llm_unit.LLMUnit'> components |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i4_model )                             | No      | Combination | No         | -                                           | -                                                                    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_implementation"></a>12.3.5.5.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ToolCallLLMWrapper

Specific value: `"ToolCallLLMWrapper"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_tool_message_prompt"></a>12.3.5.5.2. Property `tool_message_prompt`

**Title:** Tool Message Prompt

|              |                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Required** | No                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Default**  | `"You must follow these instructions:\nYou can select zero or more of the above tools based on the user query\nIf there are multiple tools required, make sure a list of tools are returned in a JSON array.\nIf there is no tool that match the user request or you have already answered the question, you will respond with empty json array for the tools.\nYou can also add any additional notes or explanations in the notes field."` |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_llm_unit"></a>12.3.5.5.3. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Same definition as**    | [llm_unit](#apu_anyOf_i0_llm_unit)                                        |

**Description:** Overview of <class 'eidolon_ai_sdk.apu.llm_unit.LLMUnit'> components

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_model"></a>12.3.5.5.4. Property `model`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                       |
| -------------------------------------------------------------------- |
| [LLMModel Reference](#apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i1)             |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0"></a>12.3.5.5.4.1. Property `LLMModel Reference`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.llm_unit.LLMModel"`                                  |

| Property                                                                           | Pattern | Type   | Deprecated | Definition | Title/Description |
| ---------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0_implementation"></a>12.3.5.5.4.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i1"></a>12.3.5.5.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i2_logic_units"></a>12.3.6. Property `logic_units`

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

##### <a name="autogenerated_heading_4"></a>12.3.6.1. LogicUnit Reference

**Title:** LogicUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.logic_unit.LogicUnit"`                               |

| Property                                                            | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i2_logic_units_items_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i2_logic_units_items_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i2_logic_units_items_implementation"></a>12.3.6.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i2_audio_unit"></a>12.3.7. Property `audio_unit`

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

##### <a name="apu_anyOf_i2_audio_unit_anyOf_i0"></a>12.3.7.1. Property `AudioUnit Reference`

**Title:** AudioUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.audio_unit.AudioUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i2_audio_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i2_audio_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i2_audio_unit_anyOf_i0_implementation"></a>12.3.7.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i2_audio_unit_anyOf_i1"></a>12.3.7.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i2_image_unit"></a>12.3.8. Property `image_unit`

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

##### <a name="apu_anyOf_i2_image_unit_anyOf_i0"></a>12.3.8.1. Property `ImageUnit Reference`

**Title:** ImageUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.image_unit.ImageUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i2_image_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i2_image_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i2_image_unit_anyOf_i0_implementation"></a>12.3.8.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i2_image_unit_anyOf_i1"></a>12.3.8.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i2_record_conversation"></a>12.3.9. Property `record_conversation`

**Title:** Record Conversation

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

#### <a name="apu_anyOf_i2_allow_tool_errors"></a>12.3.10. Property `allow_tool_errors`

**Title:** Allow Tool Errors

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

#### <a name="apu_anyOf_i2_document_processor"></a>12.3.11. Property `document_processor`

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

##### <a name="apu_anyOf_i2_document_processor_implementation"></a>12.3.11.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i2_retriever"></a>12.3.12. Property `retriever`

**Title:** Retriever Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"Retriever"`                                                             |

| Property                                                    | Pattern | Type   | Deprecated | Definition | Title/Description |
| ----------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i2_retriever_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i2_retriever_additionalProperties )         | No      | object | No         | -          | -                 |

##### <a name="apu_anyOf_i2_retriever_implementation"></a>12.3.12.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i2_retriever_apu"></a>12.3.13. Property `retriever_apu`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                        |
| ----------------------------------------------------- |
| [APU Reference](#apu_anyOf_i2_retriever_apu_anyOf_i0) |
| [item 1](#apu_anyOf_i2_retriever_apu_anyOf_i1)        |

##### <a name="apu_anyOf_i2_retriever_apu_anyOf_i0"></a>12.3.13.1. Property `APU Reference`

**Title:** APU Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.apu.APU"`                                            |

| Property                                                                 | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------ | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i2_retriever_apu_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i2_retriever_apu_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i2_retriever_apu_anyOf_i0_implementation"></a>12.3.13.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i2_retriever_apu_anyOf_i1"></a>12.3.13.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

### <a name="apu_anyOf_i3"></a>12.4. Property `ConversationalAPU.json`

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
| - [llm_unit](#apu_anyOf_i3_llm_unit )                             | No      | object          | No         | In [LLMUnit](/docs/components/llmunit/overview) | Overview of <class 'eidolon_ai_sdk.apu.llm_unit.LLMUnit'> components |
| - [logic_units](#apu_anyOf_i3_logic_units )                       | No      | array of object | No         | -                                | Logic Units                                                          |
| - [audio_unit](#apu_anyOf_i3_audio_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [image_unit](#apu_anyOf_i3_image_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [record_conversation](#apu_anyOf_i3_record_conversation )       | No      | boolean         | No         | -                                | Record Conversation                                                  |
| - [allow_tool_errors](#apu_anyOf_i3_allow_tool_errors )           | No      | boolean         | No         | -                                | Allow Tool Errors                                                    |
| - [document_processor](#apu_anyOf_i3_document_processor )         | No      | object          | No         | -                                | DocumentProcessor Reference                                          |
| - [retriever](#apu_anyOf_i3_retriever )                           | No      | object          | No         | -                                | Retriever Reference                                                  |
| - [retriever_apu](#apu_anyOf_i3_retriever_apu )                   | No      | Combination     | No         | -                                | -                                                                    |

#### <a name="apu_anyOf_i3_implementation"></a>12.4.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ConversationalAPU

Specific value: `"ConversationalAPU"`

#### <a name="apu_anyOf_i3_max_num_function_calls"></a>12.4.2. Property `max_num_function_calls`

**Title:** Max Num Function Calls

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `10`      |

**Description:** The maximum number of function calls to make in a single request.

#### <a name="apu_anyOf_i3_io_unit"></a>12.4.3. Property `io_unit`

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

##### <a name="apu_anyOf_i3_io_unit_implementation"></a>12.4.3.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i3_memory_unit"></a>12.4.4. Property `memory_unit`

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

##### <a name="apu_anyOf_i3_memory_unit_implementation"></a>12.4.4.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i3_llm_unit"></a>12.4.5. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Defined in**            | [LLMUnit](/docs/components/llmunit/overview)                                             |

**Description:** Overview of <class 'eidolon_ai_sdk.apu.llm_unit.LLMUnit'> components

| Any of(Option)                                             |
| ---------------------------------------------------------- |
| [AnthropicLLMUnit.json](#apu_anyOf_i0_llm_unit_anyOf_i0)   |
| [MistralGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i1)         |
| [OllamaLLMUnit.json](#apu_anyOf_i0_llm_unit_anyOf_i2)      |
| [OpenAIGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i3)          |
| [ToolCallLLMWrapper.json](#apu_anyOf_i0_llm_unit_anyOf_i4) |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i0"></a>12.4.5.1. Property `AnthropicLLMUnit.json`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_implementation"></a>12.4.5.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AnthropicLLMUnit

Specific value: `"AnthropicLLMUnit"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model"></a>12.4.5.1.2. Property `model`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model_implementation"></a>12.4.5.1.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_temperature"></a>12.4.5.1.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens"></a>12.4.5.1.4. Property `max_tokens`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i0"></a>12.4.5.1.4.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i1"></a>12.4.5.1.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_client_args"></a>12.4.5.1.5. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i1"></a>12.4.5.2. Property `MistralGPT.json`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_implementation"></a>12.4.5.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** MistralGPT

Specific value: `"MistralGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model"></a>12.4.5.2.2. Property `model`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model_implementation"></a>12.4.5.2.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_temperature"></a>12.4.5.2.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_force_json"></a>12.4.5.2.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens"></a>12.4.5.2.5. Property `max_tokens`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i0"></a>12.4.5.2.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i1"></a>12.4.5.2.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_client_args"></a>12.4.5.2.6. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i2"></a>12.4.5.3. Property `OllamaLLMUnit.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./OllamaLLMUnit.json                                                 |

| Property                                                            | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_implementation ) | No      | const       | No         | -          | OllamaLLMUnit      |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i2_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i2_temperature )       | No      | number      | No         | -          | Temperature        |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i2_force_json )         | No      | boolean     | No         | -          | Force Json         |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_options](#apu_anyOf_i0_llm_unit_anyOf_i2_client_options ) | No      | object      | No         | -          | Client Options     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_implementation"></a>12.4.5.3.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OllamaLLMUnit

Specific value: `"OllamaLLMUnit"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model"></a>12.4.5.3.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"llama3"`                                                                |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i2_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation"></a>12.4.5.3.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_temperature"></a>12.4.5.3.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_force_json"></a>12.4.5.3.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens"></a>12.4.5.3.5. Property `max_tokens`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i0"></a>12.4.5.3.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i1"></a>12.4.5.3.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_client_options"></a>12.4.5.3.6. Property `client_options`

**Title:** Client Options

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i3"></a>12.4.5.4. Property `OpenAIGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./OpenAIGPT.json                                                     |

| Property                                                                    | Pattern | Type        | Deprecated | Definition | Title/Description                 |
| --------------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | --------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_implementation )         | No      | const       | No         | -          | OpenAIGPT                         |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i3_model )                           | No      | object      | No         | -          | LLMModel Reference                |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i3_temperature )               | No      | number      | No         | -          | Temperature                       |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i3_force_json )                 | No      | boolean     | No         | -          | Force Json                        |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens )                 | No      | Combination | No         | -          | Max Tokens                        |
| - [connection_handler](#apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler ) | No      | object      | No         | -          | OpenAIConnectionHandler Reference |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_implementation"></a>12.4.5.4.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OpenAIGPT

Specific value: `"OpenAIGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model"></a>12.4.5.4.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"gpt-4-turbo"`                                                           |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i3_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_implementation"></a>12.4.5.4.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_temperature"></a>12.4.5.4.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_force_json"></a>12.4.5.4.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens"></a>12.4.5.4.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens_anyOf_i0"></a>12.4.5.4.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens_anyOf_i1"></a>12.4.5.4.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler"></a>12.4.5.4.6. Property `connection_handler`

**Title:** OpenAIConnectionHandler Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"OpenAIConnectionHandler"`                                               |

| Property                                                                               | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler_implementation"></a>12.4.5.4.6.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i4"></a>12.4.5.5. Property `ToolCallLLMWrapper.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./ToolCallLLMWrapper.json                                            |

| Property                                                                      | Pattern | Type        | Deprecated | Definition                                  | Title/Description                                                    |
| ----------------------------------------------------------------------------- | ------- | ----------- | ---------- | ------------------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i4_implementation )           | No      | const       | No         | -                                           | ToolCallLLMWrapper                                                   |
| - [tool_message_prompt](#apu_anyOf_i0_llm_unit_anyOf_i4_tool_message_prompt ) | No      | string      | No         | -                                           | Tool Message Prompt                                                  |
| - [llm_unit](#apu_anyOf_i0_llm_unit_anyOf_i4_llm_unit )                       | No      | object      | No         | Same as [llm_unit](#apu_anyOf_i0_llm_unit ) | Overview of <class 'eidolon_ai_sdk.apu.llm_unit.LLMUnit'> components |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i4_model )                             | No      | Combination | No         | -                                           | -                                                                    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_implementation"></a>12.4.5.5.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ToolCallLLMWrapper

Specific value: `"ToolCallLLMWrapper"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_tool_message_prompt"></a>12.4.5.5.2. Property `tool_message_prompt`

**Title:** Tool Message Prompt

|              |                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Required** | No                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Default**  | `"You must follow these instructions:\nYou can select zero or more of the above tools based on the user query\nIf there are multiple tools required, make sure a list of tools are returned in a JSON array.\nIf there is no tool that match the user request or you have already answered the question, you will respond with empty json array for the tools.\nYou can also add any additional notes or explanations in the notes field."` |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_llm_unit"></a>12.4.5.5.3. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Same definition as**    | [llm_unit](#apu_anyOf_i0_llm_unit)                                        |

**Description:** Overview of <class 'eidolon_ai_sdk.apu.llm_unit.LLMUnit'> components

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_model"></a>12.4.5.5.4. Property `model`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                       |
| -------------------------------------------------------------------- |
| [LLMModel Reference](#apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i1)             |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0"></a>12.4.5.5.4.1. Property `LLMModel Reference`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.llm_unit.LLMModel"`                                  |

| Property                                                                           | Pattern | Type   | Deprecated | Definition | Title/Description |
| ---------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0_implementation"></a>12.4.5.5.4.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i1"></a>12.4.5.5.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i3_logic_units"></a>12.4.6. Property `logic_units`

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

##### <a name="autogenerated_heading_5"></a>12.4.6.1. LogicUnit Reference

**Title:** LogicUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.logic_unit.LogicUnit"`                               |

| Property                                                            | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i3_logic_units_items_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i3_logic_units_items_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i3_logic_units_items_implementation"></a>12.4.6.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i3_audio_unit"></a>12.4.7. Property `audio_unit`

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

##### <a name="apu_anyOf_i3_audio_unit_anyOf_i0"></a>12.4.7.1. Property `AudioUnit Reference`

**Title:** AudioUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.audio_unit.AudioUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i3_audio_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i3_audio_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i3_audio_unit_anyOf_i0_implementation"></a>12.4.7.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i3_audio_unit_anyOf_i1"></a>12.4.7.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i3_image_unit"></a>12.4.8. Property `image_unit`

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

##### <a name="apu_anyOf_i3_image_unit_anyOf_i0"></a>12.4.8.1. Property `ImageUnit Reference`

**Title:** ImageUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.image_unit.ImageUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i3_image_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i3_image_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i3_image_unit_anyOf_i0_implementation"></a>12.4.8.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i3_image_unit_anyOf_i1"></a>12.4.8.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i3_record_conversation"></a>12.4.9. Property `record_conversation`

**Title:** Record Conversation

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

#### <a name="apu_anyOf_i3_allow_tool_errors"></a>12.4.10. Property `allow_tool_errors`

**Title:** Allow Tool Errors

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

#### <a name="apu_anyOf_i3_document_processor"></a>12.4.11. Property `document_processor`

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

##### <a name="apu_anyOf_i3_document_processor_implementation"></a>12.4.11.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i3_retriever"></a>12.4.12. Property `retriever`

**Title:** Retriever Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"Retriever"`                                                             |

| Property                                                    | Pattern | Type   | Deprecated | Definition | Title/Description |
| ----------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i3_retriever_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i3_retriever_additionalProperties )         | No      | object | No         | -          | -                 |

##### <a name="apu_anyOf_i3_retriever_implementation"></a>12.4.12.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i3_retriever_apu"></a>12.4.13. Property `retriever_apu`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                        |
| ----------------------------------------------------- |
| [APU Reference](#apu_anyOf_i3_retriever_apu_anyOf_i0) |
| [item 1](#apu_anyOf_i3_retriever_apu_anyOf_i1)        |

##### <a name="apu_anyOf_i3_retriever_apu_anyOf_i0"></a>12.4.13.1. Property `APU Reference`

**Title:** APU Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.apu.APU"`                                            |

| Property                                                                 | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------ | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i3_retriever_apu_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i3_retriever_apu_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i3_retriever_apu_anyOf_i0_implementation"></a>12.4.13.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i3_retriever_apu_anyOf_i1"></a>12.4.13.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

### <a name="apu_anyOf_i4"></a>12.5. Property `GPT3.5-turbo.json`

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
| - [llm_unit](#apu_anyOf_i4_llm_unit )                             | No      | object          | No         | In [LLMUnit](/docs/components/llmunit/overview) | Overview of <class 'eidolon_ai_sdk.apu.llm_unit.LLMUnit'> components |
| - [logic_units](#apu_anyOf_i4_logic_units )                       | No      | array of object | No         | -                                | Logic Units                                                          |
| - [audio_unit](#apu_anyOf_i4_audio_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [image_unit](#apu_anyOf_i4_image_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [record_conversation](#apu_anyOf_i4_record_conversation )       | No      | boolean         | No         | -                                | Record Conversation                                                  |
| - [allow_tool_errors](#apu_anyOf_i4_allow_tool_errors )           | No      | boolean         | No         | -                                | Allow Tool Errors                                                    |
| - [document_processor](#apu_anyOf_i4_document_processor )         | No      | object          | No         | -                                | DocumentProcessor Reference                                          |
| - [retriever](#apu_anyOf_i4_retriever )                           | No      | object          | No         | -                                | Retriever Reference                                                  |
| - [retriever_apu](#apu_anyOf_i4_retriever_apu )                   | No      | Combination     | No         | -                                | -                                                                    |

#### <a name="apu_anyOf_i4_implementation"></a>12.5.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** GPT3.5-turbo

Specific value: `"GPT3.5-turbo"`

#### <a name="apu_anyOf_i4_max_num_function_calls"></a>12.5.2. Property `max_num_function_calls`

**Title:** Max Num Function Calls

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `10`      |

**Description:** The maximum number of function calls to make in a single request.

#### <a name="apu_anyOf_i4_io_unit"></a>12.5.3. Property `io_unit`

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

##### <a name="apu_anyOf_i4_io_unit_implementation"></a>12.5.3.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i4_memory_unit"></a>12.5.4. Property `memory_unit`

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

##### <a name="apu_anyOf_i4_memory_unit_implementation"></a>12.5.4.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i4_llm_unit"></a>12.5.5. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Defined in**            | [LLMUnit](/docs/components/llmunit/overview)                                             |

**Description:** Overview of <class 'eidolon_ai_sdk.apu.llm_unit.LLMUnit'> components

| Any of(Option)                                             |
| ---------------------------------------------------------- |
| [AnthropicLLMUnit.json](#apu_anyOf_i0_llm_unit_anyOf_i0)   |
| [MistralGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i1)         |
| [OllamaLLMUnit.json](#apu_anyOf_i0_llm_unit_anyOf_i2)      |
| [OpenAIGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i3)          |
| [ToolCallLLMWrapper.json](#apu_anyOf_i0_llm_unit_anyOf_i4) |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i0"></a>12.5.5.1. Property `AnthropicLLMUnit.json`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_implementation"></a>12.5.5.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AnthropicLLMUnit

Specific value: `"AnthropicLLMUnit"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model"></a>12.5.5.1.2. Property `model`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model_implementation"></a>12.5.5.1.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_temperature"></a>12.5.5.1.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens"></a>12.5.5.1.4. Property `max_tokens`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i0"></a>12.5.5.1.4.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i1"></a>12.5.5.1.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_client_args"></a>12.5.5.1.5. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i1"></a>12.5.5.2. Property `MistralGPT.json`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_implementation"></a>12.5.5.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** MistralGPT

Specific value: `"MistralGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model"></a>12.5.5.2.2. Property `model`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model_implementation"></a>12.5.5.2.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_temperature"></a>12.5.5.2.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_force_json"></a>12.5.5.2.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens"></a>12.5.5.2.5. Property `max_tokens`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i0"></a>12.5.5.2.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i1"></a>12.5.5.2.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_client_args"></a>12.5.5.2.6. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i2"></a>12.5.5.3. Property `OllamaLLMUnit.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./OllamaLLMUnit.json                                                 |

| Property                                                            | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_implementation ) | No      | const       | No         | -          | OllamaLLMUnit      |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i2_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i2_temperature )       | No      | number      | No         | -          | Temperature        |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i2_force_json )         | No      | boolean     | No         | -          | Force Json         |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_options](#apu_anyOf_i0_llm_unit_anyOf_i2_client_options ) | No      | object      | No         | -          | Client Options     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_implementation"></a>12.5.5.3.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OllamaLLMUnit

Specific value: `"OllamaLLMUnit"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model"></a>12.5.5.3.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"llama3"`                                                                |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i2_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation"></a>12.5.5.3.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_temperature"></a>12.5.5.3.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_force_json"></a>12.5.5.3.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens"></a>12.5.5.3.5. Property `max_tokens`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i0"></a>12.5.5.3.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i1"></a>12.5.5.3.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_client_options"></a>12.5.5.3.6. Property `client_options`

**Title:** Client Options

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i3"></a>12.5.5.4. Property `OpenAIGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./OpenAIGPT.json                                                     |

| Property                                                                    | Pattern | Type        | Deprecated | Definition | Title/Description                 |
| --------------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | --------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_implementation )         | No      | const       | No         | -          | OpenAIGPT                         |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i3_model )                           | No      | object      | No         | -          | LLMModel Reference                |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i3_temperature )               | No      | number      | No         | -          | Temperature                       |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i3_force_json )                 | No      | boolean     | No         | -          | Force Json                        |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens )                 | No      | Combination | No         | -          | Max Tokens                        |
| - [connection_handler](#apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler ) | No      | object      | No         | -          | OpenAIConnectionHandler Reference |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_implementation"></a>12.5.5.4.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OpenAIGPT

Specific value: `"OpenAIGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model"></a>12.5.5.4.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"gpt-4-turbo"`                                                           |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i3_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_implementation"></a>12.5.5.4.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_temperature"></a>12.5.5.4.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_force_json"></a>12.5.5.4.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens"></a>12.5.5.4.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens_anyOf_i0"></a>12.5.5.4.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens_anyOf_i1"></a>12.5.5.4.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler"></a>12.5.5.4.6. Property `connection_handler`

**Title:** OpenAIConnectionHandler Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"OpenAIConnectionHandler"`                                               |

| Property                                                                               | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler_implementation"></a>12.5.5.4.6.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i4"></a>12.5.5.5. Property `ToolCallLLMWrapper.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./ToolCallLLMWrapper.json                                            |

| Property                                                                      | Pattern | Type        | Deprecated | Definition                                  | Title/Description                                                    |
| ----------------------------------------------------------------------------- | ------- | ----------- | ---------- | ------------------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i4_implementation )           | No      | const       | No         | -                                           | ToolCallLLMWrapper                                                   |
| - [tool_message_prompt](#apu_anyOf_i0_llm_unit_anyOf_i4_tool_message_prompt ) | No      | string      | No         | -                                           | Tool Message Prompt                                                  |
| - [llm_unit](#apu_anyOf_i0_llm_unit_anyOf_i4_llm_unit )                       | No      | object      | No         | Same as [llm_unit](#apu_anyOf_i0_llm_unit ) | Overview of <class 'eidolon_ai_sdk.apu.llm_unit.LLMUnit'> components |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i4_model )                             | No      | Combination | No         | -                                           | -                                                                    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_implementation"></a>12.5.5.5.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ToolCallLLMWrapper

Specific value: `"ToolCallLLMWrapper"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_tool_message_prompt"></a>12.5.5.5.2. Property `tool_message_prompt`

**Title:** Tool Message Prompt

|              |                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Required** | No                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Default**  | `"You must follow these instructions:\nYou can select zero or more of the above tools based on the user query\nIf there are multiple tools required, make sure a list of tools are returned in a JSON array.\nIf there is no tool that match the user request or you have already answered the question, you will respond with empty json array for the tools.\nYou can also add any additional notes or explanations in the notes field."` |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_llm_unit"></a>12.5.5.5.3. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Same definition as**    | [llm_unit](#apu_anyOf_i0_llm_unit)                                        |

**Description:** Overview of <class 'eidolon_ai_sdk.apu.llm_unit.LLMUnit'> components

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_model"></a>12.5.5.5.4. Property `model`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                       |
| -------------------------------------------------------------------- |
| [LLMModel Reference](#apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i1)             |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0"></a>12.5.5.5.4.1. Property `LLMModel Reference`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.llm_unit.LLMModel"`                                  |

| Property                                                                           | Pattern | Type   | Deprecated | Definition | Title/Description |
| ---------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0_implementation"></a>12.5.5.5.4.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i1"></a>12.5.5.5.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i4_logic_units"></a>12.5.6. Property `logic_units`

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

##### <a name="autogenerated_heading_6"></a>12.5.6.1. LogicUnit Reference

**Title:** LogicUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.logic_unit.LogicUnit"`                               |

| Property                                                            | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i4_logic_units_items_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i4_logic_units_items_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i4_logic_units_items_implementation"></a>12.5.6.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i4_audio_unit"></a>12.5.7. Property `audio_unit`

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

##### <a name="apu_anyOf_i4_audio_unit_anyOf_i0"></a>12.5.7.1. Property `AudioUnit Reference`

**Title:** AudioUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.audio_unit.AudioUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i4_audio_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i4_audio_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i4_audio_unit_anyOf_i0_implementation"></a>12.5.7.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i4_audio_unit_anyOf_i1"></a>12.5.7.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i4_image_unit"></a>12.5.8. Property `image_unit`

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

##### <a name="apu_anyOf_i4_image_unit_anyOf_i0"></a>12.5.8.1. Property `ImageUnit Reference`

**Title:** ImageUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.image_unit.ImageUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i4_image_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i4_image_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i4_image_unit_anyOf_i0_implementation"></a>12.5.8.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i4_image_unit_anyOf_i1"></a>12.5.8.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i4_record_conversation"></a>12.5.9. Property `record_conversation`

**Title:** Record Conversation

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

#### <a name="apu_anyOf_i4_allow_tool_errors"></a>12.5.10. Property `allow_tool_errors`

**Title:** Allow Tool Errors

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

#### <a name="apu_anyOf_i4_document_processor"></a>12.5.11. Property `document_processor`

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

##### <a name="apu_anyOf_i4_document_processor_implementation"></a>12.5.11.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i4_retriever"></a>12.5.12. Property `retriever`

**Title:** Retriever Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"Retriever"`                                                             |

| Property                                                    | Pattern | Type   | Deprecated | Definition | Title/Description |
| ----------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i4_retriever_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i4_retriever_additionalProperties )         | No      | object | No         | -          | -                 |

##### <a name="apu_anyOf_i4_retriever_implementation"></a>12.5.12.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i4_retriever_apu"></a>12.5.13. Property `retriever_apu`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                        |
| ----------------------------------------------------- |
| [APU Reference](#apu_anyOf_i4_retriever_apu_anyOf_i0) |
| [item 1](#apu_anyOf_i4_retriever_apu_anyOf_i1)        |

##### <a name="apu_anyOf_i4_retriever_apu_anyOf_i0"></a>12.5.13.1. Property `APU Reference`

**Title:** APU Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.apu.APU"`                                            |

| Property                                                                 | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------ | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i4_retriever_apu_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i4_retriever_apu_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i4_retriever_apu_anyOf_i0_implementation"></a>12.5.13.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i4_retriever_apu_anyOf_i1"></a>12.5.13.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

### <a name="apu_anyOf_i5"></a>12.6. Property `GPT4-turbo.json`

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
| - [llm_unit](#apu_anyOf_i5_llm_unit )                             | No      | object          | No         | In [LLMUnit](/docs/components/llmunit/overview) | Overview of <class 'eidolon_ai_sdk.apu.llm_unit.LLMUnit'> components |
| - [logic_units](#apu_anyOf_i5_logic_units )                       | No      | array of object | No         | -                                | Logic Units                                                          |
| - [audio_unit](#apu_anyOf_i5_audio_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [image_unit](#apu_anyOf_i5_image_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [record_conversation](#apu_anyOf_i5_record_conversation )       | No      | boolean         | No         | -                                | Record Conversation                                                  |
| - [allow_tool_errors](#apu_anyOf_i5_allow_tool_errors )           | No      | boolean         | No         | -                                | Allow Tool Errors                                                    |
| - [document_processor](#apu_anyOf_i5_document_processor )         | No      | object          | No         | -                                | DocumentProcessor Reference                                          |
| - [retriever](#apu_anyOf_i5_retriever )                           | No      | object          | No         | -                                | Retriever Reference                                                  |
| - [retriever_apu](#apu_anyOf_i5_retriever_apu )                   | No      | Combination     | No         | -                                | -                                                                    |

#### <a name="apu_anyOf_i5_implementation"></a>12.6.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** GPT4-turbo

Specific value: `"GPT4-turbo"`

#### <a name="apu_anyOf_i5_max_num_function_calls"></a>12.6.2. Property `max_num_function_calls`

**Title:** Max Num Function Calls

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `10`      |

**Description:** The maximum number of function calls to make in a single request.

#### <a name="apu_anyOf_i5_io_unit"></a>12.6.3. Property `io_unit`

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

##### <a name="apu_anyOf_i5_io_unit_implementation"></a>12.6.3.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i5_memory_unit"></a>12.6.4. Property `memory_unit`

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

##### <a name="apu_anyOf_i5_memory_unit_implementation"></a>12.6.4.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i5_llm_unit"></a>12.6.5. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Defined in**            | [LLMUnit](/docs/components/llmunit/overview)                                             |

**Description:** Overview of <class 'eidolon_ai_sdk.apu.llm_unit.LLMUnit'> components

| Any of(Option)                                             |
| ---------------------------------------------------------- |
| [AnthropicLLMUnit.json](#apu_anyOf_i0_llm_unit_anyOf_i0)   |
| [MistralGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i1)         |
| [OllamaLLMUnit.json](#apu_anyOf_i0_llm_unit_anyOf_i2)      |
| [OpenAIGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i3)          |
| [ToolCallLLMWrapper.json](#apu_anyOf_i0_llm_unit_anyOf_i4) |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i0"></a>12.6.5.1. Property `AnthropicLLMUnit.json`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_implementation"></a>12.6.5.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AnthropicLLMUnit

Specific value: `"AnthropicLLMUnit"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model"></a>12.6.5.1.2. Property `model`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model_implementation"></a>12.6.5.1.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_temperature"></a>12.6.5.1.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens"></a>12.6.5.1.4. Property `max_tokens`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i0"></a>12.6.5.1.4.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i1"></a>12.6.5.1.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_client_args"></a>12.6.5.1.5. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i1"></a>12.6.5.2. Property `MistralGPT.json`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_implementation"></a>12.6.5.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** MistralGPT

Specific value: `"MistralGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model"></a>12.6.5.2.2. Property `model`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model_implementation"></a>12.6.5.2.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_temperature"></a>12.6.5.2.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_force_json"></a>12.6.5.2.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens"></a>12.6.5.2.5. Property `max_tokens`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i0"></a>12.6.5.2.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i1"></a>12.6.5.2.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_client_args"></a>12.6.5.2.6. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i2"></a>12.6.5.3. Property `OllamaLLMUnit.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./OllamaLLMUnit.json                                                 |

| Property                                                            | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_implementation ) | No      | const       | No         | -          | OllamaLLMUnit      |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i2_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i2_temperature )       | No      | number      | No         | -          | Temperature        |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i2_force_json )         | No      | boolean     | No         | -          | Force Json         |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_options](#apu_anyOf_i0_llm_unit_anyOf_i2_client_options ) | No      | object      | No         | -          | Client Options     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_implementation"></a>12.6.5.3.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OllamaLLMUnit

Specific value: `"OllamaLLMUnit"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model"></a>12.6.5.3.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"llama3"`                                                                |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i2_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation"></a>12.6.5.3.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_temperature"></a>12.6.5.3.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_force_json"></a>12.6.5.3.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens"></a>12.6.5.3.5. Property `max_tokens`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i0"></a>12.6.5.3.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i1"></a>12.6.5.3.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_client_options"></a>12.6.5.3.6. Property `client_options`

**Title:** Client Options

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i3"></a>12.6.5.4. Property `OpenAIGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./OpenAIGPT.json                                                     |

| Property                                                                    | Pattern | Type        | Deprecated | Definition | Title/Description                 |
| --------------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | --------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_implementation )         | No      | const       | No         | -          | OpenAIGPT                         |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i3_model )                           | No      | object      | No         | -          | LLMModel Reference                |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i3_temperature )               | No      | number      | No         | -          | Temperature                       |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i3_force_json )                 | No      | boolean     | No         | -          | Force Json                        |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens )                 | No      | Combination | No         | -          | Max Tokens                        |
| - [connection_handler](#apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler ) | No      | object      | No         | -          | OpenAIConnectionHandler Reference |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_implementation"></a>12.6.5.4.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OpenAIGPT

Specific value: `"OpenAIGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model"></a>12.6.5.4.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"gpt-4-turbo"`                                                           |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i3_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_implementation"></a>12.6.5.4.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_temperature"></a>12.6.5.4.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_force_json"></a>12.6.5.4.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens"></a>12.6.5.4.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens_anyOf_i0"></a>12.6.5.4.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens_anyOf_i1"></a>12.6.5.4.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler"></a>12.6.5.4.6. Property `connection_handler`

**Title:** OpenAIConnectionHandler Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"OpenAIConnectionHandler"`                                               |

| Property                                                                               | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler_implementation"></a>12.6.5.4.6.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i4"></a>12.6.5.5. Property `ToolCallLLMWrapper.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./ToolCallLLMWrapper.json                                            |

| Property                                                                      | Pattern | Type        | Deprecated | Definition                                  | Title/Description                                                    |
| ----------------------------------------------------------------------------- | ------- | ----------- | ---------- | ------------------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i4_implementation )           | No      | const       | No         | -                                           | ToolCallLLMWrapper                                                   |
| - [tool_message_prompt](#apu_anyOf_i0_llm_unit_anyOf_i4_tool_message_prompt ) | No      | string      | No         | -                                           | Tool Message Prompt                                                  |
| - [llm_unit](#apu_anyOf_i0_llm_unit_anyOf_i4_llm_unit )                       | No      | object      | No         | Same as [llm_unit](#apu_anyOf_i0_llm_unit ) | Overview of <class 'eidolon_ai_sdk.apu.llm_unit.LLMUnit'> components |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i4_model )                             | No      | Combination | No         | -                                           | -                                                                    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_implementation"></a>12.6.5.5.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ToolCallLLMWrapper

Specific value: `"ToolCallLLMWrapper"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_tool_message_prompt"></a>12.6.5.5.2. Property `tool_message_prompt`

**Title:** Tool Message Prompt

|              |                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Required** | No                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Default**  | `"You must follow these instructions:\nYou can select zero or more of the above tools based on the user query\nIf there are multiple tools required, make sure a list of tools are returned in a JSON array.\nIf there is no tool that match the user request or you have already answered the question, you will respond with empty json array for the tools.\nYou can also add any additional notes or explanations in the notes field."` |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_llm_unit"></a>12.6.5.5.3. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Same definition as**    | [llm_unit](#apu_anyOf_i0_llm_unit)                                        |

**Description:** Overview of <class 'eidolon_ai_sdk.apu.llm_unit.LLMUnit'> components

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_model"></a>12.6.5.5.4. Property `model`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                       |
| -------------------------------------------------------------------- |
| [LLMModel Reference](#apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i1)             |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0"></a>12.6.5.5.4.1. Property `LLMModel Reference`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.llm_unit.LLMModel"`                                  |

| Property                                                                           | Pattern | Type   | Deprecated | Definition | Title/Description |
| ---------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0_implementation"></a>12.6.5.5.4.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i1"></a>12.6.5.5.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i5_logic_units"></a>12.6.6. Property `logic_units`

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

##### <a name="autogenerated_heading_7"></a>12.6.6.1. LogicUnit Reference

**Title:** LogicUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.logic_unit.LogicUnit"`                               |

| Property                                                            | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i5_logic_units_items_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i5_logic_units_items_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i5_logic_units_items_implementation"></a>12.6.6.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i5_audio_unit"></a>12.6.7. Property `audio_unit`

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

##### <a name="apu_anyOf_i5_audio_unit_anyOf_i0"></a>12.6.7.1. Property `AudioUnit Reference`

**Title:** AudioUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.audio_unit.AudioUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i5_audio_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i5_audio_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i5_audio_unit_anyOf_i0_implementation"></a>12.6.7.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i5_audio_unit_anyOf_i1"></a>12.6.7.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i5_image_unit"></a>12.6.8. Property `image_unit`

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

##### <a name="apu_anyOf_i5_image_unit_anyOf_i0"></a>12.6.8.1. Property `ImageUnit Reference`

**Title:** ImageUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.image_unit.ImageUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i5_image_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i5_image_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i5_image_unit_anyOf_i0_implementation"></a>12.6.8.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i5_image_unit_anyOf_i1"></a>12.6.8.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i5_record_conversation"></a>12.6.9. Property `record_conversation`

**Title:** Record Conversation

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

#### <a name="apu_anyOf_i5_allow_tool_errors"></a>12.6.10. Property `allow_tool_errors`

**Title:** Allow Tool Errors

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

#### <a name="apu_anyOf_i5_document_processor"></a>12.6.11. Property `document_processor`

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

##### <a name="apu_anyOf_i5_document_processor_implementation"></a>12.6.11.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i5_retriever"></a>12.6.12. Property `retriever`

**Title:** Retriever Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"Retriever"`                                                             |

| Property                                                    | Pattern | Type   | Deprecated | Definition | Title/Description |
| ----------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i5_retriever_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i5_retriever_additionalProperties )         | No      | object | No         | -          | -                 |

##### <a name="apu_anyOf_i5_retriever_implementation"></a>12.6.12.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i5_retriever_apu"></a>12.6.13. Property `retriever_apu`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                        |
| ----------------------------------------------------- |
| [APU Reference](#apu_anyOf_i5_retriever_apu_anyOf_i0) |
| [item 1](#apu_anyOf_i5_retriever_apu_anyOf_i1)        |

##### <a name="apu_anyOf_i5_retriever_apu_anyOf_i0"></a>12.6.13.1. Property `APU Reference`

**Title:** APU Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.apu.APU"`                                            |

| Property                                                                 | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------ | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i5_retriever_apu_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i5_retriever_apu_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i5_retriever_apu_anyOf_i0_implementation"></a>12.6.13.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i5_retriever_apu_anyOf_i1"></a>12.6.13.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

### <a name="apu_anyOf_i6"></a>12.7. Property `GPT4o.json`

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
| - [llm_unit](#apu_anyOf_i6_llm_unit )                             | No      | object          | No         | In [LLMUnit](/docs/components/llmunit/overview) | Overview of <class 'eidolon_ai_sdk.apu.llm_unit.LLMUnit'> components |
| - [logic_units](#apu_anyOf_i6_logic_units )                       | No      | array of object | No         | -                                | Logic Units                                                          |
| - [audio_unit](#apu_anyOf_i6_audio_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [image_unit](#apu_anyOf_i6_image_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [record_conversation](#apu_anyOf_i6_record_conversation )       | No      | boolean         | No         | -                                | Record Conversation                                                  |
| - [allow_tool_errors](#apu_anyOf_i6_allow_tool_errors )           | No      | boolean         | No         | -                                | Allow Tool Errors                                                    |
| - [document_processor](#apu_anyOf_i6_document_processor )         | No      | object          | No         | -                                | DocumentProcessor Reference                                          |
| - [retriever](#apu_anyOf_i6_retriever )                           | No      | object          | No         | -                                | Retriever Reference                                                  |
| - [retriever_apu](#apu_anyOf_i6_retriever_apu )                   | No      | Combination     | No         | -                                | -                                                                    |

#### <a name="apu_anyOf_i6_implementation"></a>12.7.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** GPT4o

Specific value: `"GPT4o"`

#### <a name="apu_anyOf_i6_max_num_function_calls"></a>12.7.2. Property `max_num_function_calls`

**Title:** Max Num Function Calls

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `10`      |

**Description:** The maximum number of function calls to make in a single request.

#### <a name="apu_anyOf_i6_io_unit"></a>12.7.3. Property `io_unit`

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

##### <a name="apu_anyOf_i6_io_unit_implementation"></a>12.7.3.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i6_memory_unit"></a>12.7.4. Property `memory_unit`

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

##### <a name="apu_anyOf_i6_memory_unit_implementation"></a>12.7.4.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i6_llm_unit"></a>12.7.5. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Defined in**            | [LLMUnit](/docs/components/llmunit/overview)                                             |

**Description:** Overview of <class 'eidolon_ai_sdk.apu.llm_unit.LLMUnit'> components

| Any of(Option)                                             |
| ---------------------------------------------------------- |
| [AnthropicLLMUnit.json](#apu_anyOf_i0_llm_unit_anyOf_i0)   |
| [MistralGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i1)         |
| [OllamaLLMUnit.json](#apu_anyOf_i0_llm_unit_anyOf_i2)      |
| [OpenAIGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i3)          |
| [ToolCallLLMWrapper.json](#apu_anyOf_i0_llm_unit_anyOf_i4) |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i0"></a>12.7.5.1. Property `AnthropicLLMUnit.json`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_implementation"></a>12.7.5.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AnthropicLLMUnit

Specific value: `"AnthropicLLMUnit"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model"></a>12.7.5.1.2. Property `model`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model_implementation"></a>12.7.5.1.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_temperature"></a>12.7.5.1.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens"></a>12.7.5.1.4. Property `max_tokens`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i0"></a>12.7.5.1.4.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i1"></a>12.7.5.1.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_client_args"></a>12.7.5.1.5. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i1"></a>12.7.5.2. Property `MistralGPT.json`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_implementation"></a>12.7.5.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** MistralGPT

Specific value: `"MistralGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model"></a>12.7.5.2.2. Property `model`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model_implementation"></a>12.7.5.2.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_temperature"></a>12.7.5.2.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_force_json"></a>12.7.5.2.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens"></a>12.7.5.2.5. Property `max_tokens`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i0"></a>12.7.5.2.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i1"></a>12.7.5.2.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_client_args"></a>12.7.5.2.6. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i2"></a>12.7.5.3. Property `OllamaLLMUnit.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./OllamaLLMUnit.json                                                 |

| Property                                                            | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_implementation ) | No      | const       | No         | -          | OllamaLLMUnit      |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i2_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i2_temperature )       | No      | number      | No         | -          | Temperature        |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i2_force_json )         | No      | boolean     | No         | -          | Force Json         |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_options](#apu_anyOf_i0_llm_unit_anyOf_i2_client_options ) | No      | object      | No         | -          | Client Options     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_implementation"></a>12.7.5.3.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OllamaLLMUnit

Specific value: `"OllamaLLMUnit"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model"></a>12.7.5.3.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"llama3"`                                                                |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i2_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation"></a>12.7.5.3.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_temperature"></a>12.7.5.3.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_force_json"></a>12.7.5.3.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens"></a>12.7.5.3.5. Property `max_tokens`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i0"></a>12.7.5.3.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i1"></a>12.7.5.3.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_client_options"></a>12.7.5.3.6. Property `client_options`

**Title:** Client Options

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i3"></a>12.7.5.4. Property `OpenAIGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./OpenAIGPT.json                                                     |

| Property                                                                    | Pattern | Type        | Deprecated | Definition | Title/Description                 |
| --------------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | --------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_implementation )         | No      | const       | No         | -          | OpenAIGPT                         |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i3_model )                           | No      | object      | No         | -          | LLMModel Reference                |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i3_temperature )               | No      | number      | No         | -          | Temperature                       |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i3_force_json )                 | No      | boolean     | No         | -          | Force Json                        |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens )                 | No      | Combination | No         | -          | Max Tokens                        |
| - [connection_handler](#apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler ) | No      | object      | No         | -          | OpenAIConnectionHandler Reference |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_implementation"></a>12.7.5.4.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OpenAIGPT

Specific value: `"OpenAIGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model"></a>12.7.5.4.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"gpt-4-turbo"`                                                           |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i3_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_implementation"></a>12.7.5.4.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_temperature"></a>12.7.5.4.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_force_json"></a>12.7.5.4.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens"></a>12.7.5.4.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens_anyOf_i0"></a>12.7.5.4.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens_anyOf_i1"></a>12.7.5.4.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler"></a>12.7.5.4.6. Property `connection_handler`

**Title:** OpenAIConnectionHandler Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"OpenAIConnectionHandler"`                                               |

| Property                                                                               | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler_implementation"></a>12.7.5.4.6.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i4"></a>12.7.5.5. Property `ToolCallLLMWrapper.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./ToolCallLLMWrapper.json                                            |

| Property                                                                      | Pattern | Type        | Deprecated | Definition                                  | Title/Description                                                    |
| ----------------------------------------------------------------------------- | ------- | ----------- | ---------- | ------------------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i4_implementation )           | No      | const       | No         | -                                           | ToolCallLLMWrapper                                                   |
| - [tool_message_prompt](#apu_anyOf_i0_llm_unit_anyOf_i4_tool_message_prompt ) | No      | string      | No         | -                                           | Tool Message Prompt                                                  |
| - [llm_unit](#apu_anyOf_i0_llm_unit_anyOf_i4_llm_unit )                       | No      | object      | No         | Same as [llm_unit](#apu_anyOf_i0_llm_unit ) | Overview of <class 'eidolon_ai_sdk.apu.llm_unit.LLMUnit'> components |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i4_model )                             | No      | Combination | No         | -                                           | -                                                                    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_implementation"></a>12.7.5.5.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ToolCallLLMWrapper

Specific value: `"ToolCallLLMWrapper"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_tool_message_prompt"></a>12.7.5.5.2. Property `tool_message_prompt`

**Title:** Tool Message Prompt

|              |                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Required** | No                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Default**  | `"You must follow these instructions:\nYou can select zero or more of the above tools based on the user query\nIf there are multiple tools required, make sure a list of tools are returned in a JSON array.\nIf there is no tool that match the user request or you have already answered the question, you will respond with empty json array for the tools.\nYou can also add any additional notes or explanations in the notes field."` |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_llm_unit"></a>12.7.5.5.3. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Same definition as**    | [llm_unit](#apu_anyOf_i0_llm_unit)                                        |

**Description:** Overview of <class 'eidolon_ai_sdk.apu.llm_unit.LLMUnit'> components

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_model"></a>12.7.5.5.4. Property `model`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                       |
| -------------------------------------------------------------------- |
| [LLMModel Reference](#apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i1)             |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0"></a>12.7.5.5.4.1. Property `LLMModel Reference`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.llm_unit.LLMModel"`                                  |

| Property                                                                           | Pattern | Type   | Deprecated | Definition | Title/Description |
| ---------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0_implementation"></a>12.7.5.5.4.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i1"></a>12.7.5.5.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i6_logic_units"></a>12.7.6. Property `logic_units`

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

##### <a name="autogenerated_heading_8"></a>12.7.6.1. LogicUnit Reference

**Title:** LogicUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.logic_unit.LogicUnit"`                               |

| Property                                                            | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i6_logic_units_items_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i6_logic_units_items_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i6_logic_units_items_implementation"></a>12.7.6.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i6_audio_unit"></a>12.7.7. Property `audio_unit`

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

##### <a name="apu_anyOf_i6_audio_unit_anyOf_i0"></a>12.7.7.1. Property `AudioUnit Reference`

**Title:** AudioUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.audio_unit.AudioUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i6_audio_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i6_audio_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i6_audio_unit_anyOf_i0_implementation"></a>12.7.7.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i6_audio_unit_anyOf_i1"></a>12.7.7.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i6_image_unit"></a>12.7.8. Property `image_unit`

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

##### <a name="apu_anyOf_i6_image_unit_anyOf_i0"></a>12.7.8.1. Property `ImageUnit Reference`

**Title:** ImageUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.image_unit.ImageUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i6_image_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i6_image_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i6_image_unit_anyOf_i0_implementation"></a>12.7.8.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i6_image_unit_anyOf_i1"></a>12.7.8.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i6_record_conversation"></a>12.7.9. Property `record_conversation`

**Title:** Record Conversation

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

#### <a name="apu_anyOf_i6_allow_tool_errors"></a>12.7.10. Property `allow_tool_errors`

**Title:** Allow Tool Errors

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

#### <a name="apu_anyOf_i6_document_processor"></a>12.7.11. Property `document_processor`

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

##### <a name="apu_anyOf_i6_document_processor_implementation"></a>12.7.11.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i6_retriever"></a>12.7.12. Property `retriever`

**Title:** Retriever Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"Retriever"`                                                             |

| Property                                                    | Pattern | Type   | Deprecated | Definition | Title/Description |
| ----------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i6_retriever_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i6_retriever_additionalProperties )         | No      | object | No         | -          | -                 |

##### <a name="apu_anyOf_i6_retriever_implementation"></a>12.7.12.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i6_retriever_apu"></a>12.7.13. Property `retriever_apu`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                        |
| ----------------------------------------------------- |
| [APU Reference](#apu_anyOf_i6_retriever_apu_anyOf_i0) |
| [item 1](#apu_anyOf_i6_retriever_apu_anyOf_i1)        |

##### <a name="apu_anyOf_i6_retriever_apu_anyOf_i0"></a>12.7.13.1. Property `APU Reference`

**Title:** APU Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.apu.APU"`                                            |

| Property                                                                 | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------ | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i6_retriever_apu_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i6_retriever_apu_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i6_retriever_apu_anyOf_i0_implementation"></a>12.7.13.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i6_retriever_apu_anyOf_i1"></a>12.7.13.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

### <a name="apu_anyOf_i7"></a>12.8. Property `Llamma3-8b.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./Llamma3-8b.json                                                    |

| Property                                                          | Pattern | Type            | Deprecated | Definition                       | Title/Description                                                    |
| ----------------------------------------------------------------- | ------- | --------------- | ---------- | -------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i7_implementation )                 | No      | const           | No         | -                                | Llamma3-8b                                                           |
| - [max_num_function_calls](#apu_anyOf_i7_max_num_function_calls ) | No      | integer         | No         | -                                | Max Num Function Calls                                               |
| - [io_unit](#apu_anyOf_i7_io_unit )                               | No      | object          | No         | -                                | IOUnit Reference                                                     |
| - [memory_unit](#apu_anyOf_i7_memory_unit )                       | No      | object          | No         | -                                | MemoryUnit Reference                                                 |
| - [llm_unit](#apu_anyOf_i7_llm_unit )                             | No      | object          | No         | In [LLMUnit](/docs/components/llmunit/overview) | Overview of <class 'eidolon_ai_sdk.apu.llm_unit.LLMUnit'> components |
| - [logic_units](#apu_anyOf_i7_logic_units )                       | No      | array of object | No         | -                                | Logic Units                                                          |
| - [audio_unit](#apu_anyOf_i7_audio_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [image_unit](#apu_anyOf_i7_image_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [record_conversation](#apu_anyOf_i7_record_conversation )       | No      | boolean         | No         | -                                | Record Conversation                                                  |
| - [allow_tool_errors](#apu_anyOf_i7_allow_tool_errors )           | No      | boolean         | No         | -                                | Allow Tool Errors                                                    |
| - [document_processor](#apu_anyOf_i7_document_processor )         | No      | object          | No         | -                                | DocumentProcessor Reference                                          |
| - [retriever](#apu_anyOf_i7_retriever )                           | No      | object          | No         | -                                | Retriever Reference                                                  |
| - [retriever_apu](#apu_anyOf_i7_retriever_apu )                   | No      | Combination     | No         | -                                | -                                                                    |

#### <a name="apu_anyOf_i7_implementation"></a>12.8.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** Llamma3-8b

Specific value: `"Llamma3-8b"`

#### <a name="apu_anyOf_i7_max_num_function_calls"></a>12.8.2. Property `max_num_function_calls`

**Title:** Max Num Function Calls

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `10`      |

**Description:** The maximum number of function calls to make in a single request.

#### <a name="apu_anyOf_i7_io_unit"></a>12.8.3. Property `io_unit`

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

##### <a name="apu_anyOf_i7_io_unit_implementation"></a>12.8.3.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i7_memory_unit"></a>12.8.4. Property `memory_unit`

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

##### <a name="apu_anyOf_i7_memory_unit_implementation"></a>12.8.4.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i7_llm_unit"></a>12.8.5. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Defined in**            | [LLMUnit](/docs/components/llmunit/overview)                                             |

**Description:** Overview of <class 'eidolon_ai_sdk.apu.llm_unit.LLMUnit'> components

| Any of(Option)                                             |
| ---------------------------------------------------------- |
| [AnthropicLLMUnit.json](#apu_anyOf_i0_llm_unit_anyOf_i0)   |
| [MistralGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i1)         |
| [OllamaLLMUnit.json](#apu_anyOf_i0_llm_unit_anyOf_i2)      |
| [OpenAIGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i3)          |
| [ToolCallLLMWrapper.json](#apu_anyOf_i0_llm_unit_anyOf_i4) |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i0"></a>12.8.5.1. Property `AnthropicLLMUnit.json`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_implementation"></a>12.8.5.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AnthropicLLMUnit

Specific value: `"AnthropicLLMUnit"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model"></a>12.8.5.1.2. Property `model`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model_implementation"></a>12.8.5.1.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_temperature"></a>12.8.5.1.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens"></a>12.8.5.1.4. Property `max_tokens`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i0"></a>12.8.5.1.4.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i1"></a>12.8.5.1.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_client_args"></a>12.8.5.1.5. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i1"></a>12.8.5.2. Property `MistralGPT.json`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_implementation"></a>12.8.5.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** MistralGPT

Specific value: `"MistralGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model"></a>12.8.5.2.2. Property `model`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model_implementation"></a>12.8.5.2.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_temperature"></a>12.8.5.2.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_force_json"></a>12.8.5.2.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens"></a>12.8.5.2.5. Property `max_tokens`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i0"></a>12.8.5.2.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i1"></a>12.8.5.2.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_client_args"></a>12.8.5.2.6. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i2"></a>12.8.5.3. Property `OllamaLLMUnit.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./OllamaLLMUnit.json                                                 |

| Property                                                            | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_implementation ) | No      | const       | No         | -          | OllamaLLMUnit      |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i2_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i2_temperature )       | No      | number      | No         | -          | Temperature        |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i2_force_json )         | No      | boolean     | No         | -          | Force Json         |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_options](#apu_anyOf_i0_llm_unit_anyOf_i2_client_options ) | No      | object      | No         | -          | Client Options     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_implementation"></a>12.8.5.3.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OllamaLLMUnit

Specific value: `"OllamaLLMUnit"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model"></a>12.8.5.3.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"llama3"`                                                                |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i2_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation"></a>12.8.5.3.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_temperature"></a>12.8.5.3.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_force_json"></a>12.8.5.3.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens"></a>12.8.5.3.5. Property `max_tokens`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i0"></a>12.8.5.3.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i1"></a>12.8.5.3.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_client_options"></a>12.8.5.3.6. Property `client_options`

**Title:** Client Options

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i3"></a>12.8.5.4. Property `OpenAIGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./OpenAIGPT.json                                                     |

| Property                                                                    | Pattern | Type        | Deprecated | Definition | Title/Description                 |
| --------------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | --------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_implementation )         | No      | const       | No         | -          | OpenAIGPT                         |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i3_model )                           | No      | object      | No         | -          | LLMModel Reference                |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i3_temperature )               | No      | number      | No         | -          | Temperature                       |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i3_force_json )                 | No      | boolean     | No         | -          | Force Json                        |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens )                 | No      | Combination | No         | -          | Max Tokens                        |
| - [connection_handler](#apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler ) | No      | object      | No         | -          | OpenAIConnectionHandler Reference |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_implementation"></a>12.8.5.4.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OpenAIGPT

Specific value: `"OpenAIGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model"></a>12.8.5.4.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"gpt-4-turbo"`                                                           |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i3_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_implementation"></a>12.8.5.4.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_temperature"></a>12.8.5.4.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_force_json"></a>12.8.5.4.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens"></a>12.8.5.4.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens_anyOf_i0"></a>12.8.5.4.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens_anyOf_i1"></a>12.8.5.4.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler"></a>12.8.5.4.6. Property `connection_handler`

**Title:** OpenAIConnectionHandler Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"OpenAIConnectionHandler"`                                               |

| Property                                                                               | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler_implementation"></a>12.8.5.4.6.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i4"></a>12.8.5.5. Property `ToolCallLLMWrapper.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./ToolCallLLMWrapper.json                                            |

| Property                                                                      | Pattern | Type        | Deprecated | Definition                                  | Title/Description                                                    |
| ----------------------------------------------------------------------------- | ------- | ----------- | ---------- | ------------------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i4_implementation )           | No      | const       | No         | -                                           | ToolCallLLMWrapper                                                   |
| - [tool_message_prompt](#apu_anyOf_i0_llm_unit_anyOf_i4_tool_message_prompt ) | No      | string      | No         | -                                           | Tool Message Prompt                                                  |
| - [llm_unit](#apu_anyOf_i0_llm_unit_anyOf_i4_llm_unit )                       | No      | object      | No         | Same as [llm_unit](#apu_anyOf_i0_llm_unit ) | Overview of <class 'eidolon_ai_sdk.apu.llm_unit.LLMUnit'> components |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i4_model )                             | No      | Combination | No         | -                                           | -                                                                    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_implementation"></a>12.8.5.5.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ToolCallLLMWrapper

Specific value: `"ToolCallLLMWrapper"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_tool_message_prompt"></a>12.8.5.5.2. Property `tool_message_prompt`

**Title:** Tool Message Prompt

|              |                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Required** | No                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Default**  | `"You must follow these instructions:\nYou can select zero or more of the above tools based on the user query\nIf there are multiple tools required, make sure a list of tools are returned in a JSON array.\nIf there is no tool that match the user request or you have already answered the question, you will respond with empty json array for the tools.\nYou can also add any additional notes or explanations in the notes field."` |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_llm_unit"></a>12.8.5.5.3. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Same definition as**    | [llm_unit](#apu_anyOf_i0_llm_unit)                                        |

**Description:** Overview of <class 'eidolon_ai_sdk.apu.llm_unit.LLMUnit'> components

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_model"></a>12.8.5.5.4. Property `model`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                       |
| -------------------------------------------------------------------- |
| [LLMModel Reference](#apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i1)             |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0"></a>12.8.5.5.4.1. Property `LLMModel Reference`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.llm_unit.LLMModel"`                                  |

| Property                                                                           | Pattern | Type   | Deprecated | Definition | Title/Description |
| ---------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0_implementation"></a>12.8.5.5.4.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i1"></a>12.8.5.5.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i7_logic_units"></a>12.8.6. Property `logic_units`

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

##### <a name="autogenerated_heading_9"></a>12.8.6.1. LogicUnit Reference

**Title:** LogicUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.logic_unit.LogicUnit"`                               |

| Property                                                            | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i7_logic_units_items_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i7_logic_units_items_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i7_logic_units_items_implementation"></a>12.8.6.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i7_audio_unit"></a>12.8.7. Property `audio_unit`

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

##### <a name="apu_anyOf_i7_audio_unit_anyOf_i0"></a>12.8.7.1. Property `AudioUnit Reference`

**Title:** AudioUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.audio_unit.AudioUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i7_audio_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i7_audio_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i7_audio_unit_anyOf_i0_implementation"></a>12.8.7.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i7_audio_unit_anyOf_i1"></a>12.8.7.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i7_image_unit"></a>12.8.8. Property `image_unit`

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

##### <a name="apu_anyOf_i7_image_unit_anyOf_i0"></a>12.8.8.1. Property `ImageUnit Reference`

**Title:** ImageUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.image_unit.ImageUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i7_image_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i7_image_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i7_image_unit_anyOf_i0_implementation"></a>12.8.8.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i7_image_unit_anyOf_i1"></a>12.8.8.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i7_record_conversation"></a>12.8.9. Property `record_conversation`

**Title:** Record Conversation

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

#### <a name="apu_anyOf_i7_allow_tool_errors"></a>12.8.10. Property `allow_tool_errors`

**Title:** Allow Tool Errors

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

#### <a name="apu_anyOf_i7_document_processor"></a>12.8.11. Property `document_processor`

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

##### <a name="apu_anyOf_i7_document_processor_implementation"></a>12.8.11.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i7_retriever"></a>12.8.12. Property `retriever`

**Title:** Retriever Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"Retriever"`                                                             |

| Property                                                    | Pattern | Type   | Deprecated | Definition | Title/Description |
| ----------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i7_retriever_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i7_retriever_additionalProperties )         | No      | object | No         | -          | -                 |

##### <a name="apu_anyOf_i7_retriever_implementation"></a>12.8.12.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i7_retriever_apu"></a>12.8.13. Property `retriever_apu`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                        |
| ----------------------------------------------------- |
| [APU Reference](#apu_anyOf_i7_retriever_apu_anyOf_i0) |
| [item 1](#apu_anyOf_i7_retriever_apu_anyOf_i1)        |

##### <a name="apu_anyOf_i7_retriever_apu_anyOf_i0"></a>12.8.13.1. Property `APU Reference`

**Title:** APU Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.apu.APU"`                                            |

| Property                                                                 | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------ | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i7_retriever_apu_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i7_retriever_apu_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i7_retriever_apu_anyOf_i0_implementation"></a>12.8.13.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i7_retriever_apu_anyOf_i1"></a>12.8.13.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

### <a name="apu_anyOf_i8"></a>12.9. Property `MistralLarge.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./MistralLarge.json                                                  |

| Property                                                          | Pattern | Type            | Deprecated | Definition                       | Title/Description                                                    |
| ----------------------------------------------------------------- | ------- | --------------- | ---------- | -------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i8_implementation )                 | No      | const           | No         | -                                | MistralLarge                                                         |
| - [max_num_function_calls](#apu_anyOf_i8_max_num_function_calls ) | No      | integer         | No         | -                                | Max Num Function Calls                                               |
| - [io_unit](#apu_anyOf_i8_io_unit )                               | No      | object          | No         | -                                | IOUnit Reference                                                     |
| - [memory_unit](#apu_anyOf_i8_memory_unit )                       | No      | object          | No         | -                                | MemoryUnit Reference                                                 |
| - [llm_unit](#apu_anyOf_i8_llm_unit )                             | No      | object          | No         | In [LLMUnit](/docs/components/llmunit/overview) | Overview of <class 'eidolon_ai_sdk.apu.llm_unit.LLMUnit'> components |
| - [logic_units](#apu_anyOf_i8_logic_units )                       | No      | array of object | No         | -                                | Logic Units                                                          |
| - [audio_unit](#apu_anyOf_i8_audio_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [image_unit](#apu_anyOf_i8_image_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [record_conversation](#apu_anyOf_i8_record_conversation )       | No      | boolean         | No         | -                                | Record Conversation                                                  |
| - [allow_tool_errors](#apu_anyOf_i8_allow_tool_errors )           | No      | boolean         | No         | -                                | Allow Tool Errors                                                    |
| - [document_processor](#apu_anyOf_i8_document_processor )         | No      | object          | No         | -                                | DocumentProcessor Reference                                          |
| - [retriever](#apu_anyOf_i8_retriever )                           | No      | object          | No         | -                                | Retriever Reference                                                  |
| - [retriever_apu](#apu_anyOf_i8_retriever_apu )                   | No      | Combination     | No         | -                                | -                                                                    |

#### <a name="apu_anyOf_i8_implementation"></a>12.9.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** MistralLarge

Specific value: `"MistralLarge"`

#### <a name="apu_anyOf_i8_max_num_function_calls"></a>12.9.2. Property `max_num_function_calls`

**Title:** Max Num Function Calls

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `10`      |

**Description:** The maximum number of function calls to make in a single request.

#### <a name="apu_anyOf_i8_io_unit"></a>12.9.3. Property `io_unit`

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

##### <a name="apu_anyOf_i8_io_unit_implementation"></a>12.9.3.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i8_memory_unit"></a>12.9.4. Property `memory_unit`

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

##### <a name="apu_anyOf_i8_memory_unit_implementation"></a>12.9.4.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i8_llm_unit"></a>12.9.5. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Defined in**            | [LLMUnit](/docs/components/llmunit/overview)                                             |

**Description:** Overview of <class 'eidolon_ai_sdk.apu.llm_unit.LLMUnit'> components

| Any of(Option)                                             |
| ---------------------------------------------------------- |
| [AnthropicLLMUnit.json](#apu_anyOf_i0_llm_unit_anyOf_i0)   |
| [MistralGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i1)         |
| [OllamaLLMUnit.json](#apu_anyOf_i0_llm_unit_anyOf_i2)      |
| [OpenAIGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i3)          |
| [ToolCallLLMWrapper.json](#apu_anyOf_i0_llm_unit_anyOf_i4) |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i0"></a>12.9.5.1. Property `AnthropicLLMUnit.json`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_implementation"></a>12.9.5.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AnthropicLLMUnit

Specific value: `"AnthropicLLMUnit"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model"></a>12.9.5.1.2. Property `model`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model_implementation"></a>12.9.5.1.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_temperature"></a>12.9.5.1.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens"></a>12.9.5.1.4. Property `max_tokens`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i0"></a>12.9.5.1.4.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i1"></a>12.9.5.1.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_client_args"></a>12.9.5.1.5. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i1"></a>12.9.5.2. Property `MistralGPT.json`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_implementation"></a>12.9.5.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** MistralGPT

Specific value: `"MistralGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model"></a>12.9.5.2.2. Property `model`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model_implementation"></a>12.9.5.2.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_temperature"></a>12.9.5.2.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_force_json"></a>12.9.5.2.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens"></a>12.9.5.2.5. Property `max_tokens`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i0"></a>12.9.5.2.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i1"></a>12.9.5.2.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_client_args"></a>12.9.5.2.6. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i2"></a>12.9.5.3. Property `OllamaLLMUnit.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./OllamaLLMUnit.json                                                 |

| Property                                                            | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_implementation ) | No      | const       | No         | -          | OllamaLLMUnit      |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i2_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i2_temperature )       | No      | number      | No         | -          | Temperature        |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i2_force_json )         | No      | boolean     | No         | -          | Force Json         |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_options](#apu_anyOf_i0_llm_unit_anyOf_i2_client_options ) | No      | object      | No         | -          | Client Options     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_implementation"></a>12.9.5.3.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OllamaLLMUnit

Specific value: `"OllamaLLMUnit"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model"></a>12.9.5.3.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"llama3"`                                                                |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i2_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation"></a>12.9.5.3.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_temperature"></a>12.9.5.3.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_force_json"></a>12.9.5.3.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens"></a>12.9.5.3.5. Property `max_tokens`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i0"></a>12.9.5.3.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i1"></a>12.9.5.3.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_client_options"></a>12.9.5.3.6. Property `client_options`

**Title:** Client Options

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i3"></a>12.9.5.4. Property `OpenAIGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./OpenAIGPT.json                                                     |

| Property                                                                    | Pattern | Type        | Deprecated | Definition | Title/Description                 |
| --------------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | --------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_implementation )         | No      | const       | No         | -          | OpenAIGPT                         |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i3_model )                           | No      | object      | No         | -          | LLMModel Reference                |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i3_temperature )               | No      | number      | No         | -          | Temperature                       |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i3_force_json )                 | No      | boolean     | No         | -          | Force Json                        |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens )                 | No      | Combination | No         | -          | Max Tokens                        |
| - [connection_handler](#apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler ) | No      | object      | No         | -          | OpenAIConnectionHandler Reference |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_implementation"></a>12.9.5.4.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OpenAIGPT

Specific value: `"OpenAIGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model"></a>12.9.5.4.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"gpt-4-turbo"`                                                           |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i3_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_implementation"></a>12.9.5.4.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_temperature"></a>12.9.5.4.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_force_json"></a>12.9.5.4.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens"></a>12.9.5.4.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens_anyOf_i0"></a>12.9.5.4.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens_anyOf_i1"></a>12.9.5.4.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler"></a>12.9.5.4.6. Property `connection_handler`

**Title:** OpenAIConnectionHandler Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"OpenAIConnectionHandler"`                                               |

| Property                                                                               | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler_implementation"></a>12.9.5.4.6.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i4"></a>12.9.5.5. Property `ToolCallLLMWrapper.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./ToolCallLLMWrapper.json                                            |

| Property                                                                      | Pattern | Type        | Deprecated | Definition                                  | Title/Description                                                    |
| ----------------------------------------------------------------------------- | ------- | ----------- | ---------- | ------------------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i4_implementation )           | No      | const       | No         | -                                           | ToolCallLLMWrapper                                                   |
| - [tool_message_prompt](#apu_anyOf_i0_llm_unit_anyOf_i4_tool_message_prompt ) | No      | string      | No         | -                                           | Tool Message Prompt                                                  |
| - [llm_unit](#apu_anyOf_i0_llm_unit_anyOf_i4_llm_unit )                       | No      | object      | No         | Same as [llm_unit](#apu_anyOf_i0_llm_unit ) | Overview of <class 'eidolon_ai_sdk.apu.llm_unit.LLMUnit'> components |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i4_model )                             | No      | Combination | No         | -                                           | -                                                                    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_implementation"></a>12.9.5.5.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ToolCallLLMWrapper

Specific value: `"ToolCallLLMWrapper"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_tool_message_prompt"></a>12.9.5.5.2. Property `tool_message_prompt`

**Title:** Tool Message Prompt

|              |                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Required** | No                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Default**  | `"You must follow these instructions:\nYou can select zero or more of the above tools based on the user query\nIf there are multiple tools required, make sure a list of tools are returned in a JSON array.\nIf there is no tool that match the user request or you have already answered the question, you will respond with empty json array for the tools.\nYou can also add any additional notes or explanations in the notes field."` |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_llm_unit"></a>12.9.5.5.3. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Same definition as**    | [llm_unit](#apu_anyOf_i0_llm_unit)                                        |

**Description:** Overview of <class 'eidolon_ai_sdk.apu.llm_unit.LLMUnit'> components

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_model"></a>12.9.5.5.4. Property `model`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                       |
| -------------------------------------------------------------------- |
| [LLMModel Reference](#apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i1)             |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0"></a>12.9.5.5.4.1. Property `LLMModel Reference`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.llm_unit.LLMModel"`                                  |

| Property                                                                           | Pattern | Type   | Deprecated | Definition | Title/Description |
| ---------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0_implementation"></a>12.9.5.5.4.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i1"></a>12.9.5.5.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i8_logic_units"></a>12.9.6. Property `logic_units`

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

##### <a name="autogenerated_heading_10"></a>12.9.6.1. LogicUnit Reference

**Title:** LogicUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.logic_unit.LogicUnit"`                               |

| Property                                                            | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i8_logic_units_items_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i8_logic_units_items_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i8_logic_units_items_implementation"></a>12.9.6.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i8_audio_unit"></a>12.9.7. Property `audio_unit`

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

##### <a name="apu_anyOf_i8_audio_unit_anyOf_i0"></a>12.9.7.1. Property `AudioUnit Reference`

**Title:** AudioUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.audio_unit.AudioUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i8_audio_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i8_audio_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i8_audio_unit_anyOf_i0_implementation"></a>12.9.7.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i8_audio_unit_anyOf_i1"></a>12.9.7.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i8_image_unit"></a>12.9.8. Property `image_unit`

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

##### <a name="apu_anyOf_i8_image_unit_anyOf_i0"></a>12.9.8.1. Property `ImageUnit Reference`

**Title:** ImageUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.image_unit.ImageUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i8_image_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i8_image_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i8_image_unit_anyOf_i0_implementation"></a>12.9.8.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i8_image_unit_anyOf_i1"></a>12.9.8.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i8_record_conversation"></a>12.9.9. Property `record_conversation`

**Title:** Record Conversation

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

#### <a name="apu_anyOf_i8_allow_tool_errors"></a>12.9.10. Property `allow_tool_errors`

**Title:** Allow Tool Errors

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

#### <a name="apu_anyOf_i8_document_processor"></a>12.9.11. Property `document_processor`

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

##### <a name="apu_anyOf_i8_document_processor_implementation"></a>12.9.11.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i8_retriever"></a>12.9.12. Property `retriever`

**Title:** Retriever Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"Retriever"`                                                             |

| Property                                                    | Pattern | Type   | Deprecated | Definition | Title/Description |
| ----------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i8_retriever_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i8_retriever_additionalProperties )         | No      | object | No         | -          | -                 |

##### <a name="apu_anyOf_i8_retriever_implementation"></a>12.9.12.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i8_retriever_apu"></a>12.9.13. Property `retriever_apu`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                        |
| ----------------------------------------------------- |
| [APU Reference](#apu_anyOf_i8_retriever_apu_anyOf_i0) |
| [item 1](#apu_anyOf_i8_retriever_apu_anyOf_i1)        |

##### <a name="apu_anyOf_i8_retriever_apu_anyOf_i0"></a>12.9.13.1. Property `APU Reference`

**Title:** APU Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.apu.APU"`                                            |

| Property                                                                 | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------ | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i8_retriever_apu_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i8_retriever_apu_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i8_retriever_apu_anyOf_i0_implementation"></a>12.9.13.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i8_retriever_apu_anyOf_i1"></a>12.9.13.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

### <a name="apu_anyOf_i9"></a>12.10. Property `MistralMedium.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./MistralMedium.json                                                 |

| Property                                                          | Pattern | Type            | Deprecated | Definition                       | Title/Description                                                    |
| ----------------------------------------------------------------- | ------- | --------------- | ---------- | -------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i9_implementation )                 | No      | const           | No         | -                                | MistralMedium                                                        |
| - [max_num_function_calls](#apu_anyOf_i9_max_num_function_calls ) | No      | integer         | No         | -                                | Max Num Function Calls                                               |
| - [io_unit](#apu_anyOf_i9_io_unit )                               | No      | object          | No         | -                                | IOUnit Reference                                                     |
| - [memory_unit](#apu_anyOf_i9_memory_unit )                       | No      | object          | No         | -                                | MemoryUnit Reference                                                 |
| - [llm_unit](#apu_anyOf_i9_llm_unit )                             | No      | object          | No         | In [LLMUnit](/docs/components/llmunit/overview) | Overview of <class 'eidolon_ai_sdk.apu.llm_unit.LLMUnit'> components |
| - [logic_units](#apu_anyOf_i9_logic_units )                       | No      | array of object | No         | -                                | Logic Units                                                          |
| - [audio_unit](#apu_anyOf_i9_audio_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [image_unit](#apu_anyOf_i9_image_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [record_conversation](#apu_anyOf_i9_record_conversation )       | No      | boolean         | No         | -                                | Record Conversation                                                  |
| - [allow_tool_errors](#apu_anyOf_i9_allow_tool_errors )           | No      | boolean         | No         | -                                | Allow Tool Errors                                                    |
| - [document_processor](#apu_anyOf_i9_document_processor )         | No      | object          | No         | -                                | DocumentProcessor Reference                                          |
| - [retriever](#apu_anyOf_i9_retriever )                           | No      | object          | No         | -                                | Retriever Reference                                                  |
| - [retriever_apu](#apu_anyOf_i9_retriever_apu )                   | No      | Combination     | No         | -                                | -                                                                    |

#### <a name="apu_anyOf_i9_implementation"></a>12.10.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** MistralMedium

Specific value: `"MistralMedium"`

#### <a name="apu_anyOf_i9_max_num_function_calls"></a>12.10.2. Property `max_num_function_calls`

**Title:** Max Num Function Calls

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `10`      |

**Description:** The maximum number of function calls to make in a single request.

#### <a name="apu_anyOf_i9_io_unit"></a>12.10.3. Property `io_unit`

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

##### <a name="apu_anyOf_i9_io_unit_implementation"></a>12.10.3.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i9_memory_unit"></a>12.10.4. Property `memory_unit`

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

##### <a name="apu_anyOf_i9_memory_unit_implementation"></a>12.10.4.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i9_llm_unit"></a>12.10.5. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Defined in**            | [LLMUnit](/docs/components/llmunit/overview)                                             |

**Description:** Overview of <class 'eidolon_ai_sdk.apu.llm_unit.LLMUnit'> components

| Any of(Option)                                             |
| ---------------------------------------------------------- |
| [AnthropicLLMUnit.json](#apu_anyOf_i0_llm_unit_anyOf_i0)   |
| [MistralGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i1)         |
| [OllamaLLMUnit.json](#apu_anyOf_i0_llm_unit_anyOf_i2)      |
| [OpenAIGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i3)          |
| [ToolCallLLMWrapper.json](#apu_anyOf_i0_llm_unit_anyOf_i4) |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i0"></a>12.10.5.1. Property `AnthropicLLMUnit.json`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_implementation"></a>12.10.5.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AnthropicLLMUnit

Specific value: `"AnthropicLLMUnit"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model"></a>12.10.5.1.2. Property `model`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model_implementation"></a>12.10.5.1.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_temperature"></a>12.10.5.1.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens"></a>12.10.5.1.4. Property `max_tokens`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i0"></a>12.10.5.1.4.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i1"></a>12.10.5.1.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_client_args"></a>12.10.5.1.5. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i1"></a>12.10.5.2. Property `MistralGPT.json`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_implementation"></a>12.10.5.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** MistralGPT

Specific value: `"MistralGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model"></a>12.10.5.2.2. Property `model`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model_implementation"></a>12.10.5.2.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_temperature"></a>12.10.5.2.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_force_json"></a>12.10.5.2.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens"></a>12.10.5.2.5. Property `max_tokens`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i0"></a>12.10.5.2.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i1"></a>12.10.5.2.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_client_args"></a>12.10.5.2.6. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i2"></a>12.10.5.3. Property `OllamaLLMUnit.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./OllamaLLMUnit.json                                                 |

| Property                                                            | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_implementation ) | No      | const       | No         | -          | OllamaLLMUnit      |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i2_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i2_temperature )       | No      | number      | No         | -          | Temperature        |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i2_force_json )         | No      | boolean     | No         | -          | Force Json         |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_options](#apu_anyOf_i0_llm_unit_anyOf_i2_client_options ) | No      | object      | No         | -          | Client Options     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_implementation"></a>12.10.5.3.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OllamaLLMUnit

Specific value: `"OllamaLLMUnit"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model"></a>12.10.5.3.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"llama3"`                                                                |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i2_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation"></a>12.10.5.3.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_temperature"></a>12.10.5.3.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_force_json"></a>12.10.5.3.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens"></a>12.10.5.3.5. Property `max_tokens`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i0"></a>12.10.5.3.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i1"></a>12.10.5.3.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_client_options"></a>12.10.5.3.6. Property `client_options`

**Title:** Client Options

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i3"></a>12.10.5.4. Property `OpenAIGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./OpenAIGPT.json                                                     |

| Property                                                                    | Pattern | Type        | Deprecated | Definition | Title/Description                 |
| --------------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | --------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_implementation )         | No      | const       | No         | -          | OpenAIGPT                         |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i3_model )                           | No      | object      | No         | -          | LLMModel Reference                |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i3_temperature )               | No      | number      | No         | -          | Temperature                       |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i3_force_json )                 | No      | boolean     | No         | -          | Force Json                        |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens )                 | No      | Combination | No         | -          | Max Tokens                        |
| - [connection_handler](#apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler ) | No      | object      | No         | -          | OpenAIConnectionHandler Reference |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_implementation"></a>12.10.5.4.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OpenAIGPT

Specific value: `"OpenAIGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model"></a>12.10.5.4.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"gpt-4-turbo"`                                                           |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i3_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_implementation"></a>12.10.5.4.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_temperature"></a>12.10.5.4.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_force_json"></a>12.10.5.4.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens"></a>12.10.5.4.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens_anyOf_i0"></a>12.10.5.4.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens_anyOf_i1"></a>12.10.5.4.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler"></a>12.10.5.4.6. Property `connection_handler`

**Title:** OpenAIConnectionHandler Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"OpenAIConnectionHandler"`                                               |

| Property                                                                               | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler_implementation"></a>12.10.5.4.6.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i4"></a>12.10.5.5. Property `ToolCallLLMWrapper.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./ToolCallLLMWrapper.json                                            |

| Property                                                                      | Pattern | Type        | Deprecated | Definition                                  | Title/Description                                                    |
| ----------------------------------------------------------------------------- | ------- | ----------- | ---------- | ------------------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i4_implementation )           | No      | const       | No         | -                                           | ToolCallLLMWrapper                                                   |
| - [tool_message_prompt](#apu_anyOf_i0_llm_unit_anyOf_i4_tool_message_prompt ) | No      | string      | No         | -                                           | Tool Message Prompt                                                  |
| - [llm_unit](#apu_anyOf_i0_llm_unit_anyOf_i4_llm_unit )                       | No      | object      | No         | Same as [llm_unit](#apu_anyOf_i0_llm_unit ) | Overview of <class 'eidolon_ai_sdk.apu.llm_unit.LLMUnit'> components |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i4_model )                             | No      | Combination | No         | -                                           | -                                                                    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_implementation"></a>12.10.5.5.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ToolCallLLMWrapper

Specific value: `"ToolCallLLMWrapper"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_tool_message_prompt"></a>12.10.5.5.2. Property `tool_message_prompt`

**Title:** Tool Message Prompt

|              |                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Required** | No                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Default**  | `"You must follow these instructions:\nYou can select zero or more of the above tools based on the user query\nIf there are multiple tools required, make sure a list of tools are returned in a JSON array.\nIf there is no tool that match the user request or you have already answered the question, you will respond with empty json array for the tools.\nYou can also add any additional notes or explanations in the notes field."` |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_llm_unit"></a>12.10.5.5.3. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Same definition as**    | [llm_unit](#apu_anyOf_i0_llm_unit)                                        |

**Description:** Overview of <class 'eidolon_ai_sdk.apu.llm_unit.LLMUnit'> components

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_model"></a>12.10.5.5.4. Property `model`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                       |
| -------------------------------------------------------------------- |
| [LLMModel Reference](#apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i1)             |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0"></a>12.10.5.5.4.1. Property `LLMModel Reference`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.llm_unit.LLMModel"`                                  |

| Property                                                                           | Pattern | Type   | Deprecated | Definition | Title/Description |
| ---------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0_implementation"></a>12.10.5.5.4.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i1"></a>12.10.5.5.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i9_logic_units"></a>12.10.6. Property `logic_units`

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

##### <a name="autogenerated_heading_11"></a>12.10.6.1. LogicUnit Reference

**Title:** LogicUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.logic_unit.LogicUnit"`                               |

| Property                                                            | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i9_logic_units_items_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i9_logic_units_items_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i9_logic_units_items_implementation"></a>12.10.6.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i9_audio_unit"></a>12.10.7. Property `audio_unit`

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

##### <a name="apu_anyOf_i9_audio_unit_anyOf_i0"></a>12.10.7.1. Property `AudioUnit Reference`

**Title:** AudioUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.audio_unit.AudioUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i9_audio_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i9_audio_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i9_audio_unit_anyOf_i0_implementation"></a>12.10.7.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i9_audio_unit_anyOf_i1"></a>12.10.7.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i9_image_unit"></a>12.10.8. Property `image_unit`

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

##### <a name="apu_anyOf_i9_image_unit_anyOf_i0"></a>12.10.8.1. Property `ImageUnit Reference`

**Title:** ImageUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.image_unit.ImageUnit"`                               |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i9_image_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i9_image_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i9_image_unit_anyOf_i0_implementation"></a>12.10.8.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i9_image_unit_anyOf_i1"></a>12.10.8.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i9_record_conversation"></a>12.10.9. Property `record_conversation`

**Title:** Record Conversation

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

#### <a name="apu_anyOf_i9_allow_tool_errors"></a>12.10.10. Property `allow_tool_errors`

**Title:** Allow Tool Errors

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

#### <a name="apu_anyOf_i9_document_processor"></a>12.10.11. Property `document_processor`

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

##### <a name="apu_anyOf_i9_document_processor_implementation"></a>12.10.11.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i9_retriever"></a>12.10.12. Property `retriever`

**Title:** Retriever Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"Retriever"`                                                             |

| Property                                                    | Pattern | Type   | Deprecated | Definition | Title/Description |
| ----------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i9_retriever_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i9_retriever_additionalProperties )         | No      | object | No         | -          | -                 |

##### <a name="apu_anyOf_i9_retriever_implementation"></a>12.10.12.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i9_retriever_apu"></a>12.10.13. Property `retriever_apu`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                        |
| ----------------------------------------------------- |
| [APU Reference](#apu_anyOf_i9_retriever_apu_anyOf_i0) |
| [item 1](#apu_anyOf_i9_retriever_apu_anyOf_i1)        |

##### <a name="apu_anyOf_i9_retriever_apu_anyOf_i0"></a>12.10.13.1. Property `APU Reference`

**Title:** APU Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.apu.APU"`                                            |

| Property                                                                 | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------ | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i9_retriever_apu_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i9_retriever_apu_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i9_retriever_apu_anyOf_i0_implementation"></a>12.10.13.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i9_retriever_apu_anyOf_i1"></a>12.10.13.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

### <a name="apu_anyOf_i10"></a>12.11. Property `MistralSmall.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./MistralSmall.json                                                  |

| Property                                                           | Pattern | Type            | Deprecated | Definition                       | Title/Description                                                    |
| ------------------------------------------------------------------ | ------- | --------------- | ---------- | -------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i10_implementation )                 | No      | const           | No         | -                                | MistralSmall                                                         |
| - [max_num_function_calls](#apu_anyOf_i10_max_num_function_calls ) | No      | integer         | No         | -                                | Max Num Function Calls                                               |
| - [io_unit](#apu_anyOf_i10_io_unit )                               | No      | object          | No         | -                                | IOUnit Reference                                                     |
| - [memory_unit](#apu_anyOf_i10_memory_unit )                       | No      | object          | No         | -                                | MemoryUnit Reference                                                 |
| - [llm_unit](#apu_anyOf_i10_llm_unit )                             | No      | object          | No         | In [LLMUnit](/docs/components/llmunit/overview) | Overview of <class 'eidolon_ai_sdk.apu.llm_unit.LLMUnit'> components |
| - [logic_units](#apu_anyOf_i10_logic_units )                       | No      | array of object | No         | -                                | Logic Units                                                          |
| - [audio_unit](#apu_anyOf_i10_audio_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [image_unit](#apu_anyOf_i10_image_unit )                         | No      | Combination     | No         | -                                | -                                                                    |
| - [record_conversation](#apu_anyOf_i10_record_conversation )       | No      | boolean         | No         | -                                | Record Conversation                                                  |
| - [allow_tool_errors](#apu_anyOf_i10_allow_tool_errors )           | No      | boolean         | No         | -                                | Allow Tool Errors                                                    |
| - [document_processor](#apu_anyOf_i10_document_processor )         | No      | object          | No         | -                                | DocumentProcessor Reference                                          |
| - [retriever](#apu_anyOf_i10_retriever )                           | No      | object          | No         | -                                | Retriever Reference                                                  |
| - [retriever_apu](#apu_anyOf_i10_retriever_apu )                   | No      | Combination     | No         | -                                | -                                                                    |

#### <a name="apu_anyOf_i10_implementation"></a>12.11.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** MistralSmall

Specific value: `"MistralSmall"`

#### <a name="apu_anyOf_i10_max_num_function_calls"></a>12.11.2. Property `max_num_function_calls`

**Title:** Max Num Function Calls

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `10`      |

**Description:** The maximum number of function calls to make in a single request.

#### <a name="apu_anyOf_i10_io_unit"></a>12.11.3. Property `io_unit`

**Title:** IOUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"IOUnit"`                                                                |

| Property                                                   | Pattern | Type   | Deprecated | Definition | Title/Description |
| ---------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i10_io_unit_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i10_io_unit_additionalProperties )         | No      | object | No         | -          | -                 |

##### <a name="apu_anyOf_i10_io_unit_implementation"></a>12.11.3.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i10_memory_unit"></a>12.11.4. Property `memory_unit`

**Title:** MemoryUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"MemoryUnit"`                                                            |

| Property                                                       | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i10_memory_unit_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i10_memory_unit_additionalProperties )         | No      | object | No         | -          | -                 |

##### <a name="apu_anyOf_i10_memory_unit_implementation"></a>12.11.4.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i10_llm_unit"></a>12.11.5. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Defined in**            | [LLMUnit](/docs/components/llmunit/overview)                                             |

**Description:** Overview of <class 'eidolon_ai_sdk.apu.llm_unit.LLMUnit'> components

| Any of(Option)                                             |
| ---------------------------------------------------------- |
| [AnthropicLLMUnit.json](#apu_anyOf_i0_llm_unit_anyOf_i0)   |
| [MistralGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i1)         |
| [OllamaLLMUnit.json](#apu_anyOf_i0_llm_unit_anyOf_i2)      |
| [OpenAIGPT.json](#apu_anyOf_i0_llm_unit_anyOf_i3)          |
| [ToolCallLLMWrapper.json](#apu_anyOf_i0_llm_unit_anyOf_i4) |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i0"></a>12.11.5.1. Property `AnthropicLLMUnit.json`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_implementation"></a>12.11.5.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AnthropicLLMUnit

Specific value: `"AnthropicLLMUnit"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model"></a>12.11.5.1.2. Property `model`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_model_implementation"></a>12.11.5.1.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_temperature"></a>12.11.5.1.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens"></a>12.11.5.1.4. Property `max_tokens`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i0"></a>12.11.5.1.4.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_max_tokens_anyOf_i1"></a>12.11.5.1.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i0_client_args"></a>12.11.5.1.5. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i1"></a>12.11.5.2. Property `MistralGPT.json`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_implementation"></a>12.11.5.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** MistralGPT

Specific value: `"MistralGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model"></a>12.11.5.2.2. Property `model`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_model_implementation"></a>12.11.5.2.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_temperature"></a>12.11.5.2.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_force_json"></a>12.11.5.2.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens"></a>12.11.5.2.5. Property `max_tokens`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i0"></a>12.11.5.2.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_max_tokens_anyOf_i1"></a>12.11.5.2.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i1_client_args"></a>12.11.5.2.6. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i2"></a>12.11.5.3. Property `OllamaLLMUnit.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./OllamaLLMUnit.json                                                 |

| Property                                                            | Pattern | Type        | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ------------------ |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_implementation ) | No      | const       | No         | -          | OllamaLLMUnit      |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i2_model )                   | No      | object      | No         | -          | LLMModel Reference |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i2_temperature )       | No      | number      | No         | -          | Temperature        |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i2_force_json )         | No      | boolean     | No         | -          | Force Json         |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens )         | No      | Combination | No         | -          | Max Tokens         |
| - [client_options](#apu_anyOf_i0_llm_unit_anyOf_i2_client_options ) | No      | object      | No         | -          | Client Options     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_implementation"></a>12.11.5.3.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OllamaLLMUnit

Specific value: `"OllamaLLMUnit"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model"></a>12.11.5.3.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"llama3"`                                                                |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i2_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_model_implementation"></a>12.11.5.3.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_temperature"></a>12.11.5.3.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_force_json"></a>12.11.5.3.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens"></a>12.11.5.3.5. Property `max_tokens`

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

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i0"></a>12.11.5.3.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_max_tokens_anyOf_i1"></a>12.11.5.3.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i2_client_options"></a>12.11.5.3.6. Property `client_options`

**Title:** Client Options

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i3"></a>12.11.5.4. Property `OpenAIGPT.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./OpenAIGPT.json                                                     |

| Property                                                                    | Pattern | Type        | Deprecated | Definition | Title/Description                 |
| --------------------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | --------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_implementation )         | No      | const       | No         | -          | OpenAIGPT                         |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i3_model )                           | No      | object      | No         | -          | LLMModel Reference                |
| - [temperature](#apu_anyOf_i0_llm_unit_anyOf_i3_temperature )               | No      | number      | No         | -          | Temperature                       |
| - [force_json](#apu_anyOf_i0_llm_unit_anyOf_i3_force_json )                 | No      | boolean     | No         | -          | Force Json                        |
| - [max_tokens](#apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens )                 | No      | Combination | No         | -          | Max Tokens                        |
| - [connection_handler](#apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler ) | No      | object      | No         | -          | OpenAIConnectionHandler Reference |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_implementation"></a>12.11.5.4.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OpenAIGPT

Specific value: `"OpenAIGPT"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model"></a>12.11.5.4.2. Property `model`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"gpt-4-turbo"`                                                           |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_model_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i3_model_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_model_implementation"></a>12.11.5.4.2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_temperature"></a>12.11.5.4.3. Property `temperature`

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_force_json"></a>12.11.5.4.4. Property `force_json`

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens"></a>12.11.5.4.5. Property `max_tokens`

**Title:** Max Tokens

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [item 0](#apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens_anyOf_i1) |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens_anyOf_i0"></a>12.11.5.4.5.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_max_tokens_anyOf_i1"></a>12.11.5.4.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler"></a>12.11.5.4.6. Property `connection_handler`

**Title:** OpenAIConnectionHandler Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"OpenAIConnectionHandler"`                                               |

| Property                                                                               | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i3_connection_handler_implementation"></a>12.11.5.4.6.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i0_llm_unit_anyOf_i4"></a>12.11.5.5. Property `ToolCallLLMWrapper.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./ToolCallLLMWrapper.json                                            |

| Property                                                                      | Pattern | Type        | Deprecated | Definition                                  | Title/Description                                                    |
| ----------------------------------------------------------------------------- | ------- | ----------- | ---------- | ------------------------------------------- | -------------------------------------------------------------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i4_implementation )           | No      | const       | No         | -                                           | ToolCallLLMWrapper                                                   |
| - [tool_message_prompt](#apu_anyOf_i0_llm_unit_anyOf_i4_tool_message_prompt ) | No      | string      | No         | -                                           | Tool Message Prompt                                                  |
| - [llm_unit](#apu_anyOf_i0_llm_unit_anyOf_i4_llm_unit )                       | No      | object      | No         | Same as [llm_unit](#apu_anyOf_i0_llm_unit ) | Overview of <class 'eidolon_ai_sdk.apu.llm_unit.LLMUnit'> components |
| - [model](#apu_anyOf_i0_llm_unit_anyOf_i4_model )                             | No      | Combination | No         | -                                           | -                                                                    |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_implementation"></a>12.11.5.5.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ToolCallLLMWrapper

Specific value: `"ToolCallLLMWrapper"`

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_tool_message_prompt"></a>12.11.5.5.2. Property `tool_message_prompt`

**Title:** Tool Message Prompt

|              |                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Required** | No                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Default**  | `"You must follow these instructions:\nYou can select zero or more of the above tools based on the user query\nIf there are multiple tools required, make sure a list of tools are returned in a JSON array.\nIf there is no tool that match the user request or you have already answered the question, you will respond with empty json array for the tools.\nYou can also add any additional notes or explanations in the notes field."` |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_llm_unit"></a>12.11.5.5.3. Property `llm_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"LLMUnit"`                                                               |
| **Same definition as**    | [llm_unit](#apu_anyOf_i0_llm_unit)                                        |

**Description:** Overview of <class 'eidolon_ai_sdk.apu.llm_unit.LLMUnit'> components

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_model"></a>12.11.5.5.4. Property `model`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                                       |
| -------------------------------------------------------------------- |
| [LLMModel Reference](#apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0) |
| [item 1](#apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i1)             |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0"></a>12.11.5.5.4.1. Property `LLMModel Reference`

**Title:** LLMModel Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.llm_unit.LLMModel"`                                  |

| Property                                                                           | Pattern | Type   | Deprecated | Definition | Title/Description |
| ---------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i0_implementation"></a>12.11.5.5.4.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="apu_anyOf_i0_llm_unit_anyOf_i4_model_anyOf_i1"></a>12.11.5.5.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i10_logic_units"></a>12.11.6. Property `logic_units`

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

| Each item of this array must be                         | Description |
| ------------------------------------------------------- | ----------- |
| [LogicUnit Reference](#apu_anyOf_i10_logic_units_items) | -           |

##### <a name="autogenerated_heading_12"></a>12.11.6.1. LogicUnit Reference

**Title:** LogicUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.logic_unit.LogicUnit"`                               |

| Property                                                             | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i10_logic_units_items_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i10_logic_units_items_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i10_logic_units_items_implementation"></a>12.11.6.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i10_audio_unit"></a>12.11.7. Property `audio_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                            |
| --------------------------------------------------------- |
| [AudioUnit Reference](#apu_anyOf_i10_audio_unit_anyOf_i0) |
| [item 1](#apu_anyOf_i10_audio_unit_anyOf_i1)              |

##### <a name="apu_anyOf_i10_audio_unit_anyOf_i0"></a>12.11.7.1. Property `AudioUnit Reference`

**Title:** AudioUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.audio_unit.AudioUnit"`                               |

| Property                                                               | Pattern | Type   | Deprecated | Definition | Title/Description |
| ---------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i10_audio_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i10_audio_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i10_audio_unit_anyOf_i0_implementation"></a>12.11.7.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i10_audio_unit_anyOf_i1"></a>12.11.7.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i10_image_unit"></a>12.11.8. Property `image_unit`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                            |
| --------------------------------------------------------- |
| [ImageUnit Reference](#apu_anyOf_i10_image_unit_anyOf_i0) |
| [item 1](#apu_anyOf_i10_image_unit_anyOf_i1)              |

##### <a name="apu_anyOf_i10_image_unit_anyOf_i0"></a>12.11.8.1. Property `ImageUnit Reference`

**Title:** ImageUnit Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.image_unit.ImageUnit"`                               |

| Property                                                               | Pattern | Type   | Deprecated | Definition | Title/Description |
| ---------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i10_image_unit_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i10_image_unit_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i10_image_unit_anyOf_i0_implementation"></a>12.11.8.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i10_image_unit_anyOf_i1"></a>12.11.8.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="apu_anyOf_i10_record_conversation"></a>12.11.9. Property `record_conversation`

**Title:** Record Conversation

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

#### <a name="apu_anyOf_i10_allow_tool_errors"></a>12.11.10. Property `allow_tool_errors`

**Title:** Allow Tool Errors

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

#### <a name="apu_anyOf_i10_document_processor"></a>12.11.11. Property `document_processor`

**Title:** DocumentProcessor Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"DocumentProcessor"`                                                     |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i10_document_processor_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i10_document_processor_additionalProperties )         | No      | object | No         | -          | -                 |

##### <a name="apu_anyOf_i10_document_processor_implementation"></a>12.11.11.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i10_retriever"></a>12.11.12. Property `retriever`

**Title:** Retriever Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"Retriever"`                                                             |

| Property                                                     | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------ | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i10_retriever_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i10_retriever_additionalProperties )         | No      | object | No         | -          | -                 |

##### <a name="apu_anyOf_i10_retriever_implementation"></a>12.11.12.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apu_anyOf_i10_retriever_apu"></a>12.11.13. Property `retriever_apu`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                         |
| ------------------------------------------------------ |
| [APU Reference](#apu_anyOf_i10_retriever_apu_anyOf_i0) |
| [item 1](#apu_anyOf_i10_retriever_apu_anyOf_i1)        |

##### <a name="apu_anyOf_i10_retriever_apu_anyOf_i0"></a>12.11.13.1. Property `APU Reference`

**Title:** APU Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"eidolon_ai_sdk.apu.apu.APU"`                                            |

| Property                                                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_anyOf_i10_retriever_apu_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#apu_anyOf_i10_retriever_apu_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="apu_anyOf_i10_retriever_apu_anyOf_i0_implementation"></a>12.11.13.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

##### <a name="apu_anyOf_i10_retriever_apu_anyOf_i1"></a>12.11.13.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

----------------------------------------------------------------------------------------------------------------------------
