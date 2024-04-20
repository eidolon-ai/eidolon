---
title: Setup
description: References - Setup
---

If you use poetry, the following setup script will create and configure your project template. 
```bash
poetry new getting_started
sed -i '' 's/python = .*/python = ">=3.11,<3.12"/' getting_started/pyproject.toml
cd getting_started
touch getting_started/hello_world.py
touch getting_started/qa.py
mkdir resources
touch resources/qa_agent.yaml
touch resources/hello_world_agent.yaml
touch resources/frugal_apu.yaml
touch resources/machine.yaml
poetry env use python3.11
poetry add eidolon-ai-sdk
```

Currently, you need to stop and rerun the server when you make changes to your agents.
```bash
poetry run eidolon-server -m local_dev resources
```

The <a title="swagger ui" target="_blank" href="http://localhost:8080/docs">swagger ui</a> will be an easy place to try out your agents.
