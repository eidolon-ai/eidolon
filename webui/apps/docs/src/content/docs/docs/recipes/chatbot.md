---
title: Chatbot
description: Create a multi-media chatbot powered by the llm of your choice
---

[![GitHub](https://img.shields.io/badge/eidolon-Chatbot-blue?style=flat&logo=github)](https://github.com/eidolon-ai/eidolon-chatbot)

[![Static Badge](https://img.shields.io/badge/fork-grey?style=flat&logo=forgejo&logoColor=white)](https://github.com/eidolon-ai/eidolon-chatbot/fork)



This Recipe shows an example of a multi-llm multimedia enabled chatbot. 

Not all LLMs support multimedia, let alone 
mid-conversation brain-boosts. This can cause issues when swapping out components. 

Eidolon's AgentProcessingUnit abstracts away those concepts so you can enable multimedia, json output, and function 
calling on even the smallest LLM.

<iframe width="720"
src="https://www.youtube.com/embed/8GOsbX8Hs50">
</iframe>

## Core Concepts
<li>Customizing the AgentProcessingUnit</li>
<li>Running the UI</li>

## Agents
### [Conversational Agent](https://github.com/eidolon-ai/eidolon-chatbot/blob/main/resources/conversational_agent.yaml)
This uses the SimpleAgent template, but needs some customization to enable file uploads and support multiple LLMs. 

You will notice that enabled file upload on our AgentProcessingUnit's primary action.
```yaml
  actions:
    - name: "converse"
      description: "A copilot that engages with the user."
      allow_file_upload: true
```


We also have a list of available APUs in resources/apus.yaml.
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
gh repo fork eidolon-ai/eidolon-chatbot --clone=true
cd eidolon-chatbot
make serve-dev
```

Next let's run the ui locally.
```bash
docker run -e "EIDOLON_SERVER=http://host.docker.internal:8080" -p 3000:3000 eidolonai/webui:latest
```

Now Head over to the [chatbot ui](http://localhost:3000/eidolon-apps/sp/chatbot) in your favorite browser and start chatting with your new agent.

