---
title: Using LLM APIs
description: References - How to get started with LLMs and set API keys
---

## LLM Prerequisites

To access their models through APIs, LLM providers may require you to:

- create an account
- acquire an API key
- fund the account
- install the LLM's SDK to work with its APIs

Use the table below to get started with popular LLM providers. Note that each provider has its own terms and conditions regarding account payment and usage pricing.

| LLM | Provider Documentation | Eidolon API_Key attribute |
| --- | --- | --- |
| Claude | [Anthropic Quickstart](https://docs.anthropic.com/en/docs/quickstart)  | ANTHROPIC_API_KEY |
| Mistral | [Mistral AI Quickstart: Account Setup](https://docs.mistral.ai/getting-started/quickstart/#account-setup)<br>[Mistral Python Client](https://docs.mistral.ai/getting-started/clients/) | MISTRAL_API_KEY |
| Ollama | [Ollama Github](https://github.com/ollama/ollama)  | n/a -- you run Ollama locally |
| GPT | [OpenAI Developer Quickstart](https://platform.openai.com/docs/quickstart)  | OPENAI_API_KEY |

## Configuring Eidolon

You may be prompted to enter an API key during an Eidolon installation process, which automatically adds the key to the Eidolon `.env` file. 

To see your Eidolon environment settings:

```console
cd <Eidolon application root directory>
ls -oa
cat .env
```

If the `.env` file does not contain the API key you need for an LLM provider, simply add it to the file using a text editor. 

Restart the Eidolon server. Use the LLM providers' usage and activity tracking tools to confirm success.