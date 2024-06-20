# Welcome to Eidolon - an Open Source Agent Service SDK

[![PyPI - Downloads](https://img.shields.io/pypi/v/eidolon-ai-sdk?style=flat&label=eidolon-ai-sdk)](https://pypi.org/project/eidolon-ai-sdk/)
[![PyPI - Downloads](https://img.shields.io/pypi/v/eidolon-ai-client?style=flat&label=eidolon-ai-client)](https://pypi.org/project/eidolon-ai-client)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/eidolon-ai-sdk)](https://pypistats.org/packages/eidolon-ai-sdk)
[![Tests - Status](https://img.shields.io/github/actions/workflow/status/eidolon-ai/eidolon/test_python.yml?style=flat&label=test)](https://github.com/eidolon-ai/eidolon/actions/workflows/test_python.yml?query=branch%3Amain)


Eidolon helps developers designing and deploying agent-based services.

## Why Eidolon?
### 1. Easy to deploy
With Eidolon, agents are services, so there is no extra work when it comes time to deploy. The HTTP server is built in.

### 2. Simple agent-to-agent communication
Since agents are services with well-defined interfaces, they easilyaasdfasdf communicate with tools dynamically generated from 
the openapi json schema defined by the agent services. 

### 3. Painless component customization and upgrade
With a focus on modularity, Eidolon makes it easy to swap out components. Grab an off the shelf llm, rag impl, tools, 
etc or just define your own.

This means no vendor lock-in and minimizes the work needed to upgrade portions of an agent. Without this flexibility, 
developers will not be able to adapt their agents to the rapidly changing AI landscape.

Check out [Eidolon's website](https://eidolonai.com/) to learn more.

## [Quickstart Guide 🚀](https://www.eidolonai.com/docs/quickstart)

### Running the AgentMachine
```bash
git clone https://github.com/eidolon-ai/eidolon-quickstart.git
cd eidolon-quickstart
make check
make serve-dev
```

If your AgentMachine successfully started, you should see the following logs in your terminal.
```bash
INFO - Building machine 'local_dev'
INFO - Starting agent 'hello_world'
INFO - Server Started
```

You can also check out your machine's [swagger docs](http://localhost:8080/docs#/).

### Try it out!
Head over to another terminal where we will install a cli, create a new process, and then converse with our agent on 
that process.
```bash
pip install 'eidolon-ai-client[cli]'
export PID=$(eidolon-cli processes create --agent hello_world)
eidolon-cli actions converse --process-id $PID --body "Hi! I made you"
```

Believe it or not, you are already up and running with a simple agent! 🎉

### Next Steps
Now that you have a running agent machine with a simple agent. Let's start customizing!

- [ ] Add new capabilities via logic units (tools)
- [ ] Enable [agent-to-agent communication](/docs/howto/communication)
- [ ] [Swap out components](/docs/howto/customize_builtins) (like the underlying llm)
- [ ] Use [structured inputs](/docs/components/simple_agent#defining-actions) for prompt templating
- [ ] Leverage your agent's [state machine](/docs/components/simple_agent#defining-actions)
- [ ] Launch [Eidolon's UI](/docs/howto/webui)


## Support ⭐️
Eidolon is a completely open source project. Keep your dirty money!

⭐️ But we love your stars ⭐️

## Contributing

We welcome and appreciate contributions! 

Reach out to us on [discord](https://discord.gg/6kVQrHpeqG) if you have 
any questions or suggestions.

If you need help with the mechanics of contributing, check out the [First Contributions Repository](https://github.com/firstcontributions/first-contributions). 
