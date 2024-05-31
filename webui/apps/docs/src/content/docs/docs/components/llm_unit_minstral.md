---
title: MistralGPTSpec
description: Component - MistralGPTSpec
---
The `MistralGPTSpec` class configures the interaction with Mistral's GPT models within the Eidolon framework, defaulting to the Mistral Large model. It allows customization of the model's behavior, including temperature settings, JSON formatting, and token limits.

## Spec

| Key          | Description                                                                                                                                                                                                          |
|--------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| model        | `type`: AnnotatedReference[LLMModel, mistral_large]<br/>`Default`: mistral_large<br/>`Description:` Specifies the Mistral Large model, known for its advanced capabilities in language understanding and generation. |
| temperature  | `type`: float<br/>`Default`: 0.3<br/>`Description:` Sets the creativity of the model's responses. A lower value results in more deterministic and predictable responses.                                             |
| force_json   | `type`: bool<br/>`Default`: True<br/>`Description:` Forces the model to output responses in JSON format, facilitating easier parsing and integration within digital systems.                                         |
| max_tokens   | `type`: Optional[int]<br/>`Default`: None<br/>`Description:` Limits the number of tokens in the model's responses, which is useful for controlling response length or computational load.                            |
| client_args  | `type`: dict<br/>`Default`: {}<br/>`Description:` Allows for the passing of additional arguments to the model client, providing flexibility to customize the model's behavior based on specific requirements.        |