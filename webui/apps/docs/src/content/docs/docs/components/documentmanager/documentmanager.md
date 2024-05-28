---
title: DocumentManager
description: Description of DocumentManager component
---
*Manages a collection of documents and provides search functionality. Automatically embeds and syncs documents (
provided by loader) into similarity memory where they can be searched.*

## Properties

- **`name`** *(string)*: The name of the document manager (used to name database collections).
- **`recheck_frequency`** *(integer)*: The number of seconds between checks. Default: `60`.
- **`loader`** *([Reference[DocumentLoader]](/docs/components/documentloader/overview/))*: Default: `"DocumentLoader"`.
- **`doc_processor`** *(Reference[DocumentProcessor])*: Default: `"DocumentProcessor"`.
