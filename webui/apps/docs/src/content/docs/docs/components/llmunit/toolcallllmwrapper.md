---
title: ToolCallLLMWrapper
description: Description of ToolCallLLMWrapper component
---
## Properties

- **`tool_message_prompt`** *(string)*: Default: `"You must follow these instructions:\nYou can select zero or more of the above tools based on the user query\nIf there are multiple tools required, make sure a list of tools are returned in a JSON array.\nIf there is no tool that match the user request or you have already answered the question, you will respond with empty json array for the tools.\nYou can also add any additional notes or explanations in the notes field."`.
- **`llm_unit`** *([Reference[LLMUnit]](/docs/components/llmunit/overview/))*: Default: `"LLMUnit"`.
- **`model`**: Default: `null`.
  - **Any of**
    - *[Reference[LLMModel]](/docs/components/llmmodel/overview/)*: Default: `"eidolon_ai_sdk.cpu.llm_unit.LLMModel"`.
    - *null*
