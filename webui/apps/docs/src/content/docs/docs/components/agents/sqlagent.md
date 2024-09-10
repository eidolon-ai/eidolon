---
title: SqlAgent
description: "Description of SqlAgent component"
---

| Property                                         | Pattern | Type                 | Deprecated | Definition                         | Title/Description                                                                                                                                                                                                                                                                                                                                                                       |
| ------------------------------------------------ | ------- | -------------------- | ---------- | ---------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| - [implementation](#implementation )             | No      | const                | No         | -                                  | SqlAgent                                                                                                                                                                                                                                                                                                                                                                                |
| - [client](#client )                             | No      | Reference[SqlClient] | No         | In [SqlClient](/docs/components/sqlclient/overview) | Overview of SqlClient components                                                                                                                                                                                                                                                                                                                                                        |
| - [apu](#apu )                                   | No      | Reference[APU]       | No         | In [APU](/docs/components/apu/overview)       | The APU is the main interface for the Agent to interact with the LLM.<br />The APU provides a set of capabilities that encapsulate LLM functionality and creates a clear separation between business logic and the underlying LLM implementation.<br /><br />To learn more, check out our blog article APU: [What is it and how does it work?](https://www.eidolonai.com/what_is_apu/). |
| - [description](#description )                   | No      | string               | No         | -                                  | Description                                                                                                                                                                                                                                                                                                                                                                             |
| - [system_prompt](#system_prompt )               | No      | string               | No         | -                                  | System Prompt                                                                                                                                                                                                                                                                                                                                                                           |
| - [user_prompt](#user_prompt )                   | No      | string               | No         | -                                  | User Prompt                                                                                                                                                                                                                                                                                                                                                                             |
| - [clarification_prompt](#clarification_prompt ) | No      | string               | No         | -                                  | Clarification Prompt                                                                                                                                                                                                                                                                                                                                                                    |
| - [response_prompt](#response_prompt )           | No      | string               | No         | -                                  | Response Prompt                                                                                                                                                                                                                                                                                                                                                                         |
| - [error_prompt](#error_prompt )                 | No      | string               | No         | -                                  | Error Prompt                                                                                                                                                                                                                                                                                                                                                                            |
| - [num_retries](#num_retries )                   | No      | integer              | No         | -                                  | Num Retries                                                                                                                                                                                                                                                                                                                                                                             |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** SqlAgent

Specific value: `"SqlAgent"`

## <a name="client"></a>2. Property `client`

|                |                                   |
| -------------- | --------------------------------- |
| **Type**       | `Reference[SqlClient]`            |
| **Required**   | No                                |
| **Default**    | `{"implementation": "SqlClient"}` |
| **Defined in** | [SqlClient](/docs/components/sqlclient/overview)   |

**Description:** Overview of SqlClient components

## <a name="apu"></a>3. Property `apu`

|                |                             |
| -------------- | --------------------------- |
| **Type**       | `Reference[APU]`            |
| **Required**   | No                          |
| **Default**    | `{"implementation": "APU"}` |
| **Defined in** | [APU](/docs/components/apu/overview)   |

**Description:** The APU is the main interface for the Agent to interact with the LLM.
The APU provides a set of capabilities that encapsulate LLM functionality and creates a clear separation between business logic and the underlying LLM implementation.

To learn more, check out our blog article APU: [What is it and how does it work?](https://www.eidolonai.com/what_is_apu/).

## <a name="description"></a>4. Property `description`

**Title:** Description

|              |                                                                                              |
| ------------ | -------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                     |
| **Required** | No                                                                                           |
| **Default**  | `"An agent for interacting with data. Can respond to queries provided in natural language."` |

## <a name="system_prompt"></a>5. Property `system_prompt`

**Title:** System Prompt

|              |                                                                                                                                                                                                                                                                                                                                                                        |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                                                                                                                                                                                                                                                                               |
| **Required** | No                                                                                                                                                                                                                                                                                                                                                                     |
| **Default**  | `"\n    You are a helpful assistant that is a sql expert and helps a user query a {{ protocol }} database and analyse the response.\n    \n    Here is the database schema:\n    {{ metadata }}\n    \n    Use your as needed tools to investigate the database with the goal of providing the user with the query that they need.\n    \n    Think carefully.\n    "` |

## <a name="user_prompt"></a>6. Property `user_prompt`

**Title:** User Prompt

|              |                   |
| ------------ | ----------------- |
| **Type**     | `string`          |
| **Required** | No                |
| **Default**  | `"{{ message }}"` |

## <a name="clarification_prompt"></a>7. Property `clarification_prompt`

**Title:** Clarification Prompt

|              |                                                                                                                 |
| ------------ | --------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                        |
| **Required** | No                                                                                                              |
| **Default**  | `"What clarifying information do you need? Phrase your response as an explicit question or several questions."` |

## <a name="response_prompt"></a>8. Property `response_prompt`

**Title:** Response Prompt

|              |                                                     |
| ------------ | --------------------------------------------------- |
| **Type**     | `string`                                            |
| **Required** | No                                                  |
| **Default**  | `"What is your response? Be explicit and concise."` |

## <a name="error_prompt"></a>9. Property `error_prompt`

**Title:** Error Prompt

|              |                                                                        |
| ------------ | ---------------------------------------------------------------------- |
| **Type**     | `string`                                                               |
| **Required** | No                                                                     |
| **Default**  | `"An error occurred executing the query \"{{ query }}\": {{ error }}"` |

## <a name="num_retries"></a>10. Property `num_retries`

**Title:** Num Retries

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `3`       |

----------------------------------------------------------------------------------------------------------------------------
