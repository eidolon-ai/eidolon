---
title: Prerequisites and Install
description: Walk through prequisites for Mac and Linux
---

### MacOS
##### [Python 3.11](https://formulae.brew.sh/formula/python@3.11)
Ensure Python3.11 is installed
##### Python PIP
```bash
python -m ensurepip
```
##### [OpenAI API Key](https://platform.openai.com/account/api-keys "Create an OpenAI key") 
You should have an envrionment variable OPENAI_API_KEY set to your OpenAI API key.
```bash
export OPENAI_API_KEY=<YOUR OPENAI API KEY>
```
##### Eidolon SDK
```bash
pip install eidolon-ai-sdk
```

### Linux
Commands used are for Debian Bullseye, use apk instead of apt for Alpine Linux.

apt requires root access to run in most Linux distributions. Elevate access by running the commands with ```sudo```.
##### Python 3.11
```bash
apt install python3
```
##### Python PIP
```bash
apt install python3-pip
```
##### Python Poetry
```bash
apt install python3-poetry
```
##### Python VENV
```bash
apt install python3.11-venv
python3 -m venv eidolon_venv # Create VENV
source eidolon_venv/bin/activate # Activate VENV
```
##### [OpenAI API Key](https://platform.openai.com/account/api-keys "Create an OpenAI key") 
You should have an envrionment variable OPENAI_API_KEY set to your OpenAI API key.
```bash
export OPENAI_API_KEY=<YOUR OPENAI API KEY>
```
##### Eidolon SDK
```bash
pip install eidolon-ai-sdk
```

### Windows
Eidolon AI SDK is only supported on UNIX (Linux/MacOS) systems. Follow the instructions below to install WSL, a feature that lets you to run a Linux environment directly on Windows, and the Debian Linux distribution.

#### [Windows Subsystem for Linux (WSL)](https://learn.microsoft.com/en-us/windows/wsl/install#manual-installation-steps)

You must be running Windows 10 version 2004 and higher (Build 19041 and higher) or Windows 11 to use the command below. If you are on earlier versions please see the official Microsoft [manual install page](https://learn.microsoft.com/en-us/windows/wsl/install-manual) for older versions of WSL.
```powershell
wsl --install -d Debian
```
Upon installing WSL and Debian, you will be prompted to create setup your Linux credentials. Remember the password from this step as you will need it when running commands in Linux as the user. If you need to run WSL again, use the command ```wsl```, or find the installed distribution using the Windows key menu.

Once you have installed WSL and a Linux distribution, follow the Linux quickstart process to get started with Eidolon AI!