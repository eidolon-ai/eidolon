
---
title: RetrieverAgent
description: RetrieverAgent
---
# RetrieverAgent

## Properties

- **`max_num_results`** *(integer)*: The maximum number of results to send to cpu. Default: `10`.
- **`question_transformer`** *(Reference[QuestionTransformer])*: Default: `"QuestionTransformer"`.
- **`document_reranker`** *(Reference[DocumentReranker])*: Default: `"DocumentReranker"`.
- **`name`** *(string)*: The name of the document store to use.
- **`description`** *(string)*: A detailed description of the the retriever including all necessary information for the calling agent to decide to call this agent, i.e. file type or location or etc...
- **`loader_root_location`** *(string)*: A URL specifying the root location of the loader. Default: `null`.
- **`loader_pattern`** *(string)*: The search pattern to use when loading files. Default: `"**/*"`.
- **`document_manager`** *(Reference[DocumentManager])*: Default: `"eidolon_ai_sdk.agent.doc_manager.document_manager.DocumentManager"`.
