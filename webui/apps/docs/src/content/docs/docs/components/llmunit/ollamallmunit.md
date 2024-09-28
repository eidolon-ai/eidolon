---
title: OllamaLLMUnit
description: "Description of OllamaLLMUnit component"
---
# OllamaLLMUnit

- [1. [Optional] Property implementation](#implementation)
- [2. [Optional] Property model](#model)
- [3. [Optional] Property temperature](#temperature)
- [4. [Optional] Property force_json](#force_json)
- [5. [Optional] Property max_tokens](#max_tokens)
- [6. [Optional] Property client_options](#client_options)

**Title:** OllamaLLMUnit

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

Specific value: `"OllamaLLMUnit"`

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
<strong> <a name="client_options"></a>6. [Optional] Property client_options</strong>  

</summary>
<blockquote>

**Title:** Client Options

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

</blockquote>
</details>

----------------------------------------------------------------------------------------------------------------------------
