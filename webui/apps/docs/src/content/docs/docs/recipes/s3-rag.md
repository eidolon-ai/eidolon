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

This recipe shows how a chatbot agent working with a RAG agent can use documents stored in an Amazon S3 bucket to find answers to questions.

### Core Concepts

This example highlights the following core concepts:
- [Multi-agent communication](/docs/howto/communication)
- [Configuring Components](/docs/howto/configure_builtins)
- [Dynamic embedding management](/docs/components/retriever_agent)

### Prerequisites
Specific to this example, you need:
- access to an AWS bucket that contains at least one document

If you completed the [Quickstart](/docs/quickstart) you should be all set with the remaining prerequisites. If not, make sure to:
- confirm `make` and `poetry` are installed
- you have a [funded OpenAI account](/docs/howto/authenticate_llm)

## Agents
This example uses two agents: 
- [conversational-agent](https://github.com/eidolon-ai/eidolon-s3-rag/blob/main/resources/conversational_agent.eidolon.yaml): a user-facing copilot that is instantiated from the built-in <a href="/docs/components/agent/simpleagent" target=_blank>SimpleAgent</a>, which is the default agent if none is specified
- [s3-search](https://github.com/eidolon-ai/eidolon-s3-rag/blob/main/resources/s3_search.eidolon.yaml): a RAG agent that is instantiated from the built-in <a href="/docs/components/agent/retrieveragent" target-_blank>RetrieverAgent</a>

| Note: you can name agents as you wish. You can use hyphens (dashes) but not underscores in agent names.

### Conversational Agent: the user-facing copilot

Resources of kind Agent can use an LLM to:
- reason
- converse with you and other agents

```yaml
apiVersion: server.eidolonai.com/v1alpha1
kind: Agent
metadata:
  name: conversational-agent
```
The conversational-agent can delegate tasks to the s3-search agent. This relationship is configured through [agent_refs](/docs/components/agent/simpleagent#agent_refs), which is a property specified ("spec'd") by SimpleAgent.

Typically, you would reference elements of an array on separate lines, with each element preceded by a hyphen (dash). In this example, the array has one element: `s3-search`.
```yaml
spec:
  agent_refs:
  -  s3-search
```

Note that the elements in this array are of type string (as opposed to objects). You can use a shorthand mechanism that is built into SimpleAgent for a more compact presentation. 
```yaml
spec:
  agent_refs: [s3-search]
```

### S3 Search: the RAG agent that searches documents

The s3-search agent's job is to load, embed, and re-embed documents that may change frequently.

This agent also translates requests (in this case, from the conversational-agent) into a vector search query and returns the top results.

```yaml
apiVersion: server.eidolonai.com/v1alpha1
kind: Agent
metadata:primary 
  name: s3-search

spec:
  implementation: RetrieverAgent
  name: "agentic-papers"
  description: "Search curated papers on building Agentic AI"
```

RetrieverAgent, upon which the s3-agent is instantiated, uses a default loader that reads files from disk. We can override this default by specifying the built-in S3Loader instead.

```yaml
  document_manager:
    loader:
      implementation: S3Loader
      bucket: agentic-papers
      region_name: us-east-2
```
| Note: See the description for the [RetrieverAgent](/docs/components/agent/retrieveragent) regarding volume processing. To process a large body of data, you will want to set up an ingestion pipeline.

## Try it out!

1. First clone Eidolon's chatbot repository.

```bash
git clone https://github.com/eidolon-ai/eidolon-s3-rag.git
cd eidolon-s3-rag
```

2. Use a text editor to add your LLM API key and AWS keys to a plain-text `.env` file, e.g.:

```text
OPENAI_API_KEY=your_openai_key
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_access_key
```
3. Change the `bucket` and `region_name`

```yaml title=s3_search.eidolon.yaml
    loader:
      implementation: S3Loader
      bucket: agentic-papers # change to a bucket you can access with your AWS keys
      region_name: us-east-2 # change to the region that hosts the s3 bucket
```

4. Start your server.
```bash
make docker-serve  # or sudo make docker serve; launches agent server and webui
```

5. Use the online [dev tool ui](http://localhost:3000/) in your browser. As you converse with the chatbot, it can retrieve information from the S3 buckets before responding back to you.
