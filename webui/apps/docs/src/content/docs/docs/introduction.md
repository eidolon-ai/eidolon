---
title: Introduction
description: This page gives a broad overview of Eidolon and the documentation
---


<div>
  <a href="https://pypi.org/project/eidolon-ai-sdk/">
    <img style="display: inline-block;" alt="PyPI - Version" src="https://img.shields.io/pypi/v/eidolon-ai-sdk?style=flat&label=eidolon-ai-sdk">
  </a>
  <a href="https://pypi.org/project/eidolon-ai-client/">
    <img style="display: inline-block" alt="PyPI - Version" src="https://img.shields.io/pypi/v/eidolon-ai-client?style=flat&label=eidolon-ai-client">
  </a>
  <a href="https://github.com/eidolon-ai/eidolon">
    <img style="display: inline-block;" alt="GitHub Test Status" src="https://img.shields.io/github/actions/workflow/status/eidolon-ai/eidolon/test_python.yml?style=flat&logo=github&label=test">
  </a>
</div>


Welcome to the official documentation of Eidolon Agent Services, an open-source framework for designing and deploying agent-based services.

This page gives a broad overview of the framework and of this documentation, so that you know where to start if you are new to Eidolon or where to look if you need information on a specific feature.


## Before you Start

The [Quickstart Guide](/docs/quickstart/) is a great starting point for anyone new to the Eidolon Framework. There you will find a step-by-step tutorial on setting up and running your first project with Eidolon.

After that check out our [Recipes](/docs/recipes/chatbot) for inspiration and to see what is possible with Eidolon.

The [Builtin Components](/docs/components/symbolicmemory/overview) section contains an in-depth guide showcasing the features and capabilities of Eidolon. And if you're curious about the design behind Eidolon check out the [Architecture](/docs/architecture/introduction) section.


## Frequently Asked Questions

### What is an Agent?
An agent is software (or a software property) that supplements client requests. One very simple type in common use is the User-Agent parameter of a browser. This property tells a website the type and version of the browser that is being used. The site itself may respond with different tools or message types accordingly. 

In AI and LLM-based applications, an agent acts on your behalf as an autonomous entity (In Eidolon we use a service model). We define an agent to operate in some domain -- an LLM -- to satisfy some requirement we've identified. But LLM agents don't just respond to a command. They accept prompts in natural language. They reason out one or more tasks needed to address the prompt, and use the LLM as a tool to compose a response.


### Why do you need an Agent Services Framework?
Products in the generative AI space today -- chatbots, virtual assistants, co-pilots -- all require direct human interaction. The quality of that interaction is amazing, but still one-dimensional. 

With a services framework, agents can work autonomously. They are deployed and begin to work on their own. In a services framework, you can configure these agent services to collaborate and cooperate. One goal may be to create a service that brings together agents operating in different domain (or LLMs). This approach strives for modularity and flexibility. 

Instead of human interaction with a monolithic service -- one that draws from an enormous body of documents -- service agents can work in specific domains. Developers can orchestrate these services to build their own resources and tools for more sophisticated outcomes.

Finally, a developer gets the consistency of development that comes with a framework. Of course there's plenty of room for DIY development with agent libraries, but it's unlikely two more developers will magically agree on process, methodology, or style.  

### What is Eidolon?
Eidolon is a service-oriented framework for developing agents. We want developers to get beyond direct LLM interaction and create modular, flexible services that cooperate and collaborate. We want to help developers lift the veil of today's generative AI innovations and think in simpler, more goal-oriented terms. 

Prompt-and-response work focuses on the speed of producing seemingly human, easy-to-read content. Many of us say it feels like magic, and it's fun. Eidolon makes it possible to think beyond the thrill of this interaction to the productivity we can enable for a variety of goals.


### Why Eidolon?
Eidolon is an open-source project dedicated to service-oriented agent development. It's simple to define and deploy a service, including hyperparameter tuning to modify agent behavior. Developers can create a suite of cooperative agents, each of which can perform tasks with a specific scope and domain. With Eidolon, decomposing a complex task into units of service is the goal. This approach leads not just to a modular design, but one in which the pieces can be more easily modified, swapped out, or upgraded as requirements evolve.

#### 1. Easy to Deploy
Eidolon provides the deployment services out of the box. Define your agent's scope, configure the service with YAML, deploy to a server on-premises or in the cloud, test, Et voila!

With Eidolon, agents are services, so there is no extra work when it comes time to deploy. The HTTP server is built in.

#### 2. Simple Agent-to-Agent Communication
Eidolon is designed with inter-agent communication as a first-class concern. Loose coupling among agents is the preferred design strategy. 

Since agents are services with well-defined interfaces, they easily communicate with tools dynamically generated from the openapi json schema defined by the agent services.

#### 3. Painless Component Customization and Upgrade
With a focus on modularity, Eidolon makes it easy to swap out components. Grab an off the shelf LLM, RAG implementation, tools, etc or just define your own. 

With clear modular design comes all the benefits of customizing and changing out components, while preserving the integrity of the application.

This means no vendor lock-in and minimizes the work needed to upgrade portions of an agent. Without this flexibility, developers will not be able to adapt their agents to the rapidly changing AI landscape.

#### 4. Security & Regulatory Complicance
Perhaps the most important for the enterprise, support for governance -- security, regulatory compliance -- are factored into overall design. We know implementing security after the fact results in ongoing, inflated costs, in both retro-fitting and starting over. Let's fix that now.


#### 5. Open Source
Anyone can use Eidolon, review it, analyze, and contribute to it. Exclusive licensing and paywalls chill innovation. They don't disrupt the market so much as interrupt it. Open source helps to level the playing field. Improving and refining software remains a community concern, not a product-led marketing initiative.
