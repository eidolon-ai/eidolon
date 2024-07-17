---
title: Quickstart
description: Walk through prequisites for Mac and Linux
---

<div>
  <a href="https://github.com/eidolon-ai/eidolon-quickstart">
    <img style="display: inline-block;" alt="GitHub Repository" src="https://img.shields.io/badge/eidolon-Quickstart-blue?style=flat&logo=github">
  </a>
  <a href="https://github.com/eidolon-ai/eidolon-quickstart/fork">
    <img style="display: inline-block;" alt="GitHub Forks" src="https://img.shields.io/badge/fork-grey?style=flat&logo=forgejo&logoColor=white">
  </a>
</div>

Welcome to the Eidolon Quickstart guide. This section covers environment setup, installing **Eidolon**, creating your first **AgentProgram**, and running an **AgentMachine**.

## Setup Dev Environment

We know you are excited about creating your first agent, but first let's make sure we have everything we need to get started.

##### [OpenAI API Key](https://platform.openai.com/account/api-keys "Create an OpenAI key") 
You should have an envrionment variable OPENAI_API_KEY set to your OpenAI API.
Create a new key on [openai.com](https://platform.openai.com/api-keys) if you don't have one already.

##### [Docker Daemon](https://docs.docker.com/get-docker/ "Install Docker")
Eidolon uses Docker to run your agent machine. Make sure you have Docker installed on your machine.
Visit the [docs.docker.com](https://docs.docker.com/get-docker/) if for instructions installing Docker.


## Run Eidolon Quickstart

First let's clone Eidolon's quickstart repository, clone it to your local machine.

```bash
git clone https://github.com/eidolon-ai/eidolon-quickstart.git
cd eidolon-quickstart
```

Next run the server in dev mode.

```bash
make docker-serve
```

This command will download the dependencies required to run your agent machine and start the Eidolon http server in 
"dev-mode".

🔎 The first time you run this command, you may be prompted to enter credentials that the machine needs to run 
(ie, OpenAI API Key).

If the server starts successfully, you should see the following output:
```
Starting Server...
INFO:     Started server process [34623]
INFO:     Waiting for application startup.
INFO - Building machine 'local_dev'
...
INFO - Server Started in 1.50s
```

You can also check out your machine's [swagger docs](http://localhost:8080/docs#/).

Believe it or not, you are already up and running with a simple agent! 🎉

🚨 Running into problems? Ask for help on [Discord](https://discord.com/invite/6kVQrHpeqG).

## What just happened?

The repository you just cloned defines an **AgentMachine** 💻 with a single **AgentProgram** 🤖 named `hello_world` 👋.

The agent 🤖 is defined in a yaml file 📄 located at `resources/hello_world_agent.yaml`.

This file describes how to instantiate your agent from its **AgentTemplate** 🏭 and describes any customization you might
want (like a custom LLM. tools, etc).

```yaml
apiVersion: eidolon/v1
kind: Agent
metadata:
  name: hello_world

spec:
  description: "This is an example of a agent using the 'SimpleAgent' template."
  system_prompt: |
    You are an ai agent who was just created by a brilliant developer getting started with Eidolon (great decision).
    You love emojis and use them liberally.
```

### Try it out!

Now that your server is running, let's open a new terminal window and interact with it.

#### 1. First download the Ediolon CLI
```bash
pip install 'eidolon-ai-client[cli]' -U
```

#### 2. Then create an AgentProcess
```bash
export PID=$(eidolon-cli processes create --agent hello_world); echo $PID
```
🔬 _a process defines the boundaries of an agent's memory._

#### 3. Converse with your agent
```bash
eidolon-cli actions converse --process-id $PID --body "Hi! I made you"
```

Did your agent respond to you? 🍾 Congratulations! You have successfully created your first agent machine.

### Next Steps
Now that you have a running agent machine with a simple agent. Let's start customizing!

- [ ] ⭐ [Eidolon](https://github.com/eidolon-ai/eidolon) on GitHub. Eidolon is a fully open source project, and we love your support!
- [ ] Add new capabilities via logic units (tools)
- [ ] Enable [agent-to-agent communication](/docs/howto/communication)
- [ ] [Swap out components](/docs/howto/customize_builtins) (like the underlying llm)
- [ ] Use [structured inputs](/docs/components/simple_agent#defining-actions) for prompt templating
- [ ] Leverage your agent's [state machine](/docs/components/simple_agent#defining-actions)
- [ ] Launch [Eidolon's UI](/docs/howto/webui)
