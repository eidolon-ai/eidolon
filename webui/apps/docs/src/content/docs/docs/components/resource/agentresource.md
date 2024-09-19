---
title: AgentResource
description: "Description of AgentResource component"
---

| Property                             | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------ | ------- | ------ | ---------- | ---------- | ----------------- |
| + [implementation](#implementation ) | No      | const  | No         | -          | AgentResource     |
| + [apiVersion](#apiVersion )         | No      | string | No         | -          | Apiversion        |
| - [kind](#kind )                     | No      | const  | No         | -          | Kind              |
| - [metadata](#metadata )             | No      | object | No         | In         | -                 |
| + [spec](#spec )                     | No      | object | No         | -          | object Reference  |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | Yes     |

**Description:** AgentResource

Specific value: `"AgentResource"`

## <a name="apiVersion"></a>2. Property `apiVersion`

**Title:** Apiversion

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

## <a name="kind"></a>3. Property `kind`

**Title:** Kind

|              |           |
| ------------ | --------- |
| **Type**     | `const`   |
| **Required** | No        |
| **Default**  | `"Agent"` |

Must be one of:
* "Agent"
Specific value: `"Agent"`

## <a name="metadata"></a>4. Property `metadata`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{"name": "DEFAULT"}`                                                     |
| **Defined in**            |                                                                           |

| Property                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [name](#metadata_name )             | No      | string | No         | -          | Name              |
| - [](#metadata_additionalProperties ) | No      | object | No         | -          | -                 |

### <a name="metadata_name"></a>4.1. Property `name`

**Title:** Name

|              |             |
| ------------ | ----------- |
| **Type**     | `string`    |
| **Required** | No          |
| **Default**  | `"DEFAULT"` |

## <a name="spec"></a>5. Property `spec`

**Title:** object Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | Yes                                                                       |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

| Property                                  | Pattern | Type   | Deprecated | Definition | Title/Description |
| ----------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#spec_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#spec_additionalProperties )         | No      | object | No         | -          | -                 |

### <a name="spec_implementation"></a>5.1. Property `implementation`

**Title:** Implementation

|              |           |
| ------------ | --------- |
| **Type**     | `string`  |
| **Required** | No        |
| **Default**  | `"Agent"` |

----------------------------------------------------------------------------------------------------------------------------
