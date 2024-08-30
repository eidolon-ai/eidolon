---
title: Git Search
description: Create a github RAG agent that can answer questions about a git repository
---

<div>
  <a href="https://github.com/eidolon-ai/eidolon-git-search">
    <img style="display: inline-block;" alt="GitHub Repository" src="https://img.shields.io/badge/eidolon-Git%20Search-blue?style=flat&logo=github">
  </a>
  <a href="https://github.com/eidolon-ai/eidolon-git-search/fork">
    <img style="display: inline-block;" alt="GitHub Forks" src="https://img.shields.io/badge/fork-grey?style=flat&logo=forgejo&logoColor=white">
  </a>
</div>


In this recipe we have created a GitHub copilot who can answer questions about the Eidolon monorepo.

It dynamically pulls in information via similarity search to answer user queries.

This is important if you have a body of information that is constantly changing, but you need real time information about (ie, a git repository).

<iframe width="720"
src="https://www.youtube.com/embed/INOjIWMX4mY">
</iframe>

## Core Concepts
###### [Multi-agent communication](/docs/howto/communication)
###### [Sub-component customization](/docs/howto/communication)
###### [Dynamic embedding management](/docs/components/retriever_agent)

## Agents
### [Repo Expert](https://github.com/eidolon-ai/eidolon-git-search/blob/main/resources/repo_expert.yaml)
The user facing copilot. Ask this agent questions about a repository, and it will go and find the answer with the
assistance of the repo search agent. It needs to be able to communicate with the repo search agent to get the 
information it needs.

The SimpleAgent template defines a shorthand mechanism to add an agent as a logic unit. Just add the downstream agent 
to the `agent_refs` list.
```yaml
agent_refs: [repo_search]
```

### [Repo Search](https://github.com/eidolon-ai/eidolon-git-search/blob/main/resources/repo_search.yaml)
Handles loading, embedding, and re-embedding documents ensuring they are up-to-date.

Translates queries into a vector search query and returns the top results.

You will notice that this agent uses the RetrieverAgent template. By default, this template is defined to use 
a loader that reads files from disk, but Eidolon has a GitHub loader built in that we can use.
```yaml
  document_manager:
    loader:
      implementation: GitHubLoader
      owner: "eidolon-ai"
      repo: "eidolon"
      pattern:
        - "examples/**/getting_started/**/*.yaml"
        - "examples/**/git_search/**/*.yaml"
        - "**/*.md"
        - "**/*.py"
      exclude: "**/test/**/*"
```
💡Notice that we only care about certain types of files in the repository, and we exclude test files.

## Try it out!

First let's fork for Eidolon's chatbot repository, clone it to your local machine, and start your server.
```bash
git clone https://github.com/eidolon-ai/eidolon-git-search.git
cd eidolon-git-search
make docker-serve  # launches agent server and webui
```

🚨 make sure you set your github token, otherwise you will hit rate limit errors

Now you can interact with the Repo Expert via the Eidolon UI or the CLI. For this example let's launch the UI.

Now Head over to the [eidolon ui](http://localhost:3000) in your favorite browser and start chatting with your new agent.
