# Welcome to Eidolon - an Open Source Agent Services Framework 

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

🚨 Don't have access to OpenAI GPT4?

By default we use gpt4, but you can change the model to gpt-3.5-turbo if you don't have access to gpt4 by customizing the "cpu" within your agent's spec.


```yaml
spec:
  cpu:
    llm_unit:
      model: "gpt-3.5-turbo"
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
curl -X 'POST' 'http://localhost:8080/processes' -H 'Content-Type: application/json' -d '{
  "agent": "hello_world",
  "title": "quickstart"
}'
````

The result should be a json object with a process id. For example:

```json
{
  "agent": "hello_world",
  "process_id": "65fa0f7b51854d2cb9403aec",
  ...
}
```

Now let's try to make a request to your server.

```bash
curl -X POST http://0.0.0.0:8080/processes/{process_id}/agent/hello_world/actions/converse -H 'Content-Type: application/json' -d '{"name": "World"}'; echo
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
