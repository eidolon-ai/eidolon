---
title: Prerequisites
description: Walk through prequisites for Mac and Linux
---
Welcome to the Eidolon Quickstart guide. This section covers environment setup, installing **Eidolon**, creating your first **AgentProgram**, and running an **AgentMachine**.

If you have already been through this guide, check out the [References](/docs/references/introduction), [Demos](/docs/getting_started/demos/introduction), or [Tutorials](/docs/getting_started/tutorials/introduction) for more in-depth guidance on what you can do with Eidolon.

We know you are excited about creating your first agent, but first let's make sure we have everything we need to get started. 


### MacOS
##### [Python 3.11](https://formulae.brew.sh/formula/python@3.11)
Ensure Python3.11 is installed
```bash
brew install python@3.11
```

##### [Python Poetry](https://python-poetry.org/docs/ "Official poetry installation guide")
In this walkthrough we use will use Poetry to manage our venv.
```bash
pipx install poetry
```

##### [OpenAI API Key](https://platform.openai.com/account/api-keys "Create an OpenAI key") 
You should have an envrionment variable OPENAI_API_KEY set to your OpenAI API.
Create a new key on [openai.com](https://platform.openai.com/api-keys) if you don't have one already.
```bash
export OPENAI_API_KEY=<YOUR OPENAI API KEY>
```

##### [GitHub CLI](https://cli.github.com/) (optional)
In this walkthrough we will use the gh cli to fork our machines. You are free to use the web interface if you prefer.

To download and authenticate the cli, run the following commands:
```bash
brew install gh
gh auth login -h GitHub.com -w -p https
```

### Linux
Commands used are for Debian Bullseye, use apk instead of apt for Alpine Linux.

apt requires root access to run in most Linux distributions. Elevate access by running the commands with ```sudo```.
##### Python 3.11
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
```bash
export OPENAI_API_KEY=<YOUR OPENAI API KEY>
```

##### [GitHub CLI](https://cli.github.com/) (optional)
In this walkthrough we will use the gh cli to fork our machines. You are free to use the web interface if you prefer.
You can download the cli with brew, or check out their [installation guide](https://github.com/cli/cli#installation) for other methods.

### Windows
Eidolon AI SDK is only supported on UNIX (Linux/MacOS) systems. Follow the instructions below to install WSL, a feature that lets you to run a Linux environment directly on Windows, and the Debian Linux distribution.

#### [Windows Subsystem for Linux (WSL)](https://learn.microsoft.com/en-us/windows/wsl/install#manual-installation-steps)

You must be running Windows 10 version 2004 and higher (Build 19041 and higher) or Windows 11 to use the command below. If you are on earlier versions please see the official Microsoft [manual install page](https://learn.microsoft.com/en-us/windows/wsl/install-manual) for older versions of WSL.
```powershell
wsl --install -d Debian
```
Upon installing WSL and Debian, you will be prompted to create setup your Linux credentials. Remember the password from this step as you will need it when running commands in Linux as the user. If you need to run WSL again, use the command ```wsl```, or find the installed distribution using the Windows key menu.

Once you have installed WSL and a Linux distribution, follow the Linux quickstart process to get started with Eidolon AI!
