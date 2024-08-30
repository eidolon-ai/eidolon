---
title: LLM Authentication
description: References - How to get started with LLMs and set API keys
---

## LLM Prerequisites

To access an LLM provider's API, you may need to:

- create an account
- acquire an API key
- fund the account

> Note: You do not need to install the provider's SDK to use Eidolon.

Use the table below to get started with popular LLM providers. Note that each provider has its own terms and conditions regarding account payment and usage pricing.

| LLM | Provider Documentation | Eidolon API_KEY attribute |
| --- | --- | --- |
| Claude | [Anthropic API Keys](https://console.anthropic.com/settings/keys) and [billing](https://console.anthropic.com/settings/plans)  | ANTHROPIC_API_KEY |
| Mistral | [Mistral AI API Keys](https://console.mistral.ai/api-keys/) and [billing](https://console.mistral.ai/billing/)| MISTRAL_API_KEY |
| Ollama | [Ollama Github](https://github.com/ollama/ollama)  | n/a -- you run Ollama locally |
| GPT | [OpenAI API Keys](https://platform.openai.com/api-keys) and [billing](https://platform.openai.com/settings/organization/billing/overview) | OPENAI_API_KEY |

## Configuring Eidolon

You may be prompted to enter an API key during an Eidolon installation process, which automatically adds the key to the Eidolon `.env` file. 

To see your Eidolon environment settings:

```console
cd <Eidolon application root directory>
cat .env
```

If the `.env` file does not contain the API key you need for an LLM provider, simply add it to the file using a text editor. 

Restart the Eidolon server. Use the LLM providers' usage and activity tracking tools to confirm success.
