---
title: ReferenceResource
description: "Description of ReferenceResource component"
---

| Property                             | Pattern | Type   | Deprecated | Definition          | Title/Description |
| ------------------------------------ | ------- | ------ | ---------- | ------------------- | ----------------- |
| + [implementation](#implementation ) | No      | const  | No         | -                   | ReferenceResource |
| + [apiVersion](#apiVersion )         | No      | string | No         | -                   | Apiversion        |
| - [kind](#kind )                     | No      | const  | No         | -                   | Kind              |
| + [metadata](#metadata )             | No      | object | No         | In #/$defs/Metadata | -                 |
| + [spec](#spec )                     | No      | object | No         | -                   | Spec              |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | Yes     |

**Description:** ReferenceResource

Specific value: `"ReferenceResource"`

## <a name="apiVersion"></a>2. Property `apiVersion`

**Title:** Apiversion

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

## <a name="kind"></a>3. Property `kind`

**Title:** Kind

|              |               |
| ------------ | ------------- |
| **Type**     | `const`       |
| **Required** | No            |
| **Default**  | `"Reference"` |

Must be one of:
* "Reference"
Specific value: `"Reference"`

## <a name="metadata"></a>4. Property `metadata`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | Yes                                                                       |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | #/$defs/Metadata                                                          |

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

**Title:** Spec

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | Yes                                                                       |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

----------------------------------------------------------------------------------------------------------------------------
