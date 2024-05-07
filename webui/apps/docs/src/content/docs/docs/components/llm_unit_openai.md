---
title: OpenAiGPTSpec
description: Component - OpenAiGPTSpec
---
The `OpenAiGPTSpec` class is designed to configure and manage the interaction with OpenAI's GPT models within the Eidolon framework. This specification allows for customization of the GPT model behavior, including temperature settings, token limits, and JSON formatting preferences.

## Spec

| Key                | Description                                                                                                                                                                                                                      |
|--------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| model              | `type`: Reference[LLMModel]<br/>`Default`: Reference[gpt_4]<br/>`Description:` Specifies the GPT model to use, typically configured to use GPT-4 for its advanced capabilities in language understanding and generation.     |
| temperature        | `type`: float<br/>`Default`: 0.3<br/>`Description:` Sets the creativity of the model's responses. A lower value makes the model's responses more deterministic and predictable.                                                  |
| force_json         | `type`: bool<br/>`Default`: True<br/>`Description:` Forces the model to output responses in JSON format, facilitating easier parsing and integration within digital systems.                                                     |
| max_tokens         | `type`: Optional[int]<br/>`Default`: None<br/>`Description:` Limits the number of tokens in the model's responses, useful for controlling response length or computational load.                                                 |
| connection_handler | `type`: Reference[OpenAIConnectionHandler]<br/>`Default`: Reference[OpenAIConnectionHandler]<br/>`Description:` Manages the connection to the OpenAI API, ensuring secure and efficient communication with the service. |


###
