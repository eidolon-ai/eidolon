---
title: Azure Agent
description: Create agent backed by an LLM deployed in Azure
---

<div>
  <a href="https://github.com/eidolon-ai/azure-llm">
    <img style="display: inline-block;" alt="GitHub Repository" src="https://img.shields.io/badge/eidolon-azure-llm?style=flat&logo=github">
  </a>
  <a href="https://github.com/eidolon-ai/azure-llm/fork">
    <img style="display: inline-block;" alt="GitHub Forks" src="https://img.shields.io/badge/fork-grey?style=flat&logo=forgejo&logoColor=white">
  </a>
</div>


This Recipe shows an example of a web researcher chatbot. 

## Core Concepts
###### [How to Configure Built-in Components](/docs/howto/configure_builtins)

## Prerequisites
### Azure account with OpenAI access
If you do not have one already, sign up for an [azure acount](https://azure.microsoft.com/en-us/products/ai-services/openai-service) and get access to the OpenAI API.

### Cloned [Azure LLM Example Repository](https://github.com/eidolon-ai/azure-llm)
Clone the Azure LLM example repo locally and work from the project's root directory
```bash
https://github.com/eidolon-ai/azure-llm.git
cd azure-llm
```

## Setup
### 1. Create an [Azure OpenAPI Resource](https://ai.azure.com/resource)
Head over to the [Azure OpenAPI Resource](https://ai.azure.com/resource) page to deploy a new resource (In this demo we used `custom-azure-deployment`).

Get `Key` and add it to .env as AZURE_OPENAI_API_KEY

```bash
# make .env will prompt you for AZURE_OPENAI_API_KEY and write it to .env
make .env
```

🚨 Also note the `Endpoint` value. We will use this to update the `azure_endpoint` field in `azure_agent.eidolon.yaml` later.

### 2. Deploy a Model
Create an Azure [deployment](https://ai.azure.com/resource/deployments) for your resource a model named (in this demo we named our deployment `custom-azure-deployment`).

### 3. Create an APU for your model.
Create a new APU resource in the `resources` directory. This APU will point to your Azure LLM deployment and will be used by your agent to interact with the LLM.

```yaml
# resources/azure_4o_apu.eidolon.yaml
apiVersion: server.eidolonai.com/v1alpha1
kind: Reference
metadata:
  name: azure-gpt4o

spec:
  implementation: GPT4o
  llm_unit:
    implementation: "AzureLLMUnit"
    azure_endpoint: https://eidolon-azure.openai.azure.com  # resource azure endpoint
    model:
      name: custom-azure-deployment  # your custom deployment name
```

> 👉 **Note:** both the `spec.llm_unit.azure_endpoint` and `spec.llm_unit.model.name` fields should be updated with the values you got from the Azure portal.

<details>
<summary>The example agent already points to this apu.</summary>

```yaml
# resources/azure_agent.eidolon.yaml
apiVersion: server.eidolonai.com/v1alpha1
kind: Agent
metadata:
   name: hello-world

spec:
   implementation: SimpleAgent
   apu:
      implementation: azure-gpt4o  # points to your apu resource
```
</details>

## Testing your Azure Agent
To verify your deployment is working, run the tests in "record-mode" and see if they pass:
```bash
make test ARGS="--vcr-record=all"
```

<details>
<summary>What's up with the `--vcr-record=all` flag? 🤔</summary>

> Eidolon is designed so that you can write cheap, fast, and deterministic tests by leveraging pyvcr.
>
> This records http request/responses between test runs so that subsequent calls never actually need to
go to your llm. These recordings are stored as `cassette` files.
>
> This is normally great, but it does mean that when you change your config these cassettes are no longer valid.
> `--vcr-record=all` tells pyvcr to ignore existing recordings and re-record them again using real http requests.
</details>


## Try it out!
If your tests are passing, try chatting with your agent using the Eidolon webui:

First start the backend server + webui
```bash
make docker-serve
```

then visit the [webui](http://localhost:3000/) and start experimenting!


