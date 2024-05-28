---
title: OpenAIGPT
description: Description of OpenAIGPT component
---
## Properties

- **`model`** *([Reference[LLMModel]](/docs/components/llmmodel/overview/))*: Default: `"gpt-4-turbo"`.
- **`temperature`** *(number)*: Default: `0.3`.
- **`force_json`** *(boolean)*: Default: `true`.
- **`max_tokens`**: Default: `null`.
  - **Any of**
    - *integer*
    - *null*
- **`connection_handler`** *(Reference[OpenAIConnectionHandler])*: Default: `"OpenAIConnectionHandler"`.
