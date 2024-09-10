---
title: FAQ
description: Frequently Asked Questions
---

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

## Getting Started

To get started with Eidolon, simply click on [Get Started](https://www.eidolonai.com/docs/quickstart). You can join the [Eidolon Discord Server](https://discord.com/invite/eidolon) if you have any questions.

## Features and Functionality

### What is an AI Agent Server?
An AI Agent Server is a deployment server that provides a runtime environment for agents. The Agent Server enables easy deployment and is interoperable with other agents in a secure, scalable, and monitorable way.

### How does Eidolon scale?
Our service-first approach makes it simple to scale requests up to the limits of the environment’s resources. Eidolon agents or services are stateless and can be scaled for performance or redundancy.

### What are Eidolon’s key features?
Eidolon offers 2 key capabilities out of the box:
1. A pluggable AI Agent framework (SDK) for developers to build Agentic applications.
2. An Agent Server based on a microservice architecture, interoperable with other agents, and enabling easy production deployment.

### Why does Eidolon use YAML to configure agent services?
Eidolon uses YAML to simplify the developer experience. Developers familiar with defining Kubernetes resources will understand how to apply this model quickly, facilitating developer adoption and testing.

### Do I need to write code or does Eidolon provide everything for me?
Eidolon provides many prebuilt agents out of the box, requiring no code to put them into production, just configuration. While this is good for many situations, Eidolon also provides an extensive SDK so developers can create new and unique agent types.

### Once I’ve built an agent, how do I deploy it in production?
Eidolon provides two methods to productionalize Machines and Agents:
- **Kubernetes:** Eidolon provides k8s operators that make Eidolon resources like machines, agents, APU’s, etc., first-class k8s objects. Just `kubeapply` your changes, and the resources are updated automatically using a rolling upgrade.
- **Docker:** A single Eidolon machine can be built into a docker container, and you can choose how it is deployed.

### How do agents behave in an Eidolon environment?
Agents in Eidolon are defined as services. Each service is configured as a contract and may be connected to other agent-driven services as the developer sees fit. This service-oriented design promotes horizontal scaling that is simple and straightforward.

Eidolon’s pluggable framework lets developers focus on building secure, flexible, user-centric applications that are easy to deploy without sacrificing data privacy or other compliance requirements.

### Do you have UI widgets that can be used to create a chatbot?
Developers can create their own UI or use the Eidolon provided React components to manage user interaction with a chatbot or chatbot-like application.

## Integrations

### What if I’ve already built Agents on another platform - can they be leveraged with Eidolon and if so how?
Yes, with Eidolon you can easily deploy agents built on other platforms. All Agents in Eidolon are simply services. Integration with other frameworks is as easy as creating a new FastAPI service and defining a deployment descriptor.

### What is the benefit of using Eidolon versus using the OpenAI library hosting on some server and building the UI?
Using Eidolon offers several benefits over directly using the OpenAI library hosting on a server and building a UI:
- **Higher Accuracy:** The framework allows for iterative development which can lead to improved accuracy in AI models.
- **Rapid Deployment:** Eidolon provides an enterprise-ready AI Agent Server and SDK which significantly speeds up the process of building and deploying AI applications.
- **Scalability and Security:** It integrates easily with Kubernetes, allowing for secure and scalable deployment.
- **Extensibility:** Eidolon is designed to be flexible and customizable, allowing developers to build complex AI systems more efficiently.
- **Pre-built Tools:** It offers pre-built agents and React components for easier UI integration.

For more details, visit [Eidolon AI](https://www.eidolonai.com/).

## Security

### How does Eidolon support data privacy?
Eidolon AI lets users control their data. Although it’s easy to connect an agent to user data, the user maintains full control. Complying with international data privacy regulations such as GDPR is simple. Eidolon also supports pluggable privacy components allowing users to install the regulatory support they require.

### How does Eidolon support security requirements?
Our security framework supports any RESTful authentication method. Users can implement the security protocols most appropriate to their needs.

### Can I trust Eidolon? What are the key security and data privacy features?
Eidolon provides built-in authentication with major identity providers, as well as RBAC control to agents and fine-grained access control on agent conversations. If you need something different, it is easy to extend any of these pluggable components with custom behavior.

Eidolon’s approach to agent design can support anything from simple conversational tools to complex state machines executing business logic.

## Technical Support

### I'm having a technical issue where do I get support?
If you're experiencing a technical issue, the best place to get support is our Discord channel. Our team and community members are available there to assist you. Just head over to the #general channel, describe your issue, and someone will help you out shortly.

## Resources and Examples

### I have a specific use case in mind, do you have a repository of examples?
If you have a specific use case in mind, you can explore our repository of examples on our website. Check out the Examples of Agents on Eidolon section on [Eidolon](https://www.eidolonai.com/) to find detailed examples that might match your needs.

## General

### How can I help Eidolon?
Thank you for your generous offer to help. Here are a few ways you can support our vision:

#### Star the [Project](https://github.com/eidolon-ai/eidolon) on GitHub️ ⭐️
This helps increase our visibility and encourages others to check out Eidolon. Your support makes a big difference!

#### Join the Conversation on [Discord](https://discord.com/invite/6kVQrHpeqG) 🧠
Our developers would love to hear from you. Join our Discord server to share your feedback, ask questions, or just say hello.
