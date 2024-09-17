---
title: Chatbot
description: Create a multi-media chatbot powered by the llm of your choice
---

<div>
  <a href="https://github.com/eidolon-ai/eidolon-chatbot">
    <img style="display: inline-block;" alt="GitHub Repository" src="https://img.shields.io/badge/eidolon-Chatbot-blue?style=flat&logo=github">
  </a>
  <a href="https://github.com/eidolon-ai/eidolon-chatbot/fork">
    <img style="display: inline-block;" alt="GitHub Forks" src="https://img.shields.io/badge/fork-grey?style=flat&logo=forgejo&logoColor=white">
  </a>
</div>


This Recipe shows an example of a multi-llm multimedia enabled chatbot. 

Not all LLMs support multimedia, let alone 
mid-conversation brain-boosts. This can cause issues when swapping out components. 

Eidolon's AgentProcessingUnit abstracts away those concepts so you can enable multimedia, json output, and function 
calling on even the smallest LLM.

<iframe width="720"
src="https://www.youtube.com/embed/8GOsbX8Hs50">
</iframe>

## Core Concepts
###### [How to Configure Built-in Components](/docs/howto/configure_builtins)

## Agents
### [Conversational Agent](https://github.com/eidolon-ai/eidolon-chatbot/blob/main/resources/conversational_agent.yaml)
This uses the [SimpleAgent](/docs/components/agents/simpleagent) template, but needs some customization to enable file uploads and support multiple LLMs. 

You will notice that enabled file upload on our AgentProcessingUnit's primary action.
```yaml
  actions:
    - name: "converse"
      description: "A copilot that engages with the user."
      allow_file_upload: true
```


We also have a list of available [APUs](/docs/components/apu/overview) in resources/apus.yaml.
```yaml
  apus:
    - apu: MistralSmall
      title: Mistral Small
    - apu: MistralMedium
      title: Mistral Medium
    - apu: MistralLarge
...
```

We did not need to make any customization to support multimedia within the APU, this is turned on by default 🚀.

## Try it out!
First let's fork for Eidolon's chatbot repository, clone it to your local machine, and start your server.
```bash
git clone https://github.com/eidolon-ai/eidolon-chatbot.git
cd eidolon-chatbot
make docker-serve  # launches agent server and webui
```

Now Head over to the [chatbot ui](http://localhost:3000/eidolon-apps/sp/chatbot) in your favorite browser and start chatting with your new agent.

