---
title: SimpleAgent
description: Description of SimpleAgent component
---
*The `SimpleAgentSpec` class defines the basic configuration for a SimpleAgent within the Eidolon framework. This
agent is designed to be a flexible, modular component that can interact with various processing units and perform a
range of actions based on its configuration.*

## Properties

- **`description`**: Default: `null`.
  - **Any of**
    - *string*
    - *null*
- **`system_prompt`** *(string)*: Default: `"You are a helpful assistant"`.
- **`agent_refs`** *(array)*: Default: `[]`.
  - **Items** *(string)*
- **`actions`** *(array)*: Default: `[{"name": "converse", "title": null, "sub_title": null, "description": null, "user_prompt": "{{ body }}", "input_schema": {}, "output_schema": "str", "allow_file_upload": false, "supported_mime_types": [], "allowed_states": ["initialized", "idle", "http_error"], "output_state": "idle"}]`.
  - **Items**: Refer to *[#/$defs/ActionDefinition](#%24defs/ActionDefinition)*.
- **`apu`** *([Reference[APU]](/docs/components/apu/overview/))*: Default: `"APU"`.
- **`apus`** *(array)*: Default: `[]`.
  - **Items**: Refer to *[#/$defs/NamedCPU](#%24defs/NamedCPU)*.
- **`title_generation_mode`** *(string)*: Must be one of: `["none", "on_request"]`. Default: `"on_request"`.
- **`doc_processor`** *(Reference[DocumentProcessor])*: Default: `"DocumentProcessor"`.
## Definitions

- <a id="%24defs/ActionDefinition"></a>**`ActionDefinition`** *(object)*: Can contain additional properties.
  - **`name`** *(string)*: Default: `"converse"`.
  - **`title`**: Default: `null`.
    - **Any of**
      - *string*
      - *null*
  - **`sub_title`**: Default: `null`.
    - **Any of**
      - *string*
      - *null*
  - **`description`**: Default: `null`.
    - **Any of**
      - *string*
      - *null*
  - **`user_prompt`** *(string)*: Default: `"{{ body }}"`.
  - **`input_schema`** *(object)*: Can contain additional properties. Default: `{}`.
    - **Additional properties** *(object)*
  - **`output_schema`**: Default: `"str"`.
    - **Any of**
      - *string*: Must be one of: `["str"]`.
      - *object*
  - **`allow_file_upload`** *(boolean)*: Default: `false`.
  - **`supported_mime_types`** *(array)*: Default: `[]`.
    - **Items** *(string)*
  - **`allowed_states`** *(array)*: Default: `["initialized", "idle", "http_error"]`.
    - **Items** *(string)*
  - **`output_state`** *(string)*: Default: `"idle"`.
- <a id="%24defs/NamedCPU"></a>**`NamedCPU`** *(object)*: Can contain additional properties.
  - **`title`**: Default: `null`.
    - **Any of**
      - *string*
      - *null*
  - **`apu`** *([Reference[APU]](/docs/components/apu/overview/))*: Default: `"APU"`.
  - **`default`** *(boolean)*: Default: `false`.
