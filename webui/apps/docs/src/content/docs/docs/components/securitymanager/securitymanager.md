---
title: SecurityManager
description: "Description of SecurityManager component"
---

| Property                                                 | Pattern | Type            | Deprecated | Definition           | Title/Description                                                                                             |
| -------------------------------------------------------- | ------- | --------------- | ---------- | -------------------- | ------------------------------------------------------------------------------------------------------------- |
| - [implementation](#implementation )                     | No      | const           | No         | -                    | -                                                                                                             |
| - [authentication_processor](#authentication_processor ) | No      | object          | No         | In file:../test.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |
| - [functional_authorizer](#functional_authorizer )       | No      | object          | No         | In file:../test.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |
| - [process_authorizer](#process_authorizer )             | No      | object          | No         | In file:../test.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |
| - [safe_paths](#safe_paths )                             | No      | array of string | No         | -                    | Safe Paths                                                                                                    |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

Specific value: `"SecurityManager"`

## <a name="authentication_processor"></a>2. Property `authentication_processor`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:../test.json                                                         |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

## <a name="functional_authorizer"></a>3. Property `functional_authorizer`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:../test.json                                                         |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

## <a name="process_authorizer"></a>4. Property `process_authorizer`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:../test.json                                                         |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

## <a name="safe_paths"></a>5. Property `safe_paths`

**Title:** Safe Paths

|              |                                                                |
| ------------ | -------------------------------------------------------------- |
| **Type**     | `array of string`                                              |
| **Required** | No                                                             |
| **Default**  | `["/system/health", "/docs", "/favicon.ico", "/openapi.json"]` |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | True               |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be       | Description |
| ------------------------------------- | ----------- |
| [safe_paths items](#safe_paths_items) | -           |

### <a name="autogenerated_heading_2"></a>5.1. safe_paths items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

----------------------------------------------------------------------------------------------------------------------------
