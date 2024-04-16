# Azure OpenAI Configuration Guide

This guide provides detailed steps on how to use Azure OpenAI deployments for your application with either a static token or a token provider.

## Step 0: Prerequisites

To get started you will need an Azure OpenAI deployment, the deployment endpoint, and a deployed Azure OpenAI model.

## Step 1: Configure Eidolon

The first thing we need to do is create a resource in Eidolon to configure our openai client to use Azure OpenAI by default.

```yaml
apiVersion: eidolon/v1
kind: Reference
metadata:
  name: OpenAIConnectionHandler
spec:
  implementation: AzureOpenAIConnectionHandler
  azure_endpoint: https://testinstancename.openai.azure.com/
```

### Static Token Authentication

If you are using a token, you can set it as an environment variable ```AZURE_OPENAI_API_KEY```

Alternatively you can set the key within the AzureOpenAIConnectionHandler resource.
```yaml
spec:
  implementation: AzureOpenAIConnectionHandler
  api_key: $YOUR_API_KEY
```

### Token Provider Authentication

If you use a token provider, Eidolon supports the EnvironmentCredential out of the box, and will automatically use it if 
`AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET`, and `AZURE_TENANT_ID` are set as environment variables.

Alternatively you can manually configure your azure_ad_token_provider within your AzureOpenAIConnectionHandler resource:

```yaml
spec:
  implementation: AzureOpenAIConnectionHandler
  azure_ad_token_provider: EnvironmentCredential
```

## Step 2: Configure your Agent

Unless you named your model directly after it's openai equivalent, you will need to specify the model name in your 
agent's apu configuration. 

```yaml
apiVersion: eidolon/v1
kind: Agent
metadata:
  name: hello_world

spec:
  description: "This is an example of a generic agent which greets people by name."
  system_prompt: "You are a friendly greeter who greets people by name while using emojis"
  apu:
    llm_unit:
      model:
        name: YOUR_MODEL_NAME
```
