---
title: BrowserV2
description: Description of the BrowserV2 component
---

**Description:** A tool for interacting with a browser instance.

Requires a running browser service.

Exposes two tools to an Agent, one for navigating to a url and another for evaluating javascript on the current page.
Browser sessions are durable throughout a process, but each process has its own browser, isolating browsers between agents.

| Property                                           | Pattern | Type        | Deprecated | Definition | Title/Description     |
| -------------------------------------------------- | ------- | ----------- | ---------- | ---------- | --------------------- |
| + [implementation](#implementation )               | No      | const       | No         | -          | Implementation        |
| - [starting_url](#starting_url )                   | No      | string      | No         | -          | Starting Url          |
| - [browser_service_loc](#browser_service_loc )     | No      | string      | No         | -          | Browser Service Loc   |
| - [go_to_url_description](#go_to_url_description ) | No      | string      | No         | -          | Go To Url Description |
| - [go_to_url_summarizer](#go_to_url_summarizer )   | No      | Combination | No         | -          | -                     |
| - [evaluate_description](#evaluate_description )   | No      | string      | No         | -          | Evaluate Description  |

## <a name="implementation"></a>1. Property `implementation`

**Title:** Implementation

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | Yes     |

Specific value: `"BrowserV2"`

## <a name="starting_url"></a>2. Property `starting_url`

**Title:** Starting Url

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

## <a name="browser_service_loc"></a>3. Property `browser_service_loc`

**Title:** Browser Service Loc

|              |                           |
| ------------ | ------------------------- |
| **Type**     | `string`                  |
| **Required** | No                        |
| **Default**  | `"http://localhost:7468"` |

**Description:** The location of the playwright installation.

**Example:** 

```yaml
http://localhost:7468
```

## <a name="go_to_url_description"></a>4. Property `go_to_url_description`

**Title:** Go To Url Description

|              |                           |
| ------------ | ------------------------- |
| **Type**     | `string`                  |
| **Required** | No                        |
| **Default**  | `"Go to a specified url"` |

## <a name="go_to_url_summarizer"></a>5. Property `go_to_url_summarizer`

|                           |                                                                                                    |
| ------------------------- | -------------------------------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                                                        |
| **Required**              | No                                                                                                 |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.")                          |
| **Default**               | `{"tool_description": "Summarize the current page (Current url: {url})", "mode": "BeautifulSoup"}` |

| Any of(Option)                               |
| -------------------------------------------- |
| [Summarizer](#go_to_url_summarizer_anyOf_i0) |
| [item 1](#go_to_url_summarizer_anyOf_i1)     |

### <a name="go_to_url_summarizer_anyOf_i0"></a>5.1. Property `Summarizer`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | #/$defs/Summarizer                                                        |

| Property                                                               | Pattern | Type             | Deprecated | Definition | Title/Description |
| ---------------------------------------------------------------------- | ------- | ---------------- | ---------- | ---------- | ----------------- |
| - [tool_description](#go_to_url_summarizer_anyOf_i0_tool_description ) | No      | string           | No         | -          | Tool Description  |
| + [mode](#go_to_url_summarizer_anyOf_i0_mode )                         | No      | enum (of string) | No         | -          | Mode              |

#### <a name="go_to_url_summarizer_anyOf_i0_tool_description"></a>5.1.1. Property `tool_description`

**Title:** Tool Description

|              |                                                     |
| ------------ | --------------------------------------------------- |
| **Type**     | `string`                                            |
| **Required** | No                                                  |
| **Default**  | `"Summarize the current page (Current url: {url})"` |

#### <a name="go_to_url_summarizer_anyOf_i0_mode"></a>5.1.2. Property `mode`

**Title:** Mode

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | Yes                |

Must be one of:
* "BeautifulSoup"
* "noop"

### <a name="go_to_url_summarizer_anyOf_i1"></a>5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

## <a name="evaluate_description"></a>6. Property `evaluate_description`

**Title:** Evaluate Description

|              |                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Type**     | `string`                                                                                                                                                                                                                                                                                                                                                                                                           |
| **Required** | No                                                                                                                                                                                                                                                                                                                                                                                                                 |
| **Default**  | `"Evaluate javascript on the current page and return the last expression. This is how you interact with the DOM including retrieving structure, filling out forms, clicking buttons, etc.\n\nWill return immediately after the last expression is evaluated, so the page may not have fully loaded yet. If you need to wait for the page to load, do so explicitly or poll the page state.\n\nCurrent url: {url}"` |

----------------------------------------------------------------------------------------------------------------------------
