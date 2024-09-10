---
title: Browser
description: "Description of Browser component"
---

| Property                             | Pattern | Type             | Deprecated | Definition | Title/Description |
| ------------------------------------ | ------- | ---------------- | ---------- | ---------- | ----------------- |
| - [implementation](#implementation ) | No      | const            | No         | -          | Browser           |
| - [summarizer](#summarizer )         | No      | enum (of string) | No         | -          | Summarizer        |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** Browser

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
