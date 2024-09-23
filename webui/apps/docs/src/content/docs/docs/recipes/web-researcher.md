---
title: Web Researcher
description: Create a multi-media chatbot powered web-researcher using the llm of your choice
---

<div>
  <a href="https://github.com/eidolon-ai/web-researcher">
    <img style="display: inline-block;" alt="GitHub Repository" src="https://img.shields.io/badge/eidolon-Chatbot-blue?style=flat&logo=github">
  </a>
  <a href="https://github.com/eidolon-ai/web-researcher/fork">
    <img style="display: inline-block;" alt="GitHub Forks" src="https://img.shields.io/badge/fork-grey?style=flat&logo=forgejo&logoColor=white">
  </a>
</div>


This Recipe shows an example of a web researcher chatbot. 

## Core Concepts
###### [How to Configure Built-in Components](/docs/howto/configure_builtins)

## Agents
#### [Conversational Agent](https://github.com/eidolon-ai/web-researcher/blob/main/resources/conversational_agent.yaml)
This uses the SimpleAgent template, but needs some customization to enable file uploads and support multiple LLMs. 
#### [Speech Agent](https://github.com/eidolon-ai/web-researcher/blob/main/resources/speech_agent.yaml)
This uses the builtin AutonomousSpeechAgent to enable speech-to-text capabilities. 
#### [Web Researcher](https://github.com/eidolon-ai/web-researcher/blob/main/resources/web_research.yaml)
This is the researcher agent. Customize the prompts, search parameters, etc... to suit your needs. 

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
First let's fork for Eidolon's web researcher repository, clone it to your local machine, and start your server.
```bash
git clone https://github.com/eidolon-ai/web-researcher.git
cd web-researcher
```

Then run the server and webui in dev mode, use the following command:

```bash
make docker-serve
```

<small>
⚠️ The first time you run this command, you may be prompted to enter credentials that the machine needs
to run (ie, OpenAI API Key, Google CSE key, and Google CSE Token). These resources will be saved in the `.env` file in 
the project root.
</small>

---

If the server starts successfully, you should see the following output:
```
Starting Server...
INFO:     Started server process [34623]
INFO:     Waiting for application startup.
INFO - Building machine 'local_dev'
...
INFO - Server Started in 1.50s
```

Now Head over to the [chatbot ui](http://localhost:3000/eidolon-apps/sp/chatbot) in your favorite browser and start chatting with your new agent.

