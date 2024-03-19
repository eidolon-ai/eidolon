---
title: EidolonGPT
description: A tutorial on setting up a basic GPT with Eidolon
---

## Want to make a GPT in Eidolon?

Eidolon can do a lot of things, but sometimes the best way to learn is to start with a simple example.

In this tutorial, we'll guide you through the process of building a simple conversational agent using the Eidolon framework. This agent will be capable of understanding and responding to user inputs in a conversational manner, similar to GPTs you may be familiar with.

<a title="EidolonGTP Example" target="_blank" href="https://github.com/eidolon-ai/eidolon/tree/main/examples/eidolon_examples/conversational_chatbot">Check out our tutorial on github</a>

#### Prerequisites

Before we start, ensure you have the following:
- A Python environment with Eidolon installed.
    ```bash
    pip install eidolon-ai-sdk -U
    ```
- An OpenAI API token set at the envar OPENAI_API_KEY.
    ```bash
    export OPENAI_API_KEY=TOKEN
    ```

#### Step 1: Define Your Agent's Specification

First, you need to define the specification for your conversational agent. This involves setting up a YAML file that describes your agent's capabilities and how it should behave. For simplicity, we'll create an agent that greets users and responds to basic inquiries.

Create a file named `conversational_agent.yaml` in the `resources`
```bash
mkdir resources
touch resources/conversational_agent.yaml
open resources/conversational_agent.yaml
```

and add the following content:

```yaml
apiVersion: eidolon/v1
kind: Agent
metadata:
  name: conversational_agent
spec:
  system_prompt: "You are a helpful assistant."
```

This YAML file defines a "SimpleAgent" (default) with a conversational capability. It specifies the agent's name, a brief description, and the actions it can perform. By default, our agent has one action named `converse`, which takes a user's message as input and returns a string response.

#### Step 2: Run Your Agent

Finally, you need to run your agent so it can start processing requests. This involves using the `eidolon-server` command to serve your agent.

```bash
export AGENT_DIRECTORY=resources
eidolon-server -m local_dev $AGENT_DIRECTORY
```

This command starts the Eidolon server with your agent loaded. The `-m local_dev` option specifies using the `local_dev` built-in Machine resource, which uses in-memory symbolic memory so you don't need mongo running.

Your backend machine (with your agent) is now running, and you can see available endpoints at the <a title="swagger ui" target="_blank" href="http://localhost:8080/docs">swagger ui</a>.

#### Step 4: Try It out!
You can now create a new conversation, or `process`, on your agent.

```bash
curl -X 'POST' 'http://localhost:8080/processes' -H 'Content-Type: application/json' -d '{
  "agent": "conversational_agent",
  "title": "getting_started"
}'
```

This will return a process id, which you can use to converse with your agent.

```bash
export PROCESS_ID=YOUR_PROCESS_ID
curl -X 'POST' "http://localhost:8080/processes/$PROCESS_ID/agent/conversational_agent/actions/converse" -d 'What kind of tools can I build with LLM agents?'
```

#### Step 5: Start the UI.

If you want to interact with your conversational agent with a web rather than rest interface, Eidolon provides a simple ui for that.

It handles streaming and argument parsing so you can focus on the conversation.

See the <a title="ui docs" target="_blank" href="https://github.com/eidolon-ai/eidolon/tree/main/webui">eidolon-ui docs</a> to get started.

#### Next Steps
You have now built a conversational agent using Eidolon, and perhaps even ran the Eidolon UI. Congratulations!

Try experimenting with the system prompt to see how you can customize your Agent. Similarly, there is much more to a "SimpleAgent" (the default type of agent) 
than fits in this example. To learn see to introduce custom user-prompts, multiple actions, or even a state machine take a look at the 
<a target="_blank" href="https://github.com/eidolon-ai/eidolon/blob/main/sdk/eidolon_ai_sdk/agent/simple_agent.py">SimpleAgentSpec</a>


