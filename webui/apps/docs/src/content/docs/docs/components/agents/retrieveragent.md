---
title: RetrieverAgent
description: Description of RetrieverAgent component
---
*A RetrieverAgent is an agent that will take a query, rewrite it for better similarity vector search, and then perform the vector search on the document store.
The agent will dynamically load and embed files, so it is not performant for loading large bodies of files, but performs very well for small to medium-sized document stores (hundreds to thousands of documents) which are updating frequently.*

## Properties

- **`max_num_results`** *(integer)*: The maximum number of results to send to cpu. Default: `10`.
- **`question_transformer`** *(Reference[QuestionTransformer])*: Default: `"QuestionTransformer"`.
- **`document_reranker`** *(Reference[DocumentReranker])*: Default: `"DocumentReranker"`.
- **`name`** *(string)*: The name of the document store to use.
- **`description`** *(string)*: A detailed description of the the retriever including all necessary information for the calling agent to decide to call this agent, i.e. file type or location or etc...
- **`loader_root_location`** *(string)*: A URL specifying the root location of the loader. Default: `null`.
- **`loader_pattern`** *(string)*: The search pattern to use when loading files. Default: `"**/*"`.
- **`document_manager`** *([Reference[DocumentManager]](/docs/components/documentmanager/overview/))*: Default: `"eidolon_ai_sdk.agent.doc_manager.document_manager.DocumentManager"`.
