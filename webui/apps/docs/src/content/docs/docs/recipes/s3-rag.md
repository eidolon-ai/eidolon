---
title: S3 RAG
description: Create a S3 RAG agent that dynamically embeds and retrieves documents from an S3 bucket
---

<div>
  <a href="https://github.com/eidolon-ai/eidolon-s3-rag">
    <img style="display: inline-block;" alt="GitHub Repository" src="https://img.shields.io/badge/eidolon-S3%20RAG-blue?style=flat&logo=github">
  </a>
  <a href="https://github.com/eidolon-ai/eidolon-s3-rag/fork">
    <img style="display: inline-block;" alt="GitHub Forks" src="https://img.shields.io/badge/fork-grey?style=flat&logo=forgejo&logoColor=white">
  </a>
</div>


In this recipe we have created a RAG chatbot powered by documents living in s3.

It dynamically pulls in information via similarity search to answer user queries.

This is important if you have a body of information that is constantly changing, but you need real time information about (ie, a git repository).

## Core Concepts
###### [Multi-agent communication](/docs/howto/communication)
###### [Sub-component customization](/docs/howto/communication)
###### [Dynamic embedding management](/docs/components/retriever_agent)

## Agents
### [Conversational Agent](https://github.com/eidolon-ai/eidolon-s3-rag/blob/main/resources/conversational_agent.yaml)
The user facing copilot. Ask this agent questions and it use the llm to provide answers while reaching out to the S3
Search Agent as needed for relevant documents as needed assistance of the repo search agent.

The SimpleAgent template defines a shorthand mechanism to add an agent as a logic unit. Just add the downstream agent 
to the `agent_refs` list.
```yaml
agent_refs: [s3_search]
```

### [S3 RAG](https://github.com/eidolon-ai/eidolon-s3-rag/blob/main/resources/repo_search.yaml)
Handles loading, embedding, and re-embedding documents ensuring they are up-to-date.

Translates queries into a vector search query and returns the top results.

You will notice that this agent uses the RetrieverAgent template. By default, this template is defined to use 
a loader that reads files from disk, but Eidolon has a GitHub loader built in that we can use.
```yaml
  document_manager:
    loader:
      implementation: S3Loader
      bucket: agentic-papers
      region_name: us-east-2
      aws_access_key_id: ####
      aws_secret_access_key: ####
```

## Try it out!

First clone Eidolon's chatbot repository and then start your server.
```bash
git clone https://github.com/eidolon-ai/eidolon-s3-rag.git
cd eidolon-s3-rag
make docker-serve  # launches agent server and webui
```

🚨make sure you set your tokens

Now you can interact with the Repo Expert via the Eidolon UI or the CLI.



Now Head over to the [dev tool ui](http://localhost:3000/eidolon-apps/dev-tool) in your favorite browser and start chatting with your new agent.
