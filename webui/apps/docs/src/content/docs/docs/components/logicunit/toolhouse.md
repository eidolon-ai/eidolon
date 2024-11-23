---
title: Toolhouse
description: Description of the Toolhouse component
---

**Description:** A configurable tool backed by Toolhouse.ai that can be added to Eidolon Agents.
Toolhouse is the complete cloud infrastructure to equip LLMs with actions and knowledge.

| Property                             | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------ | ------- | ------ | ---------- | ---------- | ----------------- |
| + [implementation](#implementation ) | No      | const  | No         | -          | Implementation    |
| - [api_key](#api_key )               | No      | string | No         | -          | Api Key           |
| - [bundle](#bundle )                 | No      | string | No         | -          | Bundle            |
| - [base_url](#base_url )             | No      | string | No         | -          | Base Url          |

## <a name="implementation"></a>1. Property `implementation`

**Title:** Implementation

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | Yes     |

Specific value: `"Toolhouse"`

## <a name="api_key"></a>2. Property `api_key`

**Title:** Api Key

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Toolhouse API_KEY to connect toolhouse.

## <a name="bundle"></a>3. Property `bundle`

**Title:** Bundle

|              |             |
| ------------ | ----------- |
| **Type**     | `string`    |
| **Required** | No          |
| **Default**  | `"default"` |

**Description:** groups of tools you want to pass to the LLM based on specific contextual need of each LLM call or agent.

## <a name="base_url"></a>4. Property `base_url`

**Title:** Base Url

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

----------------------------------------------------------------------------------------------------------------------------
