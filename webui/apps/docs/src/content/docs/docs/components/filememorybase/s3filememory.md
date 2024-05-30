---
title: S3FileMemory
description: Description of S3FileMemory component
---

| Property                                                 | Pattern | Type    | Deprecated | Definition | Title/Description        |
| -------------------------------------------------------- | ------- | ------- | ---------- | ---------- | ------------------------ |
| + [bucket](#bucket )                                     | No      | string  | No         | -          | Bucket                   |
| - [region](#region )                                     | No      | string  | No         | -          | Region                   |
| - [kwargs](#kwargs )                                     | No      | object  | No         | -          | Kwargs                   |
| - [create_bucket_on_startup](#create_bucket_on_startup ) | No      | boolean | No         | -          | Create Bucket On Startup |

## <a name="bucket"></a>1. Property `bucket`

**Title:** Bucket

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

## <a name="region"></a>2. Property `region`

**Title:** Region

|              |               |
| ------------ | ------------- |
| **Type**     | `string`      |
| **Required** | No            |
| **Default**  | `"us-east-1"` |

## <a name="kwargs"></a>3. Property `kwargs`

**Title:** Kwargs

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

## <a name="create_bucket_on_startup"></a>4. Property `create_bucket_on_startup`

**Title:** Create Bucket On Startup

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `false`   |

----------------------------------------------------------------------------------------------------------------------------
