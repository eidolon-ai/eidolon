
---
title: ClaudeHaiku
description: ClaudeHaiku
---
# ClaudeHaiku

## Properties

- **`max_num_function_calls`** *(integer)*: The maximum number of function calls to make in a single request. Default: `10`.
- **`io_unit`** *(Reference[IOUnit])*: Default: `"IOUnit"`.
- **`memory_unit`** *(Reference[MemoryUnit])*: Default: `"MemoryUnit"`.
- **`llm_unit`** *(Reference[LLMUnit])*: Default: `{"implementation": "AnthropicLLMUnit", "model": "claude-3-haiku-20240307"}`.
- **`logic_units`** *(array)*: Default: `[]`.
  - **Items** *(Reference[LogicUnit])*: Default: `"eidolon_ai_sdk.cpu.logic_unit.LogicUnit"`.
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
