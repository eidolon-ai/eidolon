# Tired of Writing Documentation? Let an Agent handle that

Welcome to an exciting journey into the world of ...documentation. Although this is surely the most fascinating part of 
building software, sometimes a dev has more pressing matters at hand. Like literally anything else.

Here we'll embark on creating a code search example. By the end of this guide, you'll have crafted an agent capable of 
writing documents, leveraging the power RAG to search through your project's documents and files. Let's dive in!

## Understanding the Components

Our adventure begins in the `resources` directory, where the magic happens. Here's a brief overview of the key players:

### Document Producer
This agent is the heart of our operation, responsible for producing the documentation. It's 
like the master chef in a gourmet kitchen, ensuring every dish (or document, in our case) is prepared to perfection.

Let's take a look at the agent's definition:
```yaml
apiVersion: eidolon/v1
kind: Agent
metadata:
  name: doc_producer
spec:
  implementation: GenericAgent
  description: An agent that searches the eidolon code and documentation
  agent_refs: ["SearchCode", "SearchDocs"]
  system_prompt: ...
  user_prompt: ...
```
We want a "GenericAgent" which is a simple conversational agent. What's interesting here is the `agent_refs` field. This 
is where we specify the RAG components that our agent will use to search for code and documentation. 

### Search Code/Docs
These are our RAG components for the code and document files, respectively. Think of them as the sous-chefs, each with a specialized skill set. One excels in sifting through code, while the other navigates documents with ease.

These agents are not conversational agents, so the yaml here is going to look a little different.
```yaml
apiVersion: eidolon/v1
kind: Agent
metadata:
  name: SearchDocs

spec:
  implementation: RetrieverAgent
  name: "search_docs"
  description: "Searches for snippets in the documentation"
  loader_root_location: "file://../docs/src/content/docs"
```
A RetrieverAgent is an agent that can retrieve documents from a specified location. Its interface is defined by a query
which will drive a similarity search. 

In this case, we're searching through the documentation in the `docs` directory. As you would expect, the `SearchCode` 
agent looks very similar, but it's searching through the files in the eidolon `sdk` directory.


### Similarity Memory
The RetrieverAgents need vector search to be enabled on the machine. Sticking with our kitchen analogy, vector search is 
like our pizza oven. You only want to build a kitchen with a pizza oven if you're going to be making pizza. Or documentation in our case.

As defined by the [builtin references](https://github.com/eidolon-ai/eidolon/blob/main/sdk/eidolon_ai_sdk/builtins/code_builtins.py),
Embedding and Vector Store both point towards a noop implementation. Fortunately we can easy redefine these references 
and the new defaults will be picked up throughout your machine. 
```yaml
apiVersion: eidolon/v1
kind: Reference
metadata:
  name: Embedding
spec: OpenAIEmbedding
```
```yaml
apiVersion: eidolon/v1
kind: Reference
metadata:
  name: VectorStore
spec: ChromaVectorStore
```

## Setting Up the Server

To bring our code search example to life, we need to set up the server. Here's how:

```bash
git clone https://github.com/eidolon-ai/eidolon.git
cd eidolon/examples
poetry install
poetry run eidolon-server eidolon_examples/code_search/resources

```

This command is your key to unlocking the Eidolon server, setting the stage for our document-producing agent to perform its magic.

## Sample Request

With the server up and running, it's time to test our setup with a sample request to our doc_producer agent who is eagerly awaiting the documentation it will produce.

## Self-Exploration Challenge

Now that you've seen the basics, it's time for a challenge! Dive deeper into the Eidolon ecosystem and explore its capabilities further. Here are a few ideas to get you started:

- Create a custom agent that specializes in a specific type of documentation, such as API guides or tutorial walkthroughs.
- Explore creating additional RAG components to enhance the agent's capabilities. Can you build a S3 rag component?

## Conclusion

Congratulations! You've taken your first steps into the fascinating world of Eidolon, creating a code search example that not only serves a practical purpose but also sparks curiosity and exploration. Remember, the journey doesn't end here. Eidolon offers a vast landscape of possibilities, waiting for you to discover and innovate. Happy coding!
