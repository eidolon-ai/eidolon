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

### MacOS
##### Python [3.11](https://formulae.brew.sh/formula/python@3.11) | [3.12](https://formulae.brew.sh/formula/python@3.12)
Ensure Python 3.11 or 3.12 is installed
```bash
brew install python@3.12
```

##### [Python Poetry](https://python-poetry.org/docs/ "Official poetry installation guide")
In this walkthrough we use will use Poetry to manage our venv.
```bash
pipx install poetry
```

##### [OpenAI API Key](https://platform.openai.com/account/api-keys "Create an OpenAI key") 
You should have an OpenAI API Key handy. Create a new key at [openai.com](https://platform.openai.com/api-keys) if you 
don't have one already.

🚨 Eidolon uses gpt-4 by default which requires a paid OpenAI account.


### Linux

Linux setup is similar to MacOS with installation using the package managers of your choice.

<details>

Commands used are for Debian Bullseye, use apk instead of apt for Alpine Linux.

apt requires root access to run in most Linux distributions. Elevate access by running the commands with ```sudo```.
##### Python 3.11 | 3.12 
```bash
apt install python3
```
##### Python Poetry
In this walkthrough we use will use Poetry to manage our venv.
```bash
pipx install poetry
```

##### Python VENV
```bash
apt install python3.11-venv
python3 -m venv eidolon_venv # Create VENV
source eidolon_venv/bin/activate # Activate VENV
```
##### [OpenAI API Key](https://platform.openai.com/account/api-keys "Create an OpenAI key") 
You should have an envrionment variable OPENAI_API_KEY set to your OpenAI API.
Create a new key on [openai.com](https://platform.openai.com/api-keys) if you don't have one already.

</details>

### Windows
Eidolon AI SDK is only supported on UNIX (Linux/MacOS) systems. Follow the instructions below to install WSL, a feature that lets you to run a Linux environment directly on Windows, and the Debian Linux distribution.
<details>

#### [Windows Subsystem for Linux (WSL)](https://learn.microsoft.com/en-us/windows/wsl/install#manual-installation-steps)

You must be running Windows 10 version 2004 and higher (Build 19041 and higher) or Windows 11 to use the command below. If you are on earlier versions please see the official Microsoft [manual install page](https://learn.microsoft.com/en-us/windows/wsl/install-manual) for older versions of WSL.
```powershell
wsl --install -d Debian
```
Upon installing WSL and Debian, you will be prompted to create setup your Linux credentials. Remember the password from this step as you will need it when running commands in Linux as the user. If you need to run WSL again, use the command ```wsl```, or find the installed distribution using the Windows key menu.

Once you have installed WSL and a Linux distribution, follow the Linux quickstart process to get started with Eidolon AI!
</details>

## Run Eidolon Quickstart

First let's clone Eidolon's quickstart repository, clone it to your local machine.

```bash
git clone https://github.com/eidolon-ai/eidolon-quickstart.git
cd eidolon-quickstart
```

Next run the server in dev mode.

```bash
make serve-dev
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

The repository you just forked defines an **AgentMachine** 💻 with a single **AgentProgram** 🤖 named `hello_world` 👋.

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

### Try it out
First download the Ediolon CLI
```bash
pip install 'eidolon-ai-client[cli]' -U
```

The create an AgentProcess
```bash
export PID=$(eidolon-cli processes create --agent hello_world)
```

Now that we have started a conversation, we can converse with our agent
```bash
eidolon-cli actions converse --process-id $PID --body "Hi! I made you"
```

Did your agent respond to you? If so, congratulations! You have successfully created your first agent machine.

##### Next Steps
Now that you have a running agent machine with a simple agent. Let's start customizing!

- [ ] ⭐ [Eidolon](https://github.com/eidolon-ai/eidolon) on GitHub. Eidolon is a fully open source project, and we love your support!
- [ ] Add new capabilities via logic units (tools)
- [ ] Enable [agent-to-agent communication](/docs/references/communication)
- [ ] [Swap out components](/docs/references/pluggable) (like the underlying llm)
- [ ] Use [structured inputs](/docs/components/simple_agent#defining-actions) for prompt templating
- [ ] Leverage your agent's [state machine](/docs/components/simple_agent#defining-actions)
- [ ] Launch [Eidolon's UI](/docs/references/webui)
