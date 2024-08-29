---
title: Using LLM APIs
description: References - How to get started with and set LLM provider API keys
---

## LLM Prerequisites

For various LLM providers you wish to use, you may need to:

- create an account
- acquire an API key
- install the LLM's SDK to work with its APIs
- fund the account

Use the table below to get started with popular LLM providers. Note that each provider has its own terms and conditions regarding account payment and usage pricing.

| LLM | Provider Documentation | Eidolon API_Key attribute |
| --- | --- | --- |
| Claude | [Getting Started with Anthropic](https://docs.anthropic.com/en/api/getting-started)  | ANTHROPIC_API_KEY |
| Mistral | [Mistral AI Quickstart: Account Setup](https://docs.mistral.ai/getting-started/quickstart/#account-setup)  | MISTRAL_API_KEY |
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