# Parallel Search MCP

This opt-in `ParallelSearch` tool bundle discovers `web_search` and `web_fetch`
from [Parallel Search MCP](https://docs.parallel.ai/integrations/mcp/search-mcp)
and dispatches them through Eidolon's native tools. It uses Streamable HTTP at
`https://search.parallel.ai/mcp`, with JSON and SSE responses supported.
No Parallel API key is needed or read. Existing agents and Google search defaults
are unchanged. Anonymous access has lower rate limits and is intended for light
use; LLM inference is separate.

From the repository root, install the SDK in a fresh Python 3.11 environment:

```sh
python3.11 -m venv .venv
.venv/bin/pip install ./sdk
.venv/bin/python examples/parallel_search/verify.py
```

The verification script loads the logic unit from `resources/agent.yaml`,
discovers the current tool schemas, then executes a search and fetch through
`LLMToolWrapper`. It prints MCP content blocks containing source URLs and
excerpts. It does not call an LLM or need model credentials.

To use the bundle with a `SimpleAgent`, copy the `apu.logic_units` entry from
`resources/agent.yaml` into your agent configuration. Append it to any existing
logic units you want to keep. To run the included agent, configure your usual
LLM credentials (for the default OpenAI model, set `OPENAI_API_KEY`) and run:

```sh
.venv/bin/eidolon-server examples/parallel_search/resources
```

Use the server's `/docs` interface to create a `ParallelResearcher` process and
call its `converse` action with a research question. The tools expose the server's
current argument schemas and return the MCP result unchanged. Search takes an
`objective` and `search_queries`; fetch takes `urls` and optional excerpt guidance.
Eidolon supplies a stable conversation identifier for both tools.

`timeout` sets the deadline for tool discovery or execution, defaulting to 60
seconds. Cancellation propagates to the HTTP caller. HTTP errors, including rate
limits, MCP protocol errors and tool errors propagate to Eidolon; requests are
not automatically retried. Every request includes an Eidolon User-Agent.
