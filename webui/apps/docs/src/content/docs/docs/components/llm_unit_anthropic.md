---
title: AnthropicLLMUnitSpec
description: Component - AnthropicLLMUnitSpec
---
The `AnthropicLLMUnitSpec` class configures the interaction with Anthropic's LLM models within the Eidolon framework, defaulting on the Claude Opus model. It allows customization of the model's behavior, including temperature settings and token limits.

## Spec

| Key          | Description                                                                                                                                                                                                          |
|--------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| model        | `type`: AnnotatedReference[LLMModel, claude_opus]<br/>`Default`: claude_opus<br/>`Description:` Specifies the Claude Opus model from Anthropic, known for its capabilities in language understanding and generation. |
| temperature  | `type`: float<br/>`Default`: 0.3<br/>`Description:` Sets the creativity of the model's responses. A lower value results in more deterministic and predictable responses.                                             |
| max_tokens   | `type`: Optional[int]<br/>`Default`: None<br/>`Description:` Limits the number of tokens in the model's responses, which is useful for controlling response length or computational load.                            |
| client_args  | `type`: dict<br/>`Default`: {}<br/>`Description:` Allows for the passing of additional arguments to the model client, providing flexibility to customize the model's behavior based on specific requirements.        |
