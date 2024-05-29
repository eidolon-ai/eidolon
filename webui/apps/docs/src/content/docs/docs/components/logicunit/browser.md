---
title: Browser
description: Description of Browser component
---
# Browser

- [1. Property `Browser > summarizer`](#summarizer)

**Title:** Browser

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

| Property                     | Pattern | Type             | Deprecated | Definition | Title/Description |
| ---------------------------- | ------- | ---------------- | ---------- | ---------- | ----------------- |
| - [summarizer](#summarizer ) | No      | enum (of string) | No         | -          | Summarizer        |

## <a name="summarizer"></a>1. Property `Browser > summarizer`

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
