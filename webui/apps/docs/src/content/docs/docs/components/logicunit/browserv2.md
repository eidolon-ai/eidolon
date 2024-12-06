---
title: BrowserV2
description: Description of the BrowserV2 component
---

**Description:** A tool for interacting with a browser instance.

Requires a running browser service.

Exposes two tools to an Agent, one for navigating to a url and another for evaluating javascript on the current page.
Browser sessions are durable throughout a process, but each process has its own browser, isolating browsers between agents.

| Property                                         | Pattern | Type        | Deprecated | Definition | Title/Description    |
| ------------------------------------------------ | ------- | ----------- | ---------- | ---------- | -------------------- |
| + [implementation](#implementation )             | No      | const       | No         | -          | Implementation       |
| - [starting_url](#starting_url )                 | No      | string      | No         | -          | Starting Url         |
| - [browser_service_loc](#browser_service_loc )   | No      | string      | No         | -          | Browser Service Loc  |
| - [navigate_description](#navigate_description ) | No      | string      | No         | -          | Navigate Description |
| - [evaluate_description](#evaluate_description ) | No      | string      | No         | -          | Evaluate Description |
| - [content_description](#content_description )   | No      | string      | No         | -          | Content Description  |
| - [content_summarizer](#content_summarizer )     | No      | Combination | No         | -          | -                    |

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

## <a name="navigate_description"></a>4. Property `navigate_description`

**Title:** Navigate Description

|              |                                                                                                                                                |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                                                       |
| **Required** | No                                                                                                                                             |
| **Default**  | `"Navigate to a url from the current page. Waits for the url to load before returning.\n\nThe current page url as of {datetime} is \"{url}\""` |

## <a name="evaluate_description"></a>5. Property `evaluate_description`

**Title:** Evaluate Description

|              |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| ------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| **Required** | No                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| **Default**  | `"Evaluate javascript on the current page and return the last expression.\nThis is how you interact with the DOM including...\n* retrieving structure\n* filling out forms\n* clicking buttons\n* waiting for events, elements, urls, or other conditions\n\nJavaScript is evaluated using playwright's page.evaluate method.\nThe tool call returns immediately after the last expression is evaluated, so the page may not have fully loaded depending on the provided javascript.\n\nThe current page url as of {datetime} is \"{url}\""` |

## <a name="content_description"></a>6. Property `content_description`

**Title:** Content Description

|              |                                                                                                                                                                |
| ------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | `string`                                                                                                                                                       |
| **Required** | No                                                                                                                                                             |
| **Default**  | `"Get the HTML content of the current page. Content will be summarized to remove unnecessary elements.\n\nThe current page url as of {datetime} is \"{url}\""` |

## <a name="content_summarizer"></a>7. Property `content_summarizer`

|                           |                                                                                                    |
| ------------------------- | -------------------------------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                                                        |
| **Required**              | No                                                                                                 |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.")                          |
| **Default**               | `{"tool_description": "Summarize the current page (Current url: {url})", "mode": "BeautifulSoup"}` |

| Any of(Option)                             |
| ------------------------------------------ |
| [Summarizer](#content_summarizer_anyOf_i0) |
| [item 1](#content_summarizer_anyOf_i1)     |

### <a name="content_summarizer_anyOf_i0"></a>7.1. Property `Summarizer`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | #/$defs/Summarizer                                                        |

| Property                                                             | Pattern | Type             | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------- | ------- | ---------------- | ---------- | ---------- | ----------------- |
| - [tool_description](#content_summarizer_anyOf_i0_tool_description ) | No      | string           | No         | -          | Tool Description  |
| + [mode](#content_summarizer_anyOf_i0_mode )                         | No      | enum (of string) | No         | -          | Mode              |

#### <a name="content_summarizer_anyOf_i0_tool_description"></a>7.1.1. Property `tool_description`

**Title:** Tool Description

|              |                                                     |
| ------------ | --------------------------------------------------- |
| **Type**     | `string`                                            |
| **Required** | No                                                  |
| **Default**  | `"Summarize the current page (Current url: {url})"` |

#### <a name="content_summarizer_anyOf_i0_mode"></a>7.1.2. Property `mode`

**Title:** Mode

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | Yes                |

Must be one of:
* "BeautifulSoup"
* "noop"

### <a name="content_summarizer_anyOf_i1"></a>7.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

----------------------------------------------------------------------------------------------------------------------------
