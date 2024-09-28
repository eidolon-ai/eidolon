---
title: OpenAIGPT
description: "Description of OpenAIGPT component"
---
# OpenAIGPT

- [1. [Optional] Property implementation](#implementation)
- [2. [Optional] Property model](#model)
- [3. [Optional] Property temperature](#temperature)
- [4. [Optional] Property force_json](#force_json)
- [5. [Optional] Property max_tokens](#max_tokens)
- [6. [Optional] Property supports_system_messages](#supports_system_messages)
- [7. [Optional] Property can_stream](#can_stream)
- [8. [Optional] Property connection_handler](#connection_handler)

**Title:** OpenAIGPT

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

Specific value: `"OpenAIGPT"`

</blockquote>
</details>

<details>
<summary>
<strong> <a name="model"></a>2. [Optional] Property model</strong>  

</summary>
<blockquote>

|              |                                     |
| ------------ | ----------------------------------- |
| **Type**     | [`Reference[LLMModel]`](/docs/components/llmmodel/overview)               |
| **Required** | No                                  |
| **Default**  | `{"implementation": "gpt-4-turbo"}` |

</blockquote>
</details>

<details>
<summary>
<strong> <a name="temperature"></a>3. [Optional] Property temperature</strong>  

</summary>
<blockquote>

**Title:** Temperature

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0.3`    |

</blockquote>
</details>

<details>
<summary>
<strong> <a name="force_json"></a>4. [Optional] Property force_json</strong>  

</summary>
<blockquote>

**Title:** Force Json

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

</blockquote>
</details>

<details>
<summary>
<strong> <a name="max_tokens"></a>5. [Optional] Property max_tokens</strong>  

</summary>
<blockquote>

**Title:** Max Tokens

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `null`    |

</blockquote>
</details>

<details>
<summary>
<strong> <a name="supports_system_messages"></a>6. [Optional] Property supports_system_messages</strong>  

</summary>
<blockquote>

**Title:** Supports System Messages

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

</blockquote>
</details>

<details>
<summary>
<strong> <a name="can_stream"></a>7. [Optional] Property can_stream</strong>  

</summary>
<blockquote>

**Title:** Can Stream

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

</blockquote>
</details>

<details>
<summary>
<strong> <a name="connection_handler"></a>8. [Optional] Property connection_handler</strong>  

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
