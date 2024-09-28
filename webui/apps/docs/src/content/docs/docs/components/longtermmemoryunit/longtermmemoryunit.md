---
title: LongTermMemoryUnit
description: Description of the LongTermMemoryUnit component
---

| Property                             | Pattern | Type               | Deprecated | Definition | Title/Description |
| ------------------------------------ | ------- | ------------------ | ---------- | ---------- | ----------------- |
| + [implementation](#implementation ) | No      | const              | No         | -          | -                 |
| + [user_scoped](#user_scoped )       | No      | boolean            | No         | -          | User Scoped       |
| - [llm_unit](#llm_unit )             | No      | [Reference[LLMUnit]](/docs/components/llmunit/overview) | No         | -          | -                 |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | Yes     |

Specific value: `"LongTermMemoryUnit"`

## <a name="user_scoped"></a>2. Property `user_scoped`

**Title:** User Scoped

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

## <a name="llm_unit"></a>3. Property `llm_unit`

|              |                      |
| ------------ | -------------------- |
| **Type**     | [`Reference[LLMUnit]`](/docs/components/llmunit/overview) |
| **Required** | No                   |
| **Default**  | `null`               |

----------------------------------------------------------------------------------------------------------------------------
