---
title: RetrieverAgent
description: Component - RetrieverAgent
---
A `RetrieverAgent` is an agent that will take a query, rewrite it for better similarity vector search, and then perform
the vector search on the document store. 

The agent will dynamically load and embed files, so it is not performant for loading large bodies of files, but performs
very well for small to medium-sized document stores (hundreds to thousands of documents) which are updating frequently.


## Spec

| Key                  | Description                                                                                                                                                                                                                           |
|----------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| name                 | `type`: str<br/>`Description:` The name of the document store to use.                                                                                                                                                                 |
| description          | `type`: str<br/>`Description:` A detailed description of the retriever including all necessary information for the calling agent to decide to call this agent, i.e., file type, location, etc.                                        |
| loader_root_location | `type`: str<br/>`Default`: None<br/>`Description:` A URL specifying the root location of the loader. This should be a `file://` URL to specify the directory from which files are loaded. Passed to Loader.                           |
| loader_pattern       | `type`: str<br/>`Default`: "**/*"<br/>`Description:` The search pattern to use when loading files. This pattern determines which files are considered by the loader based on their names and locations relative to the root location. |
| document_manager     | `type`: Reference[DocumentManager]<br/>`Description:` A reference to the `DocumentManager` that manages the documents loaded by this retriever. This includes handling the specifics of document storage, retrieval, and management.  |

