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
Since agents are services with well-defined interfaces, they easily communicate with tools dynamically generated from 
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
make docker-serve
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
- [ ] Enable [agent-to-agent communication](https://www.eidolonai.com/docs/howto/communication)
- [ ] [Swap out components](https://www.eidolonai.com/docs/howto/customize_builtins) (like the underlying llm)
- [ ] Use [structured inputs](https://www.eidolonai.com/docs/components/agents/simpleagent#actions) for prompt templating
- [ ] Leverage your agent's [state machine](https://www.eidolonai.com/docs/components/agents/simpleagent#actions)
- [ ] Launch [Eidolon's UI](https://www.eidolonai.com/docs/howto/webui)


## Support ⭐️
Eidolon is a completely open source project. Keep your dirty money!

⭐️ But we love your stars ⭐️

## Contributing

We welcome and appreciate contributions! 

Reach out to us on [discord](https://discord.gg/6kVQrHpeqG) if you have 
any questions or suggestions.

If you need help with the mechanics of contributing, check out the [First Contributions Repository](https://github.com/firstcontributions/first-contributions). 

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/LukeLalor"><img src="https://avatars.githubusercontent.com/u/13319204?v=4?s=100" width="100px;" alt="Luke Lalor"/><br /><sub><b>Luke Lalor</b></sub></a><br /><a href="https://github.com/eidolon-ai/eidolon/commits?author=LukeLalor" title="Documentation">📖</a> <a href="https://github.com/eidolon-ai/eidolon/commits?author=LukeLalor" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/dbrewster"><img src="https://avatars.githubusercontent.com/u/399676?v=4?s=100" width="100px;" alt="Dave Brewster"/><br /><sub><b>Dave Brewster</b></sub></a><br /><a href="https://github.com/eidolon-ai/eidolon/commits?author=dbrewster" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/jahabeebs"><img src="https://avatars.githubusercontent.com/u/47253537?v=4?s=100" width="100px;" alt="Jacob Habib"/><br /><sub><b>Jacob Habib</b></sub></a><br /><a href="https://github.com/eidolon-ai/eidolon/commits?author=jahabeebs" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/TheSheepGoesBa"><img src="https://avatars.githubusercontent.com/u/54458170?v=4?s=100" width="100px;" alt="Eric Brewster"/><br /><sub><b>Eric Brewster</b></sub></a><br /><a href="https://github.com/eidolon-ai/eidolon/commits?author=TheSheepGoesBa" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://luislaffitte.netlify.app/"><img src="https://avatars.githubusercontent.com/u/133073175?v=4?s=100" width="100px;" alt="Luis Laffitte"/><br /><sub><b>Luis Laffitte</b></sub></a><br /><a href="https://github.com/eidolon-ai/eidolon/commits?author=Wizzerrd" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/harivmasoor"><img src="https://avatars.githubusercontent.com/u/22420711?v=4?s=100" width="100px;" alt="harivmasoor"/><br /><sub><b>harivmasoor</b></sub></a><br /><a href="https://github.com/eidolon-ai/eidolon/commits?author=harivmasoor" title="Code">💻</a> <a href="#content-harivmasoor" title="Content">🖋</a> <a href="#eventOrganizing-harivmasoor" title="Event Organizing">📋</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://speakerdeck.com/eltociear"><img src="https://avatars.githubusercontent.com/u/22633385?v=4?s=100" width="100px;" alt="Ikko Eltociear Ashimine"/><br /><sub><b>Ikko Eltociear Ashimine</b></sub></a><br /><a href="#content-eltociear" title="Content">🖋</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/ravieidolon"><img src="https://avatars.githubusercontent.com/u/157836102?v=4?s=100" width="100px;" alt="ravieidolon"/><br /><sub><b>ravieidolon</b></sub></a><br /><a href="#content-ravieidolon" title="Content">🖋</a> <a href="#eventOrganizing-ravieidolon" title="Event Organizing">📋</a></td>
    </tr>
  </tbody>
  <tfoot>
    <tr>
      <td align="center" size="13px" colspan="7">
        <img src="https://raw.githubusercontent.com/all-contributors/all-contributors-cli/1b8533af435da9854653492b1327a23a4dbd0a10/assets/logo-small.svg">
          <a href="https://all-contributors.js.org/docs/en/bot/usage">Add your contributions</a>
        </img>
      </td>
    </tr>
  </tfoot>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!