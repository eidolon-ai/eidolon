---
title: SimilarityMemoryImpl
description: Description of SimilarityMemoryImpl component
---

| Property                             | Pattern | Type   | Deprecated | Definition                           | Title/Description                  |
| ------------------------------------ | ------- | ------ | ---------- | ------------------------------------ | ---------------------------------- |
| - [implementation](#implementation ) | No      | const  | No         | -                                    | SimilarityMemoryImpl               |
| - [embedder](#embedder )             | No      | object | No         | In [Embedding](/docs/components/embedding/overview)   | Overview of Embedding components   |
| - [vector_store](#vector_store )     | No      | object | No         | In [VectorStore](/docs/components/vectorstore/overview) | Overview of VectorStore components |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** SimilarityMemoryImpl

Specific value: `"SimilarityMemoryImpl"`

## <a name="embedder"></a>2. Property `embedder`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"OpenAIEmbedding"`                                                       |
| **Defined in**            | [Embedding](/docs/components/embedding/overview)                                           |

**Description:** Overview of Embedding components

| One of(Option)                             |
| ------------------------------------------ |
| [NoopEmbedding.json](#embedder_oneOf_i0)   |
| [OpenAIEmbedding.json](#embedder_oneOf_i1) |

### <a name="embedder_oneOf_i0"></a>2.1. Property `NoopEmbedding.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./NoopEmbedding.json                                                 |

| Property                                               | Pattern | Type  | Deprecated | Definition | Title/Description |
| ------------------------------------------------------ | ------- | ----- | ---------- | ---------- | ----------------- |
| - [implementation](#embedder_oneOf_i0_implementation ) | No      | const | No         | -          | NoopEmbedding     |

#### <a name="embedder_oneOf_i0_implementation"></a>2.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** NoopEmbedding

Specific value: `"NoopEmbedding"`

### <a name="embedder_oneOf_i1"></a>2.2. Property `OpenAIEmbedding.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./OpenAIEmbedding.json                                               |

| Property                                                       | Pattern | Type   | Deprecated | Definition                                       | Title/Description                              |
| -------------------------------------------------------------- | ------- | ------ | ---------- | ------------------------------------------------ | ---------------------------------------------- |
| - [implementation](#embedder_oneOf_i1_implementation )         | No      | const  | No         | -                                                | OpenAIEmbedding                                |
| - [model](#embedder_oneOf_i1_model )                           | No      | string | No         | -                                                | Model                                          |
| - [connection_handler](#embedder_oneOf_i1_connection_handler ) | No      | object | No         | In [OpenAIConnectionHandler](/docs/components/openaiconnectionhandler/overview) | Overview of OpenAIConnectionHandler components |

#### <a name="embedder_oneOf_i1_implementation"></a>2.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OpenAIEmbedding

Specific value: `"OpenAIEmbedding"`

#### <a name="embedder_oneOf_i1_model"></a>2.2.2. Property `model`

**Title:** Model

|              |                            |
| ------------ | -------------------------- |
| **Type**     | `string`                   |
| **Required** | No                         |
| **Default**  | `"text-embedding-ada-002"` |

**Description:** The name of the model to use.

#### <a name="embedder_oneOf_i1_connection_handler"></a>2.2.3. Property `connection_handler`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"OpenAIConnectionHandler"`                                               |
| **Defined in**            | [OpenAIConnectionHandler](/docs/components/openaiconnectionhandler/overview)                             |

**Description:** Overview of OpenAIConnectionHandler components

| Property                                                                                    | Pattern | Type            | Deprecated | Definition | Title/Description            |
| ------------------------------------------------------------------------------------------- | ------- | --------------- | ---------- | ---------- | ---------------------------- |
| - [implementation](#embedder_oneOf_i1_connection_handler_implementation )                   | No      | const           | No         | -          | AzureOpenAIConnectionHandler |
| - [azure_ad_token_provider](#embedder_oneOf_i1_connection_handler_azure_ad_token_provider ) | No      | Combination     | No         | -          | -                            |
| - [token_provider_scopes](#embedder_oneOf_i1_connection_handler_token_provider_scopes )     | No      | array of string | No         | -          | Token Provider Scopes        |
| - [api_version](#embedder_oneOf_i1_connection_handler_api_version )                         | No      | string          | No         | -          | Api Version                  |
| - [](#embedder_oneOf_i1_connection_handler_additionalProperties )                           | No      | object          | No         | -          | -                            |

##### <a name="embedder_oneOf_i1_connection_handler_implementation"></a>2.2.3.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AzureOpenAIConnectionHandler

Specific value: `"AzureOpenAIConnectionHandler"`

##### <a name="embedder_oneOf_i1_connection_handler_azure_ad_token_provider"></a>2.2.3.2. Property `azure_ad_token_provider`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

| Any of(Option)                                                                      |
| ----------------------------------------------------------------------------------- |
| [Reference](#embedder_oneOf_i1_connection_handler_azure_ad_token_provider_anyOf_i0) |
| [item 1](#embedder_oneOf_i1_connection_handler_azure_ad_token_provider_anyOf_i1)    |

###### <a name="embedder_oneOf_i1_connection_handler_azure_ad_token_provider_anyOf_i0"></a>2.2.3.2.1. Property `Reference`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | #/$defs/Reference                                                         |

**Description:** Used to create references to other classes. t is designed to be used with two type variables, `B` and `D` which are
the type bound and default type respectively. Neither are required, and if only one type is provided it is assumed
to be the bound. Bound is used as the default if no default is provided. default can also be a string which will be
looked up from the OS ReferenceResources.

Examples:
    Reference(implementation=fqn(Foo)                           # Returns an instance of Foo
    Reference[FooBase](implementation=fqn(Foo)).instantiate()   # Returns an instance of Foo
    Reference[FooBase](implementation=fqn(Bar))                 # Raises ValueError
    Reference[FooBase, Foo]().instantiate()                     # Returns an instance of Foo
    Reference[FooBase]().instantiate()                          # Returns an instance of FooBase

Attributes:
    _bound: This is a type variable `B` that represents the bound type of the reference. It defaults to `object`.
    _default: This is a type variable `D` that represents the default type of the reference. It defaults to `None`.
    implementation: This is a string that represents the fully qualified name of the class that the reference points to. It is optional and can be set to `None`.
    **extra: This is a dictionary that can hold any additional specifications for the reference. It is optional and can be set to `None`.

Methods:
    instantiate: This method is used to create an instance of the class that the reference points to.

| Property                                                                                                   | Pattern | Type   | Deprecated | Definition | Title/Description |
| ---------------------------------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#embedder_oneOf_i1_connection_handler_azure_ad_token_provider_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#embedder_oneOf_i1_connection_handler_azure_ad_token_provider_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

###### <a name="embedder_oneOf_i1_connection_handler_azure_ad_token_provider_anyOf_i0_implementation"></a>2.2.3.2.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

###### <a name="embedder_oneOf_i1_connection_handler_azure_ad_token_provider_anyOf_i1"></a>2.2.3.2.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

##### <a name="embedder_oneOf_i1_connection_handler_token_provider_scopes"></a>2.2.3.3. Property `token_provider_scopes`

**Title:** Token Provider Scopes

|              |                                                    |
| ------------ | -------------------------------------------------- |
| **Type**     | `array of string`                                  |
| **Required** | No                                                 |
| **Default**  | `["https://cognitiveservices.azure.com/.default"]` |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                                                                  | Description |
| ------------------------------------------------------------------------------------------------ | ----------- |
| [token_provider_scopes items](#embedder_oneOf_i1_connection_handler_token_provider_scopes_items) | -           |

###### <a name="autogenerated_heading_2"></a>2.2.3.3.1. token_provider_scopes items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

##### <a name="embedder_oneOf_i1_connection_handler_api_version"></a>2.2.3.4. Property `api_version`

**Title:** Api Version

|              |                |
| ------------ | -------------- |
| **Type**     | `string`       |
| **Required** | No             |
| **Default**  | `"2024-02-01"` |

## <a name="vector_store"></a>3. Property `vector_store`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"ChromaVectorStore"`                                                     |
| **Defined in**            | [VectorStore](/docs/components/vectorstore/overview)                                         |

**Description:** Overview of VectorStore components

| One of(Option)                                   |
| ------------------------------------------------ |
| [ChromaVectorStore.json](#vector_store_oneOf_i0) |
| [NoopVectorStore.json](#vector_store_oneOf_i1)   |

### <a name="vector_store_oneOf_i0"></a>3.1. Property `ChromaVectorStore.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./ChromaVectorStore.json                                             |

| Property                                                                     | Pattern | Type   | Deprecated | Definition | Title/Description       |
| ---------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------------- |
| - [implementation](#vector_store_oneOf_i0_implementation )                   | No      | const  | No         | -          | ChromaVectorStore       |
| - [root_document_directory](#vector_store_oneOf_i0_root_document_directory ) | No      | string | No         | -          | Root Document Directory |
| - [url](#vector_store_oneOf_i0_url )                                         | No      | string | No         | -          | Url                     |

#### <a name="vector_store_oneOf_i0_implementation"></a>3.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ChromaVectorStore

Specific value: `"ChromaVectorStore"`

#### <a name="vector_store_oneOf_i0_root_document_directory"></a>3.1.2. Property `root_document_directory`

**Title:** Root Document Directory

|              |                   |
| ------------ | ----------------- |
| **Type**     | `string`          |
| **Required** | No                |
| **Default**  | `"vector_memory"` |

**Description:** The root directory where the vector memory will store documents.

#### <a name="vector_store_oneOf_i0_url"></a>3.1.3. Property `url`

**Title:** Url

|              |                                             |
| ------------ | ------------------------------------------- |
| **Type**     | `string`                                    |
| **Required** | No                                          |
| **Default**  | `"file://${EIDOLON_DATA_DIR}/doc_producer"` |

**Description:** The url of the chroma database. Use http(s)://$HOST:$PORT?header1=value1&header2=value2 to pass headers to the database.Use file://$PATH to use a local file database.

### <a name="vector_store_oneOf_i1"></a>3.2. Property `NoopVectorStore.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./NoopVectorStore.json                                               |

| Property                                                   | Pattern | Type  | Deprecated | Definition | Title/Description |
| ---------------------------------------------------------- | ------- | ----- | ---------- | ---------- | ----------------- |
| - [implementation](#vector_store_oneOf_i1_implementation ) | No      | const | No         | -          | NoopVectorStore   |

#### <a name="vector_store_oneOf_i1_implementation"></a>3.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** NoopVectorStore

Specific value: `"NoopVectorStore"`

----------------------------------------------------------------------------------------------------------------------------
