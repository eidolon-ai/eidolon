---
title: ToTChecker
description: "Description of ToTChecker component"
---

| Property                             | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------ | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#implementation ) | No      | const  | No         | -          | ToTChecker        |
| - [prompt](#prompt )                 | No      | string | No         | -          | Prompt            |
| - [examples](#examples )             | No      | string | No         | -          | Examples          |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ToTChecker

Specific value: `"ToTChecker"`

## <a name="prompt"></a>2. Property `prompt`

**Title:** Prompt

|              |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| ------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| **Required** | No                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| **Default**  | `"You are an intelligent agent, validating thoughts of another intelligent agent.\n\nEvaluate the thoughts and question and respond with one word.\n\n- Respond VALID if the thoughts contain the information needed so answer the question\n- Respond INVALID if the last thought is invalid or does not make progress from previous thoughts.\n- Respond INTERMEDIATE if the last thought is valid but not the final solution to the question.\n\n{% if examples %}\n<EXAMPLEs>\n{{ examples }}\n</EXAMPLE>\n{% endif %}\n\n{% if problem %}\n<QUESTION>\n{{ problem }}\n</QUESTION>\n{% endif %}\n\n{% if thoughts %}\n{% for thought in thoughts %}\n<THOUGHT>\n{{ thought }}\n</THOUGHT>\n{% endfor %}\n{% endif %}"` |

## <a name="examples"></a>3. Property `examples`

**Title:** Examples

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `""`     |

----------------------------------------------------------------------------------------------------------------------------
