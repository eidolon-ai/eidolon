---
title: How to Authenticate with Your LLM
description: Reference - How to get started with LLMs and set API keys
---

## LLM Prerequisites

To access LLM models through Eidolon, you may need to:

- Create an account with the LLM provider
- Fund the account
- Acquire an API key

Note that each provider has its own terms and conditions regarding account payment and usage pricing.

Use the table below to get started with popular LLM providers. 

| LLM | Provider Documentation | Eidolon API_Key attribute |
| --- | --- | --- |
| Claude | <a href="https://docs.anthropic.com/en/docs/quickstart" target=_blank>Anthropic Quickstart</a>  | ANTHROPIC_API_KEY |
| Mistral | <a href="https://docs.mistral.ai/getting-started/quickstart/#account-setup" target=_blank>Mistral AI Quickstart: Account Setup</a> | MISTRAL_API_KEY |
| Ollama | <a href="https://github.com/ollama/ollama" target=_blank>Ollama Github</a> | n/a -- you run Ollama locally |
| ChatGPT | <a href="https://platform.openai.com/docs/quickstart" target=_blank>OpenAI Developer Quickstart</a>  | OPENAI_API_KEY |

## Prompts During Installations

If you are prompted to enter an API key during an installation process, it will automatically be added to the Eidolon `.env` file. 

To see your Eidolon environment settings:

```console
cd <Eidolon application root directory>
cat .env
```
## Setting New LLM API Keys

If you want to [use a new LLM](/docs/howto/swap_llm), you may need to enter an API Key to the `.env` file. See [LLM Prerequisites](#llm-prerequisites) to learn about authenticating with various providers.

Example `.env` file:

```text
OPENAI_API_KEY=youropenaiapikey
ANTHROPIC_API_KEY=youranthropicapikey
MISTRAL_API_KEY=yourmistralapikey
```

Restart Eidolon. Agents can now authenticate with your preferred LLMs.

>Note: if the `.env` file does not exist in your application root directory, create it as a plain text file. 