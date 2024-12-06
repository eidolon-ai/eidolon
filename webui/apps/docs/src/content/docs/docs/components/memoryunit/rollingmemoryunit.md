---
title: RollingMemoryUnit
description: Description of the RollingMemoryUnit component
---

**Description:** Memory unit that only retrieves the most recent messages that are under a token limit. Does not summarize removed messages.

| Property                             | Pattern | Type    | Deprecated | Definition | Title/Description |
| ------------------------------------ | ------- | ------- | ---------- | ---------- | ----------------- |
| + [implementation](#implementation ) | No      | const   | No         | -          | Implementation    |
| - [encoding](#encoding )             | No      | string  | No         | -          | Encoding          |
| - [token_limit](#token_limit )       | No      | integer | No         | -          | Token Limit       |

## <a name="implementation"></a>1. Property `implementation`

**Title:** Implementation

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | Yes     |

Specific value: `"RollingMemoryUnit"`

## <a name="encoding"></a>2. Property `encoding`

**Title:** Encoding

|              |                |
| ------------ | -------------- |
| **Type**     | `string`       |
| **Required** | No             |
| **Default**  | `"o200k_base"` |

**Description:** tiktoken encoding to use when counting tokens

## <a name="token_limit"></a>3. Property `token_limit`

**Title:** Token Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `32000`   |

**Description:** The maximum number of message tokens to sent to llm

----------------------------------------------------------------------------------------------------------------------------
