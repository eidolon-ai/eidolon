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
###### [Customizing the AgentProcessingUnit](http://localhost:4321/docs/references/pluggable)
###### [Running the UI](/docs/references/webui)

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
First let's fork for Eidolon's web researcher repository, clone it to your local machine, and start your server.
```bash
git clone https://github.com/eidolon-ai/web-researcher.git
cd web-researcher
```

Then run the server in dev mode, use the following command:

```bash
make serve-dev
```

**WARNING:** By default the server is running in dev mode which does not persist the machine state between restarts. 
To start the server in non-dev mode, use the following command:

```bash
  make serve
```

This will assume mongodb is running locally on the default port. If you need to connect to a different mongodb instance,
you can set the `MONGO_CONNECTION_STR` and `MONGO_DATABASE_NAME` environment variables to the appropriate connection string.

The first time you run this command, you may be prompted to enter credentials that the machine needs 
to run (ie, OpenAI API Key, Google CSE key, and Google CSE Token).

These resources will be saved in the `.env` file in the project root.

To use other LLM services, you will need to add the appropriate credentials to the `.env` file in the project root. 
(ie, ANTHROPIC_API_KEY, MISTRAL_API_KEY, OLLAMA_URL, etc.)

This command will download the dependencies required to run your agent machine and start the Eidolon http server in 
"dev-mode".

If the server starts successfully, you should see the following output:
```
Starting Server...
INFO:     Started server process [34623]
INFO:     Waiting for application startup.
INFO - Building machine 'local_dev'
...
INFO - Server Started in 1.50s
```

Next let's run the ui locally.
```bash
docker run -e "EIDOLON_SERVER=http://host.docker.internal:8080" -p 3000:3000 eidolonai/webui:latest
```

Now Head over to the [chatbot ui](http://localhost:3000/eidolon-apps/sp/chatbot) in your favorite browser and start chatting with your new agent.

