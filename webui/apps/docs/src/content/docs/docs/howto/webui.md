---
title: Launch the Webui
description: References - Running the Webui
---

Eidolon Web UI is a powerful interface for interacting with the Eidolon project, designed to streamline your experience and enhance usability. Below you'll find concise
instructions to get your development environment set up and the server running smoothly.

## Running With Docker
If you are looking to get started quickly, we publish an image that you can use without needing to set a development environment.

### mac
```bash
docker run -e "EIDOLON_SERVER=http://host.docker.internal:8080" -p 3000:3000 eidolonai/webui:latest
```
### linux
```bash
docker run -e "EIDOLON_SERVER=http://172.17.0.1:8080" -p 3000:3000 eidolonai/webui:latest
```

## Try it out!
Head over to [localhost:3000](http://localhost:3000/) in your favorite browser and start interacting with the Eidolon 
Web UI.

🚨 Make sure you have an Eidolon machine running locally on port 8080. For instructions on how to run a machine, see our [getting started guide](https://www.eidolonai.com/docs/introduction/)

🚨 We publish several apps that depend on different types of agents. Our [⭐dev-tool app⭐](http://localhost:3000/eidolon-apps/dev-tool)️ is a great place to start, and will 
work for all agents. 
