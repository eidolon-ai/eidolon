---
title: Run and Try
description: Run your AgentProgram and try it through the API
---

Finally, open a new terminal window and run your machine using eidolon-server.

```bash
eidolon-server -m local_dev hello_world
```
🚨 Getting `command not found: eidolon-server`? Open a new terminal window and try the command again.

⚠️ The `-m local_dev` option specifies using the `local_dev` builtin Machine resource. This machine uses in-memory symbolic memory rather than mongo, so state will disappear between server restarts.

## Try it out!

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