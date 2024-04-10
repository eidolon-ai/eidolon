---
title: Agent Communication
description: References - Agent Communication
---

Eidolon simplifies agent-to-agent communication with a built-in mechanism enabling seamless interaction between agents. In the example below we will reuse the `hello_world` agent from our quickstart guide, and create a second `qa` agent who will interface with the hello world agent.

_hello_world_agent.yaml_
```yaml
apiVersion: eidolon/v1
kind: Agent
metadata:
  name: hello_world

spec:
  implementation: GenericAgent
  description: "This is an example of a generic agent which greets people by name."
  system_prompt: "You are a friendly greeter who greets people by name while using emojis"
  user_prompt: "Hi, my name is {{name}}"
  input_schema:
    name:
      type: string
      description: The caller's name
```

_qa_agent.yaml_
```yaml
apiVersion: eidolon/v1
kind: Agent
metadata:
  name: qa

spec:
  implementation: GenericAgent
  description: "This is a qa agent responsible for making sure the hello_agent is functioning properly"
  agent_refs: ["hello_world"]
  system_prompt: >-
    You are a qa agent who is responsible for testing your tools. When asked to test
    a tool, you will call all methods related to the tool with reasonable inputs and
    determine if they are operating in a justifiable manner. When you have performed
    all your tests, respond with "Error: {description}" if there is an issue, otherwise
    return "Success: [{test1 description, {test2 description}, ...}]"
  user_prompt: "Test the hello_world agent"
```

Now run your machine and hit the "question" endpoint on your qa agent. In the machine logs you will notice activity within the hello_world agent. Your qa agent is able communicating with the hello_world agent! 🎉