---
title: SqlAgent
description: "Description of SqlAgent component"
---

# SqlAgent

- [1. [Optional] Property implementation](#implementation)
- [2. [Optional] Property client](#client)
- [3. [Optional] Property apu](#apu)
- [4. [Optional] Property description](#description)
- [5. [Optional] Property system_prompt](#system_prompt)
- [6. [Optional] Property user_prompt](#user_prompt)
- [7. [Optional] Property clarification_prompt](#clarification_prompt)
- [8. [Optional] Property response_prompt](#response_prompt)
- [9. [Optional] Property error_prompt](#error_prompt)
- [10. [Optional] Property num_retries](#num_retries)

<details>
<summary>
<strong> <a name="implementation"></a>1. [Optional] Property implementation</strong>  

</summary>
<blockquote>

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

Specific value: `"SqlAgent"`

</blockquote>
</details>

<details>
<summary>
<strong> <a name="client"></a>2. [Optional] Property client</strong>  

</summary>
<blockquote>

|              |                                   |
| ------------ | --------------------------------- |
| **Type**     | [`Reference[SqlClient]`](/docs/components/sqlclient/overview)            |
| **Required** | No                                |
| **Default**  | `{"implementation": "SqlClient"}` |

</blockquote>
</details>

<details>
<summary>
<strong> <a name="apu"></a>3. [Optional] Property apu</strong>  

</summary>
<blockquote>

|              |                             |
| ------------ | --------------------------- |
| **Type**     | [`Reference[APU]`](/docs/components/apu/overview)            |
| **Required** | No                          |
| **Default**  | `{"implementation": "APU"}` |

</blockquote>
</details>

<details>
<summary>
<strong> <a name="description"></a>4. [Optional] Property description</strong>  

</summary>
<blockquote>

**Title:** Description

|              |                                                                                              |
| ------------ | -------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                     |
| **Required** | No                                                                                           |
| **Default**  | `"An agent for interacting with data. Can respond to queries provided in natural language."` |

</blockquote>
</details>

<details>
<summary>
<strong> <a name="system_prompt"></a>5. [Optional] Property system_prompt</strong>  

</summary>
<blockquote>

**Title:** System Prompt

|              |                                                                                                                                                                                                                                                                                                                                                                        |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                                                                                                                                                                                                                                                                               |
| **Required** | No                                                                                                                                                                                                                                                                                                                                                                     |
| **Default**  | `"\n    You are a helpful assistant that is a sql expert and helps a user query a {{ protocol }} database and analyse the response.\n    \n    Here is the database schema:\n    {{ metadata }}\n    \n    Use your as needed tools to investigate the database with the goal of providing the user with the query that they need.\n    \n    Think carefully.\n    "` |

</blockquote>
</details>

<details>
<summary>
<strong> <a name="user_prompt"></a>6. [Optional] Property user_prompt</strong>  

</summary>
<blockquote>

**Title:** User Prompt

|              |                   |
| ------------ | ----------------- |
| **Type**     | `string`          |
| **Required** | No                |
| **Default**  | `"{{ message }}"` |

</blockquote>
</details>

<details>
<summary>
<strong> <a name="clarification_prompt"></a>7. [Optional] Property clarification_prompt</strong>  

</summary>
<blockquote>

**Title:** Clarification Prompt

|              |                                                                                                                 |
| ------------ | --------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                        |
| **Required** | No                                                                                                              |
| **Default**  | `"What clarifying information do you need? Phrase your response as an explicit question or several questions."` |

</blockquote>
</details>

<details>
<summary>
<strong> <a name="response_prompt"></a>8. [Optional] Property response_prompt</strong>  

</summary>
<blockquote>

**Title:** Response Prompt

|              |                                                     |
| ------------ | --------------------------------------------------- |
| **Type**     | `string`                                            |
| **Required** | No                                                  |
| **Default**  | `"What is your response? Be explicit and concise."` |

</blockquote>
</details>

<details>
<summary>
<strong> <a name="error_prompt"></a>9. [Optional] Property error_prompt</strong>  

</summary>
<blockquote>

**Title:** Error Prompt

|              |                                                                        |
| ------------ | ---------------------------------------------------------------------- |
| **Type**     | `string`                                                               |
| **Required** | No                                                                     |
| **Default**  | `"An error occurred executing the query \"{{ query }}\": {{ error }}"` |

</blockquote>
</details>

<details>
<summary>
<strong> <a name="num_retries"></a>10. [Optional] Property num_retries</strong>  

</summary>
<blockquote>

**Title:** Num Retries

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `3`       |

</blockquote>
</details>

----------------------------------------------------------------------------------------------------------------------------
