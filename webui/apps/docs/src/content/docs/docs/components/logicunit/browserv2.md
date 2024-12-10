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
| - [operation_description](#operation_description ) | No      | string      | No         | -          | Operation Description |
| - [content_summarizer](#content_summarizer )       | No      | Combination | No         | -          | -                     |

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

## <a name="operation_description"></a>4. Property `operation_description`

**Title:** Operation Description

|              |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Type**     | `string`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| **Required** | No                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| **Default**  | `"Perform the specified operation on the current page. The operation is executed using a playwright \"Page\" object.\n\nPrefer using fill / click to interact with the page over executing raw javascript when possible.\n\nREMEMBER: A selector can match multiple elements, and that the first element found will be interacted with. Be sure \nto specify an index if you are using a selector that could have multiple matches. For example, to find the second \ndiv with class \"foo\", you could use \"(//div[contains(@class, 'foo')])[2]\".\n\nThe current page url as of {datetime} is \"{url}\""` |

## <a name="content_summarizer"></a>5. Property `content_summarizer`

|                           |                                                                                                                                                   |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                                                                                                       |
| **Required**              | No                                                                                                                                                |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.")                                                                         |
| **Default**               | `{"tool_description": "Summarize the current page (Current url: {url})", "mode": "BeautifulSoup", "encoding": "o200k_base", "token_limit": 8000}` |

| Any of(Option)                             |
| ------------------------------------------ |
| [Summarizer](#content_summarizer_anyOf_i0) |
| [item 1](#content_summarizer_anyOf_i1)     |

### <a name="content_summarizer_anyOf_i0"></a>5.1. Property `Summarizer`

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
| - [encoding](#content_summarizer_anyOf_i0_encoding )                 | No      | string           | No         | -          | Encoding          |
| - [token_limit](#content_summarizer_anyOf_i0_token_limit )           | No      | Combination      | No         | -          | Token Limit       |

#### <a name="content_summarizer_anyOf_i0_tool_description"></a>5.1.1. Property `tool_description`

**Title:** Tool Description

|              |                                                     |
| ------------ | --------------------------------------------------- |
| **Type**     | `string`                                            |
| **Required** | No                                                  |
| **Default**  | `"Summarize the current page (Current url: {url})"` |

#### <a name="content_summarizer_anyOf_i0_mode"></a>5.1.2. Property `mode`

**Title:** Mode

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | Yes                |

Must be one of:
* "BeautifulSoup"
* "noop"

#### <a name="content_summarizer_anyOf_i0_encoding"></a>5.1.3. Property `encoding`

**Title:** Encoding

|              |                |
| ------------ | -------------- |
| **Type**     | `string`       |
| **Required** | No             |
| **Default**  | `"o200k_base"` |

**Description:** tiktoken encoding to use when counting tokens

#### <a name="content_summarizer_anyOf_i0_token_limit"></a>5.1.4. Property `token_limit`

**Title:** Token Limit

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `8000`                                                                    |

**Description:** The maximum number of message tokens to sent respond with

| Any of(Option)                                              |
| ----------------------------------------------------------- |
| [item 0](#content_summarizer_anyOf_i0_token_limit_anyOf_i0) |
| [item 1](#content_summarizer_anyOf_i0_token_limit_anyOf_i1) |

##### <a name="content_summarizer_anyOf_i0_token_limit_anyOf_i0"></a>5.1.4.1. Property `item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

##### <a name="content_summarizer_anyOf_i0_token_limit_anyOf_i1"></a>5.1.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

### <a name="content_summarizer_anyOf_i1"></a>5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

----------------------------------------------------------------------------------------------------------------------------
