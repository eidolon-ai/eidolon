# Welcome to Eidolon - an Open Source Agent Services Framework 

<img alt="img_1" height="400" width="400" src="./docs/src/assets/main_images/img_1.png"/>

Eidolon helps developers designing and deploying agent-based services.

## Why Eidolon?
### 1. Easy to deploy
With Eidolon, agents are services, so there is no extra work when it comes time to deploy. The HTTP server is built in.

### 2. Simple agent-to-agent communication
Since agents are services with well-defined interfaces, they easily communicate with tools dynamically generated from 
the openapi json schema defined by the agent services. 

### 3. Painless component customization and upgrade
With a focus on modularity, Eidolon makes it easy to swap out components. Grab an off the shelf llm, rag impl, tools, 
etc or just define your own.

This means no vendor lock-in and minimizes the work needed to upgrade portions of an agent. Without this flexibility, 
developers will not be able to adapt their agents to the rapidly changing AI landscape.

## Demo
[Deploy a Chatbot: Help Swifties learn about Kelce](https://www.youtube.com/watch?v=jU_HYhWm6qE)


# Getting Started

## Step 0: Prerequisites

* [Python 3.11](https://formulae.brew.sh/formula/python@3.11)
* [OpenAI api key](https://platform.openai.com/account/api-keys): You should have an envar OPENAI_API_KEY set to your OpenAI api key.

## Step 1: Install Eidolon SDK

First, you need to install the Eidolon SDK. Open your terminal and run the following command:

```bash
pip install eidolon-ai-sdk
```

## Step 2: Create an Agent

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

## Step 3: Run Eidolon Server

Finally, open a new terminal window and run your machine using eidolon-server.

```bash
eidolon-server -m local_dev hello_world
```
🚨 Getting `command not found: eidolon-server`? Open a new terminal window and try the command again.

⚠️ The `-m local_dev` option specifies using the `local_dev` builtin Machine resource. This machine uses in-memory symbolic memory rather than mongo, so state will disappear between server restarts.

## Step 4: Try it out!

First create a process for your conversation.

```bash
curl -X POST http://0.0.0.0:8080/agents/hello_world/processes; echo
````

The result should be a json object with a process id. For example:

```json
{"process_id":"hello_world-1"}
```

Now let's try to make a request to your server from another terminal window.

```bash
curl -X POST http://0.0.0.0:8080/agents/hello_world/processes/{process_id}/actions/converse -H 'Content-Type: application/json' -d '{"name": "World"}'; echo
```

Replace `{process_id}` with the process id you received from the previous command.

You should now see something like `Hello, World! 🌍👋`

And that's it! You have successfully set up and used a basic project using the Eidolon SDK. To see more endpoints on your agent machine, visit the [swagger ui](http://0.0.0.0:8080/docs).

## Further Reading

For full documentation, visit [www.eidolonai.com](https://www.eidolonai.com/).

## Contributing

We welcome and appreciate contributions! 

Reach out to us on [discord](https://discord.gg/6kVQrHpeqG) if you have 
any questions or suggestions.

If you need help with the mechanics of contributing, check out the [First Contributions Repository](https://github.com/firstcontributions/first-contributions). 
