---
title: SimpleAgent
description: "Description of SimpleAgent component"
---

**Description:** The `SimpleAgentSpec` class defines the basic configuration for a SimpleAgent within the Eidolon framework. This
agent is designed to be a flexible, modular component that can interact with various processing units and perform a
range of actions based on its configuration.

| Property                                           | Pattern | Type             | Deprecated | Definition                   | Title/Description                                                                                                                                                                                                                                                                                                                                                                       |
| -------------------------------------------------- | ------- | ---------------- | ---------- | ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| - [implementation](#implementation )               | No      | const            | No         | -                            | SimpleAgent                                                                                                                                                                                                                                                                                                                                                                             |
| - [description](#description )                     | No      | string           | No         | -                            | Description                                                                                                                                                                                                                                                                                                                                                                             |
| - [system_prompt](#system_prompt )                 | No      | string           | No         | -                            | System Prompt                                                                                                                                                                                                                                                                                                                                                                           |
| - [agent_refs](#agent_refs )                       | No      | array of string  | No         | -                            | Agent Refs                                                                                                                                                                                                                                                                                                                                                                              |
| - [actions](#actions )                             | No      | array            | No         | -                            | Actions                                                                                                                                                                                                                                                                                                                                                                                 |
| - [apu](#apu )                                     | No      | Reference[APU]   | No         | In [APU](/docs/components/apu/overview) | The APU is the main interface for the Agent to interact with the LLM.<br />The APU provides a set of capabilities that encapsulate LLM functionality and creates a clear separation between business logic and the underlying LLM implementation.<br /><br />To learn more, check out our blog article APU: [What is it and how does it work?](https://www.eidolonai.com/what_is_apu/). |
| - [apus](#apus )                                   | No      | array            | No         | -                            | Apus                                                                                                                                                                                                                                                                                                                                                                                    |
| - [title_generation_mode](#title_generation_mode ) | No      | enum (of string) | No         | -                            | Title Generation Mode                                                                                                                                                                                                                                                                                                                                                                   |
| - [](#additionalProperties )                       | No      | object           | No         | -                            | -                                                                                                                                                                                                                                                                                                                                                                                       |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** SimpleAgent

Specific value: `"SimpleAgent"`

## <a name="description"></a>2. Property `description`

**Title:** Description

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

## <a name="system_prompt"></a>3. Property `system_prompt`

**Title:** System Prompt

|              |                                                                                                       |
| ------------ | ----------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                              |
| **Required** | No                                                                                                    |
| **Default**  | `"You are a helpful assistant. Always use the provided tools, if appropriate, to complete the task."` |

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
| - [title](#actions_items_title )                               | No      | string          | No         | -          | Title                |
| - [sub_title](#actions_items_sub_title )                       | No      | string          | No         | -          | Sub Title            |
| - [description](#actions_items_description )                   | No      | string          | No         | -          | Description          |
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

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="actions_items_sub_title"></a>5.1.3. Property `sub_title`

**Title:** Sub Title

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="actions_items_description"></a>5.1.4. Property `description`

**Title:** Description

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

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

|                |                             |
| -------------- | --------------------------- |
| **Type**       | `Reference[APU]`            |
| **Required**   | No                          |
| **Default**    | `{"implementation": "APU"}` |
| **Defined in** | [APU](/docs/components/apu/overview)   |

**Description:** The APU is the main interface for the Agent to interact with the LLM.
The APU provides a set of capabilities that encapsulate LLM functionality and creates a clear separation between business logic and the underlying LLM implementation.

To learn more, check out our blog article APU: [What is it and how does it work?](https://www.eidolonai.com/what_is_apu/).

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
| [NamedAPU](#apus_items)         | -           |

### <a name="autogenerated_heading_6"></a>7.1. NamedAPU

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | #/$defs/NamedAPU                                                          |

| Property                                | Pattern | Type           | Deprecated | Definition                   | Title/Description                                                                                                                                                                                                                                                                                                                                                                       |
| --------------------------------------- | ------- | -------------- | ---------- | ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| - [title](#apus_items_title )           | No      | string         | No         | -                            | Title                                                                                                                                                                                                                                                                                                                                                                                   |
| - [apu](#apus_items_apu )               | No      | Reference[APU] | No         | In [APU](/docs/components/apu/overview) | The APU is the main interface for the Agent to interact with the LLM.<br />The APU provides a set of capabilities that encapsulate LLM functionality and creates a clear separation between business logic and the underlying LLM implementation.<br /><br />To learn more, check out our blog article APU: [What is it and how does it work?](https://www.eidolonai.com/what_is_apu/). |
| - [default](#apus_items_default )       | No      | boolean        | No         | -                            | Default                                                                                                                                                                                                                                                                                                                                                                                 |
| - [](#apus_items_additionalProperties ) | No      | object         | No         | -                            | -                                                                                                                                                                                                                                                                                                                                                                                       |

#### <a name="apus_items_title"></a>7.1.1. Property `title`

**Title:** Title

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

#### <a name="apus_items_apu"></a>7.1.2. Property `apu`

|                |                             |
| -------------- | --------------------------- |
| **Type**       | `Reference[APU]`            |
| **Required**   | No                          |
| **Default**    | `{"implementation": "APU"}` |
| **Defined in** | [APU](/docs/components/apu/overview)   |

**Description:** The APU is the main interface for the Agent to interact with the LLM.
The APU provides a set of capabilities that encapsulate LLM functionality and creates a clear separation between business logic and the underlying LLM implementation.

To learn more, check out our blog article APU: [What is it and how does it work?](https://www.eidolonai.com/what_is_apu/).

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

----------------------------------------------------------------------------------------------------------------------------
