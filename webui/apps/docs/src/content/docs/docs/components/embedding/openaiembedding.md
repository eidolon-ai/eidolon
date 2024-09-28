---
title: OpenAIEmbedding
description: "Description of OpenAIEmbedding component"
---
# OpenAIEmbedding

- [1. [Optional] Property implementation](#implementation)
- [2. [Optional] Property model](#model)
- [3. [Optional] Property connection_handler](#connection_handler)

**Title:** OpenAIEmbedding

|                           |                                                         |
| ------------------------- | ------------------------------------------------------- |
| **Type**                  | `object`                                                |
| **Required**              | No                                                      |
| **Additional properties** | [[Not allowed]](# "Additional Properties not allowed.") |

<details>
<summary>
<strong> <a name="implementation"></a>1. [Optional] Property implementation</strong>  

</summary>
<blockquote>

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

Specific value: `"OpenAIEmbedding"`

</blockquote>
</details>

<details>
<summary>
<strong> <a name="model"></a>2. [Optional] Property model</strong>  

</summary>
<blockquote>

**Title:** Model

|              |                            |
| ------------ | -------------------------- |
| **Type**     | `string`                   |
| **Required** | No                         |
| **Default**  | `"text-embedding-ada-002"` |

**Description:** The name of the model to use.

</blockquote>
</details>

<details>
<summary>
<strong> <a name="connection_handler"></a>3. [Optional] Property connection_handler</strong>  

</summary>
<blockquote>

|              |                                                 |
| ------------ | ----------------------------------------------- |
| **Type**     | [`Reference[OpenAIConnectionHandler]`](/docs/components/openaiconnectionhandler/overview)            |
| **Required** | No                                              |
| **Default**  | `{"implementation": "OpenAIConnectionHandler"}` |

</blockquote>
</details>

----------------------------------------------------------------------------------------------------------------------------
