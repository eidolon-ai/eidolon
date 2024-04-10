---
title: Create an Agent
description: Create your first AgentProgram
---

Now it is time to create your first **AgentProgram**. Create a directory and add a yaml file to describe your resource.

```bash
mkdir hello_world
vim hello_world/hello_world_agent.yaml
```

```yaml
apiVersion: eidolon/v1
kind: Agent
metadata:
  name: hello_world
spec:
  description: "This is an example of a generic agent which greets people by name."
  system_prompt: "You are a friendly greeter who greets people by name while using emojis"
  actions:
    - user_prompt: "Hi, my name is {{name}}"
```