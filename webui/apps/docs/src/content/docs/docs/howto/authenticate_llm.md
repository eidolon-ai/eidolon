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
| Claude | [Anthropic Quickstart](https://docs.anthropic.com/en/docs/quickstart)  | ANTHROPIC_API_KEY |
| Mistral | [Mistral AI Quickstart: Account Setup](https://docs.mistral.ai/getting-started/quickstart/#account-setup) | MISTRAL_API_KEY |
| Ollama | [Ollama Github](https://github.com/ollama/ollama)  | n/a -- you run Ollama locally |
| ChatGPT | [OpenAI Developer Quickstart](https://platform.openai.com/docs/quickstart)  | OPENAI_API_KEY |

## Setting Your LLM API Keys

If you are prompted to enter an API key during an Eidolon installation process, it will automatically be added to the Eidolon `.env` file. 

To see your Eidolon environment settings:

```console
cd <Eidolon application root directory>
cat .env
```

If the `.env` file does not exist, create it as a plain text file. 

If the `.env` file does not contain the API key you need for an LLM provider, simply add it to the file. 

Example:

```console
OPENAI_API_KEY=youropenaiapikey
ANTHROPIC_API_KEY=youranthropicapikey
MISTRAL_API_KEY=yourmistralapikey
```

Restart the Eidolon server. Eidolon agents can now authenticate with your preferred LLMs.