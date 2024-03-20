# Tired of Writing Documentation?

Welcome to an exciting journey into the world of documentation. Sometimes you just want to focus on coding, leaving the documentation to someone—or something—else.

In this guide, we embark on creating a code search example. By the end, you'll have crafted an agent capable of writing documents and leveraging the power of RAG to sift through your project's documents and files. Let's dive in!

tldr: [deployment script](#run_server)

## Understanding the Components

Our adventure begins in the `resources` directory, where the magic happens. Here's a quick overview of the key components:

### Document Producer Agent
This agent stands at the core of our operation, tasked with crafting the documentation. Picture it as the master chef in a gourmet kitchen, ensuring every piece of documentation is meticulously prepared.

Here's a peak at the agent's definition:
```yaml
apiVersion: eidolon/v1
kind: Agent
metadata:
  name: doc_producer

spec:
  description: An agent that searches the eidolon code and documentation
  agent_refs: ["SearchCode", "SearchDocs"]
  system_prompt: ...
```
The default Agent (SimpleAgent) acts as a conversational agent driven by a system prompt. Here The `agent_refs` field specifies other agents who will act as the RAG components it employs to search for code and documentation, highlighting its resourcefulness.

### Search Code/Doc Agents
These components, our RAG equivalents for code and document files, serve as the specialized sous-chefs of our operation. One knows code, while the other adeptly navigates documentation.

Their configuration reflects their specialized functions:
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
A RetrieverAgent retrieves documents from a designated location, driven by a query for similarity search. Here, it's set to comb through the documentation directory, with the `SearchCode` agent performing a similar role for the code files within the Eidolon `sdk` directory.

## <a name="run_server">Setting Up the Server</a>

Initiate your Eidolon server with the following commands, setting the stage for our document-producing agent to work its magic:

```bash
git clone https://github.com/eidolon-ai/eidolon.git
cd eidolon/examples
poetry install
poetry run eidolon-server eidolon_examples/code_search/resources
```

## Sample Request
With the server operational, it's time to put our setup to the test with a sample request. Our doc_producer agent stands ready to generate the needed documentation.

First create a process for your conversation.

```bash
curl -X 'POST' 'http://localhost:8080/processes' -H 'Content-Type: application/json' -d '{
  "agent": "doc_producer",
  "title": "Produce Some Docs!"
}'
````

The result should be a json object with a process id. For example:

```json
{"process_id":"hello_world-1"}
```

Now let's try to make a request to your server.

```bash
curl -X 'POST' \
  'http://localhost:8080/processes/{process_id}/agent/doc_producer/actions/question' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{ "instruction": "How do I create an Agent? Be concise" }'
```

Where `{process_id}` is the process id you received from the previous request.

## Self-Exploration Challenge

Having covered the basics, challenge yourself to delve deeper into the Eidolon ecosystem. Here's how you can expand your knowledge:

- Don't just genrate our docs, build a documentation generator for your own personal project.
- Craft a custom agent tailored for specific documentation types, like API guides or tutorial walkthroughs.
- Experiment with adding new RAG components to bolster the agent's functionality. Perhaps develop an S3 rag component?

## Conclusion

Congratulations on your first foray into Eidolon's world, crafting a code search example that's both functional and inspiring. This is just the beginning—Eidolon's vast landscape brims with opportunities for discovery and innovation. Embark on your journey with creativity and curiosity. Happy coding!
