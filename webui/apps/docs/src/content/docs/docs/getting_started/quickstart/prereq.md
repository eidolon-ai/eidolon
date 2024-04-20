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
You should have an envrionment variable OPENAI_API_KEY set to your OpenAI api key.
```bash
export OPENAI_API_KEY=<YOUR OPENAI API KEY>
```
##### Eidolon SDK
```bash
pip install eidolon-ai-sdk
```

### Linux
NOTE: Commands used are for Debian Bullseye, use apk instead of apt for Alpine Linux
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
```
##### [OpenAI API Key](https://platform.openai.com/account/api-keys "Create an OpenAI key") 
You should have an envrionment variable OPENAI_API_KEY set to your OpenAI api key.
```bash
export OPENAI_API_KEY=<YOUR OPENAI API KEY>
```
##### Eidolon SDK
```bash
pip install eidolon-ai-sdk
```