---
title: gpt-3.5-turbo
description: "Description of gpt-3.5-turbo component"
---

| Property                                         | Pattern | Type    | Deprecated | Definition | Title/Description    |
| ------------------------------------------------ | ------- | ------- | ---------- | ---------- | -------------------- |
| - [implementation](#implementation )             | No      | const   | No         | -          | gpt-3.5-turbo        |
| - [human_name](#human_name )                     | No      | string  | No         | -          | Human Name           |
| - [name](#name )                                 | No      | string  | No         | -          | Name                 |
| - [input_context_limit](#input_context_limit )   | No      | integer | No         | -          | Input Context Limit  |
| - [output_context_limit](#output_context_limit ) | No      | integer | No         | -          | Output Context Limit |
| - [supports_tools](#supports_tools )             | No      | boolean | No         | -          | Supports Tools       |
| - [supports_image_input](#supports_image_input ) | No      | boolean | No         | -          | Supports Image Input |
| - [supports_audio_input](#supports_audio_input ) | No      | boolean | No         | -          | Supports Audio Input |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** gpt-3.5-turbo

Specific value: `"gpt-3.5-turbo"`

## <a name="human_name"></a>2. Property `human_name`

**Title:** Human Name

|              |                   |
| ------------ | ----------------- |
| **Type**     | `string`          |
| **Required** | No                |
| **Default**  | `"GPT-3.5 Turbo"` |

## <a name="name"></a>3. Property `name`

**Title:** Name

|              |                   |
| ------------ | ----------------- |
| **Type**     | `string`          |
| **Required** | No                |
| **Default**  | `"gpt-3.5-turbo"` |

## <a name="input_context_limit"></a>4. Property `input_context_limit`

**Title:** Input Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `16385`   |

## <a name="output_context_limit"></a>5. Property `output_context_limit`

**Title:** Output Context Limit

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `4096`    |

## <a name="supports_tools"></a>6. Property `supports_tools`

**Title:** Supports Tools

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `true`    |

## <a name="supports_image_input"></a>7. Property `supports_image_input`

**Title:** Supports Image Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `false`   |

## <a name="supports_audio_input"></a>8. Property `supports_audio_input`

**Title:** Supports Audio Input

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `false`   |

----------------------------------------------------------------------------------------------------------------------------
