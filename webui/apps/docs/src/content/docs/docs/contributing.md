---
title: Contributing
description: How to contribute to Eidolon
---

# Contributing to Eidolon
Thank you for being interested in contributing to Eidolon! We are always looking for new contributors to help us improve our project.
We want contributing to Eidolon to be fun, enjoyable, and educational for anyone and everyone. 
To contribute to this project, please follow a ["fork and pull request"](https://docs.github.com/en/get-started/quickstart/contributing-to-projects) workflow. 
Please do not try to push directly to this repo unless you are a maintainer.



## 🗺️ Contributing Guidelines

### 🚩 GitHub Issues

Our [backlog page](https://github.com/orgs/eidolon-ai/projects/1/views/1) contains bugs, improvements, and feature requests that we are currently working on.

If you are interested in working on an issue, please let us know in our [Discord channel](https://discord.gg/6kVQrHpeqG), and we 
will help you. As the size and scope of the project grows, we will likely move to a more formal process.

To get your feet wet, we keep a catalog of [good first issues](https://github.com/orgs/eidolon-ai/projects/6/views/6) for new contributors to tackle.

We will try to keep these issues as up to date as possible, though with the rapid rate of development some may get out of date. 
If you notice this happening, please just let us know.

## 🙋 Getting Help

We are always available to help you with any questions you may have. Please reach out to us on our [Discord channel](https://discord.gg/6kVQrHpeqG) for help.
Although we try to have a developer setup to make it as easy as possible for others to contribute (see below) it is possible that some pain point may arise around 
environment setup, linting, documentation, or other. Should that occur, please contact a maintainer! Not only do we want to help get you unblocked, 
but we also want to make sure that the process is smooth for future contributors.

In a similar vein, we do enforce certain linting, formatting, and documentation standards in the codebase. If you are finding these difficult (or even just annoying) to 
work with, feel free to contact a maintainer for help - we do not want these to get in the way of getting good code into the codebase.

## 🏭 Release process

As of now, Eidolon has an adhoc release process: releases are cut with high frequency by a developer and [published to pypi](https://pypi.org/project/eidolon-ai-sdk/).

Eidolon follows the [semver versioning standard](https://semver.org/). However, as pre-1.0 software, even patch releases may contain non-backwards-compatible changes.

We want to give all contributors the opportunity to be recognized for their work. As such, we will include all contributors in the repo and our website. Please let us know how
you would like to be recognized, including your X account if possible.

## 🛠️ Tooling

We employ a [monorepo](https://en.wikipedia.org/wiki/Monorepo) structure for Eidolon. This means that all code, documentation, and other project assets are stored in a single repository.
Therefore, there are two types of dependencies in the project, python for the backed and typescript for the frontend.

We use the following tools in the python project:
* [poetry](https://python-poetry.org/) for dependency management
* [mongodb](https://www.mongodb.com/) for configuration management, **or you can run in local mode, but changes between restart will be lost**
* [openai](https://openai.com) as the default LLM. You will need an OPENAI_API_KEY to run the project.
* We develop with [IntelliJ](https://www.jetbrains.com/idea/) or [PyCharm](https://www.jetbrains.com/pycharm/), but any IDE should work.

We use the following tools in the typescript project:
* [turoborepo](https://turbo.build) for the build system
* [pnpm](https://pnpm.io/) for dependency management
* [react](https://reactjs.org/) for the frontend components
* [nextjs](https://nextjs.org/) for our sample app
* We develop with [IntelliJ](https://www.jetbrains.com/idea/) or [Webstorm](https://www.jetbrains.com/webstorm/), but any IDE should work.

The core development is all done using python and if all you are interested in is the back end, you can ignore the typescript setup and run the UI via the docker-compose file.

## Operating System
We develop on macOS and all the scripts are written for that. However, we have contributors who develop on Windows and Linux. We try to make the setup as easy as 
possible for all operating systems, but if you run into any issues, please let us know.

**WARNING:** Developing on Windows can be a bit more challenging than on macOS or Linux. Tests take much longer to start and run and the configuration is quite finicky. We
**strongly** recommend using the GitHub bash shell for development on Windows.

## 🚀 Getting Started (Python)

First, let's make sure we have everything we need to get started.
### Prerequisites (macOS)

##### Ensure Python3.11 and pipx is installed
```bash
brew install python@3.11

# see https://pipx.pypa.io/
brew install pipx
```

##### [Python Poetry](https://python-poetry.org/docs/ "Official poetry installation guide")
In this walkthrough we use will use Poetry to manage our venv.
```bash
pipx install poetry
```

##### [Install MongoDB](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/)
```bash
brew tap mongodb/brew
brew install mongodb-community@5.0
```


##### [GitHub CLI](https://cli.github.com/) (optional)
```bash
brew install gh
gh auth login -h GitHub.com -w -p https
```

### Prerequisites (linux)

##### Ensure Python3.11 is installed
```bash
apt install python3
```

##### [Python Poetry](https://python-poetry.org/docs/ "Official poetry installation guide")
```bash
pipx install poetry
```

##### [Install MongoDB](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-debian/)
*follow the instructions for your distribution*

##### [GitHub CLI](https://cli.github.com/) (optional)
```bash
apt install gh
gh auth login -h GitHub.com -w -p https
```

### Setup Eidolon

Now that we have all the prerequisites, let's fork the Eidolon monorepo and get started!

##### [Fork Eidlon monorepo](https://github.com/eidolon-ai/eidolon/fork)
```bash
gh repo fork eidolon-ai/eidolon --clone=true
cd eidolon
```

##### [OpenAI API Key](https://platform.openai.com/account/api-keys "Create an OpenAI key")
Visit the open AI site and create an API key. You will need to set this as an environment variable in the .env file.

From the root directory of Eidolon, create a .env file and add your OpenAI key.
```bash
echo "OPENAI_API_KEY=<YOUR OPENAI>" > .env
```

Other optional environment variables are:
```bash
echo "MONGO_CONNECTION_STR=mongodb://localhost:27017/?directConnection=true" >> .env
echo "MONGO_DATABASE_NAME=eidolon" >> .env
echo "MISTRAL_API_KEY=<YOUR MISTRAL_API_KEY>" >> .env
echo "ANTHROPIC_API_KEY=<YOUR ANTHROPIC_API_KEY>" >> .env
echo "OLLAMA_HOST=<YOUR URL TO OLLAMA LOCAL INSTALLATION>"
```

There is also a .env.example file changed in that you can clone.

### Build and Run Eidolon
There are 3 main components that need to be built and run: 

* **Eidolon Client**: located in the client/python directory
* **Eidolon SDK**: located in the sdk directory
* **Eidolon Examples**: located in the examples directory

Each of these need a separate poetry environment. See [the poetry document](https://python-poetry.org/docs/basic-usage/#activating-the-virtual-environment) for more information.


#### Run the server
```bash
cd examples
poetry shell
poetry install
poetry run eidolon-server eidolon_examples/conversational_chatbot/resources
```

You should now be able to access the server at `http://localhost:8080' and the swagger docs at `http://localhost:8080/docs`.

## 🚀 Getting Started (Frontend)

The web UI is built using [Turbo Repo](https://turbo.build/repo). Turbo Repo is a monorepo tool that allows us to manage multiple packages in a single repository.

The following packages in apps exist in the webui directory:
* **eidolon-ui2**: ```webui/apps/eidolon-ui2```. The main web UI application for Eidolon. This contains a sample nextjs application that uses the Eidolon SDK and UI components.
* **docs**: ```webui/apps/docs```. The documentation for Eidolon. This is an astro application that uses the Eidolon SDK and UI components.
* **client**: ```webui/packages/eidolon-client```. The Eidolon client library. This is a typescript package that is used by the web UI applications to communicate with the Eidolon server.
* **components**: ```webui/packages/eidolon-components```. The Eidolon components library. This is a typescript package that contains all the shared REACT components used by the web UI applications.

First, let's make sure we have everything we need to get started.

### Prerequisites (macOS)
We need to install the tools required to build and run the frontend.

##### [Node.js](https://nodejs.org/en/download/)
```bash
brew install node
```

##### [pnpm](https://pnpm.io/)
```bash
npm install -g pnpm
```

##### [Turbo](https://turbo.build/docs/installation)
```bash
npm install -g @turbo/build
```

### Prerequisites (linux)

##### [Node.js](https://nodejs.org/en/download/)
```bash
apt install nodejs
```

##### [pnpm](https://pnpm.io/)
```bash
npm install -g pnpm
```

##### [Turbo](https://turbo.build/docs/installation)
```bash
npm install -g @turbo/build
```

### Setup Eidolon

Assuming you have already forked the Eidolon monorepo, let's get started with the frontend.

##### Add environment variables
From the root directory of Eidolon:
```bash
cd webui/apps/eidolon-ui2
echo "EIDOLON_SERVER=http://localhost:8080" > .env
echo "EIDOLON_AUTH_PROVIDERS=" >> .env
echo "NEXTAUTH_SECRET=" >> .env
```

##### Install the dependencies
```bash
cd webui
pnpm install
```

### Run Eidolon in dev mode
```bash
cd webui/apps/eidolon-ui2
turbo run dev
```
