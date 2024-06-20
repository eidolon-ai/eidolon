---
title: SecurityManagerImpl
description: Description of SecurityManagerImpl component
---

| Property                                                 | Pattern | Type            | Deprecated | Definition | Title/Description       |
| -------------------------------------------------------- | ------- | --------------- | ---------- | ---------- | ----------------------- |
| - [implementation](#implementation )                     | No      | const           | No         | -          | SecurityManagerImpl     |
| - [authentication_processor](#authentication_processor ) | No      | object          | No         | -          | AuthenticationProcessor |
| - [functional_authorizer](#functional_authorizer )       | No      | object          | No         | -          | FunctionalAuthorizer    |
| - [process_authorizer](#process_authorizer )             | No      | object          | No         | -          | ProcessAuthorizer       |
| - [safe_paths](#safe_paths )                             | No      | array of string | No         | -          | Safe Paths              |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** SecurityManagerImpl

Specific value: `"SecurityManagerImpl"`

## <a name="authentication_processor"></a>2. Property `authentication_processor`

**Title:** AuthenticationProcessor

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{"implementation": "NoopAuthProcessor"}`                                 |

**Description:** Overview of AuthenticationProcessor components

| Property                                                      | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#authentication_processor_implementation ) | No      | string | No         | -          | -                 |

### <a name="authentication_processor_implementation"></a>2.1. Property `implementation`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

## <a name="functional_authorizer"></a>3. Property `functional_authorizer`

**Title:** FunctionalAuthorizer

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{"implementation": "NoopFunctionalAuth"}`                                |

**Description:** Overview of FunctionalAuthorizer components

| Property                                                   | Pattern | Type   | Deprecated | Definition | Title/Description |
| ---------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#functional_authorizer_implementation ) | No      | string | No         | -          | -                 |

### <a name="functional_authorizer_implementation"></a>3.1. Property `implementation`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

## <a name="process_authorizer"></a>4. Property `process_authorizer`

**Title:** ProcessAuthorizer

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{"implementation": "PrivateAuthorizer"}`                                 |

**Description:** Overview of ProcessAuthorizer components

| Property                                                | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#process_authorizer_implementation ) | No      | string | No         | -          | -                 |

### <a name="process_authorizer_implementation"></a>4.1. Property `implementation`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

## <a name="safe_paths"></a>5. Property `safe_paths`

**Title:** Safe Paths

|              |                                                                |
| ------------ | -------------------------------------------------------------- |
| **Type**     | `array of string`                                              |
| **Required** | No                                                             |
| **Default**  | `["/openapi.json", "/favicon.ico", "/docs", "/system/health"]` |

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
