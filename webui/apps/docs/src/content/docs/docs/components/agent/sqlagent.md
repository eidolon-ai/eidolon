---
title: SqlAgentSpec
description: "Description of SqlAgentSpec component"
---
# SqlAgentSpec

- [1. Property `client`](#client)
  - [1.1. Property `implementation`](#client_implementation)
- [2. Property `apu`](#apu)
  - [2.1. Property `implementation`](#apu_implementation)
- [3. Property `description`](#description)
- [4. Property `system_prompt`](#system_prompt)
- [5. Property `user_prompt`](#user_prompt)
- [6. Property `clarification_prompt`](#clarification_prompt)
- [7. Property `response_prompt`](#response_prompt)
- [8. Property `error_prompt`](#error_prompt)
- [9. Property `num_retries`](#num_retries)
- [10. Property `implementation`](#implementation)

**Title:** SqlAgentSpec

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

| Property                                         | Pattern | Type    | Deprecated | Definition | Title/Description    |
| ------------------------------------------------ | ------- | ------- | ---------- | ---------- | -------------------- |
| - [client](#client )                             | No      | object  | No         | -          | -                    |
| - [apu](#apu )                                   | No      | object  | No         | -          | -                    |
| - [description](#description )                   | No      | string  | No         | -          | Description          |
| - [system_prompt](#system_prompt )               | No      | string  | No         | -          | System Prompt        |
| - [user_prompt](#user_prompt )                   | No      | string  | No         | -          | User Prompt          |
| - [clarification_prompt](#clarification_prompt ) | No      | string  | No         | -          | Clarification Prompt |
| - [response_prompt](#response_prompt )           | No      | string  | No         | -          | Response Prompt      |
| - [error_prompt](#error_prompt )                 | No      | string  | No         | -          | Error Prompt         |
| - [num_retries](#num_retries )                   | No      | integer | No         | -          | Num Retries          |
| - [implementation](#implementation )             | No      | const   | No         | -          | -                    |

## <a name="client"></a>1. Property `client`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

| Property                                    | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#client_implementation ) | No      | string | No         | -          | -                 |
| - [](#client_additionalProperties )         | No      | object | No         | -          | -                 |

### <a name="client_implementation"></a>1.1. Property `implementation`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

## <a name="apu"></a>2. Property `apu`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

| Property                                 | Pattern | Type   | Deprecated | Definition | Title/Description |
| ---------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#apu_implementation ) | No      | string | No         | -          | -                 |
| - [](#apu_additionalProperties )         | No      | object | No         | -          | -                 |

### <a name="apu_implementation"></a>2.1. Property `implementation`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

## <a name="description"></a>3. Property `description`

**Title:** Description

|              |                                                                                              |
| ------------ | -------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                     |
| **Required** | No                                                                                           |
| **Default**  | `"An agent for interacting with data. Can respond to queries provided in natural language."` |

## <a name="system_prompt"></a>4. Property `system_prompt`

**Title:** System Prompt

|              |                                                                                                                                                                                                                                                                                                                                                                        |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                                                                                                                                                                                                                                                                               |
| **Required** | No                                                                                                                                                                                                                                                                                                                                                                     |
| **Default**  | `"\n    You are a helpful assistant that is a sql expert and helps a user query a {{ protocol }} database and analyse the response.\n    \n    Here is the database schema:\n    {{ metadata }}\n    \n    Use your as needed tools to investigate the database with the goal of providing the user with the query that they need.\n    \n    Think carefully.\n    "` |

## <a name="user_prompt"></a>5. Property `user_prompt`

**Title:** User Prompt

|              |                   |
| ------------ | ----------------- |
| **Type**     | `string`          |
| **Required** | No                |
| **Default**  | `"{{ message }}"` |

## <a name="clarification_prompt"></a>6. Property `clarification_prompt`

**Title:** Clarification Prompt

|              |                                                                                                                 |
| ------------ | --------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                        |
| **Required** | No                                                                                                              |
| **Default**  | `"What clarifying information do you need? Phrase your response as an explicit question or several questions."` |

## <a name="response_prompt"></a>7. Property `response_prompt`

**Title:** Response Prompt

|              |                                                     |
| ------------ | --------------------------------------------------- |
| **Type**     | `string`                                            |
| **Required** | No                                                  |
| **Default**  | `"What is your response? Be explicit and concise."` |

## <a name="error_prompt"></a>8. Property `error_prompt`

**Title:** Error Prompt

|              |                                                                        |
| ------------ | ---------------------------------------------------------------------- |
| **Type**     | `string`                                                               |
| **Required** | No                                                                     |
| **Default**  | `"An error occurred executing the query \"{{ query }}\": {{ error }}"` |

## <a name="num_retries"></a>9. Property `num_retries`

**Title:** Num Retries

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `3`       |

## <a name="implementation"></a>10. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

Specific value: `"SqlAgent"`

----------------------------------------------------------------------------------------------------------------------------
