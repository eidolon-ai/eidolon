# Eidolon
## An Open Source Agent Services Framework


Eidolon makes it easy to build, deploy, and manage agents and other generative ai services.


### Step 0: Prerequisites

* [Python 3.11](https://formulae.brew.sh/formula/python@3.11)
* [OpenAI api key](https://platform.openai.com/account/api-keys): You should have an envar OPENAI_API_KEY set to your OpenAI api key.

### Step 1: Install Eidolon SDK

First, you need to install the Eidolon SDK. Open your terminal and run the following command:

```bash
pip install eidolon-ai-sdk
```

### Step 2: Create an Agent

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
    user_prompt: "Hi, my name is {{name}}"
```

### Step 3: Run Eidolon Server

Finally, open a new terminal window and run your machine using eidolon-server.

```bash
eidolon-server -m local_dev hello_world
```
🚨 Getting `command not found: eidolon-server`? Open a new terminal window and try the command again.

⚠️ The `-m local_dev` option specifies using the `local_dev` builtin Machine resource. This machine uses in-memory symbolic memory rather than mongo, so state will disappear between server restarts.

### Step 4: Try it out!

First create a process for your conversation.

```bash
curl -X 'POST' 'http://localhost:8080/processes' -H 'Content-Type: application/json' -d '{
  "agent": "hello_world",
  "title": "quickstart"
}'
````

The result should be a json object with a process id. For example:

```json
{"process_id":"hello_world-1"}
```

Now let's try to make a request to your server from another terminal window.

```bash
curl -X POST http://0.0.0.0:8080/processes/{process_id}/agent/hello_world/actions/converse -H 'Content-Type: application/json' -d '{"name": "World"}'; echo
```

Replace `{process_id}` with the process id you received from the previous command.

You should now see something like `Hello, World! 🌍👋`


And that's it! You have successfully set up and used a basic project using the Eidolon SDK. To see more endpoints on your agent machine, visit the [swagger ui](http://0.0.0.0:8080/docs).

### Further Reading

For full documentation, visit [www.eidolonai.com](https://www.eidolonai.com/).
