---
title: ThoughtGenerationStrategy
description: Description of ThoughtGenerationStrategy component
---

| Property                             | Pattern | Type    | Deprecated | Definition | Title/Description         |
| ------------------------------------ | ------- | ------- | ---------- | ---------- | ------------------------- |
| - [implementation](#implementation ) | No      | const   | No         | -          | ThoughtGenerationStrategy |
| - [preamble](#preamble )             | No      | string  | No         | -          | Preamble                  |
| - [thoughts](#thoughts )             | No      | string  | No         | -          | Thoughts                  |
| - [post_amble](#post_amble )         | No      | string  | No         | -          | Post Amble                |
| - [num_children](#num_children )     | No      | integer | No         | -          | Num Children              |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** ThoughtGenerationStrategy

Specific value: `"ThoughtGenerationStrategy"`

## <a name="preamble"></a>2. Property `preamble`

**Title:** Preamble

|              |                                                                                                          |
| ------------ | -------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                 |
| **Required** | No                                                                                                       |
| **Default**  | `"You are an intelligent agent that is generating one thought at a time in a tree of thoughts setting."` |

## <a name="thoughts"></a>3. Property `thoughts`

**Title:** Thoughts

|              |                                                                                                            |
| ------------ | ---------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                   |
| **Required** | No                                                                                                         |
| **Default**  | `"{% if thoughts %}\nTHOUGHTS\n\n{% for thought in thoughts %}\n{{ thought }}\n{% endfor %}\n{% endif %}"` |

## <a name="post_amble"></a>4. Property `post_amble`

**Title:** Post Amble

|              |                                                                                                                                                                                        |
| ------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                                                                                               |
| **Required** | No                                                                                                                                                                                     |
| **Default**  | `"{% if thoughts %}\nPlease generate {{ n }} valid thoughts based on the last valid thought\n{% else %}\nPlease generate {{ n }} valid thoughts based on the question\n{%- endif -%}"` |

## <a name="num_children"></a>5. Property `num_children`

**Title:** Num Children

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `3`       |

**Description:** The number of thoughts to generate.

----------------------------------------------------------------------------------------------------------------------------
