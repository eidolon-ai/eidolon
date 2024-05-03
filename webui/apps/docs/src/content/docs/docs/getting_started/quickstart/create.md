---
title: Create an Agent Machine
description: Create your first AgentProgram
---

### Setup Development Environment

First let's fork for Eidolon's quickstart repository, clone it to your local machine, and start your server.

```bash
gh repo fork eidolon-ai/eidolon-quickstart --clone=true
cd eidolon-quickstart
make serve-dev
```

If this was successful, you should see machine logs in your terminal.
```bash
INFO - Building machine 'local_dev'
INFO - Starting agent 'hello_world'
INFO - Server Started
```

You can also check out your machine's [swagger docs]((http://localhost:8080/docs#/)).

Believe it or not, you are already up and running with a simple agent! 🎉

### What just happened?

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
  description: "This is an example of a generic agent which greets people by name."
  system_prompt: |
    You are an ai agent who was just created by a brilliant developer getting started with Eidolon (great decision).
    You love emojis and use them liberally.
```

### Try it out

So, if I already have a server running, how do I interact with my agent?

Head over to another terminal where we will install a cli, create a new process, and then converse with our agent on 
that process.
```bash
pip install eidolon-client[cli]
export PID=$(eidolon-cli processes create --agent hello_world)
eidolon-cli actions converse --process-id $PID --body "Hi! I made you"
```

Did your agent respond to you? If so, congratulations! You have successfully created your first agent machine.

If you found this guide helpful, ⭐ [Eidolon](https://github.com/eidolon-ai/eidolon) on GitHub.\
Eidolon is a fully open source project, and we love your support!
```bash
gh repo star eidolon-ai/eidolon
```
##### Next Steps
Now that you have a running agent machine with a simple agent. Let's start customizing!

- [ ] Add new capabilities via logic units (tools)
- [ ] Enable agent-to-agent communication
- [ ] Swap out components (like the underlying llm)
- [ ] Use structured inputs for prompt templating
- [ ] Leverage your agent's state machine
- [ ] Launch Eidolon's UI
