# Azure OpenAI Configuration Guide

This guide provides detailed steps on how to use Azure OpenAI deployments for your application with either a static token or a token provider.

## Step 0: Prerequisites

To get started you will need an Azure OpenAI deployment, the deployment endpoint, and a deployed Azure OpenAI model.

## Step 1: Configure Eidolon AzureOpenAIConnectionHandler

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

### Authentication
You have two approaches for authentication, static tokens or using a token provider. Eidolon supports both. All you 
need to do is set the respective environment variables and Eidolon will automatically configure the client.

#### Static Token Authentication

If you are using a token, you can set it as an environment variable ```AZURE_OPENAI_API_KEY```

#### Token Provider Authentication

Eidolon will automatically use the EnvironmentCredential if the environment variables 
`AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET`, and `AZURE_TENANT_ID` are set.


## Step 2: Configure Eidolon Model(s) 

We still need to override our model to point to the Azure OpenAI deployment. We can do this by overriding the default 
gpt-4 model.

Since this is the model used by default, your agents will automatically use it. You will need to similarly customize any 
additional models used by your Eidolon Machine.

```yaml
apiVersion: eidolon/v1
kind: Reference
metadata:
  name: "gpt-4-turbo-preview"
spec:
  name: YOUR_MODEL_NAME
```
