---
title: Browser
description: "Description of Browser component"
---
# Schema Docs

- [1. Property `implementation`](#implementation)
- [2. Property `summarizer`](#summarizer)

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

| Property                             | Pattern | Type             | Deprecated | Definition | Title/Description |
| ------------------------------------ | ------- | ---------------- | ---------- | ---------- | ----------------- |
| - [implementation](#implementation ) | No      | const            | No         | -          | -                 |
| - [summarizer](#summarizer )         | No      | enum (of string) | No         | -          | Summarizer        |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

Specific value: `"Browser"`

## <a name="summarizer"></a>2. Property `summarizer`

**Title:** Summarizer

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | No                 |
| **Default**  | `"BeautifulSoup"`  |

Must be one of:
* "BeautifulSoup"
* "noop"

----------------------------------------------------------------------------------------------------------------------------
