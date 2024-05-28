---
title: MistralMedium
description: Description of MistralMedium component
---
## Properties

- **`max_num_function_calls`** *(integer)*: The maximum number of function calls to make in a single request. Default: `10`.
- **`io_unit`** *(Reference[IOUnit])*: Default: `"IOUnit"`.
- **`memory_unit`** *(Reference[MemoryUnit])*: Default: `"MemoryUnit"`.
- **`llm_unit`** *([Reference[LLMUnit]](/docs/components/llmunit/overview/))*: Default: `{"implementation": "MistralGPT", "model": "mistral-medium-latest"}`.
- **`logic_units`** *(array)*: Default: `[]`.
  - **Items** *([Reference[LogicUnit]](/docs/components/logicunit/overview/))*: Default: `"eidolon_ai_sdk.cpu.logic_unit.LogicUnit"`.
- **`audio_unit`**: Default: `null`.
  - **Any of**
    - *Reference[AudioUnit]*: Default: `"eidolon_ai_sdk.cpu.audio_unit.AudioUnit"`.
    - *null*
- **`image_unit`**: Default: `null`.
  - **Any of**
    - *Reference[ImageUnit]*: Default: `"eidolon_ai_sdk.cpu.image_unit.ImageUnit"`.
    - *null*
- **`record_conversation`** *(boolean)*: Default: `true`.
- **`allow_tool_errors`** *(boolean)*: Default: `true`.
- **`document_processor`** *(Reference[DocumentProcessor])*: Default: `"DocumentProcessor"`.
