---
title: S3Loader
description: Description of the S3Loader component
---

| Property                                           | Pattern | Type   | Deprecated | Definition | Title/Description     |
| -------------------------------------------------- | ------- | ------ | ---------- | ---------- | --------------------- |
| + [implementation](#implementation )               | No      | const  | No         | -          | Implementation        |
| + [bucket](#bucket )                               | No      | string | No         | -          | Bucket                |
| - [region_name](#region_name )                     | No      | string | No         | -          | Region Name           |
| - [aws_access_key_id](#aws_access_key_id )         | No      | string | No         | -          | Aws Access Key Id     |
| - [aws_secret_access_key](#aws_secret_access_key ) | No      | string | No         | -          | Aws Secret Access Key |
| - [aws_session_token](#aws_session_token )         | No      | string | No         | -          | Aws Session Token     |
| - [session_args](#session_args )                   | No      | object | No         | -          | Session Args          |
| - [pattern](#pattern )                             | No      | string | No         | -          | Pattern               |

## <a name="implementation"></a>1. Property `implementation`

**Title:** Implementation

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | Yes     |

Specific value: `"S3Loader"`

## <a name="bucket"></a>2. Property `bucket`

**Title:** Bucket

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

## <a name="region_name"></a>3. Property `region_name`

**Title:** Region Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

## <a name="aws_access_key_id"></a>4. Property `aws_access_key_id`

**Title:** Aws Access Key Id

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

## <a name="aws_secret_access_key"></a>5. Property `aws_secret_access_key`

**Title:** Aws Secret Access Key

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

## <a name="aws_session_token"></a>6. Property `aws_session_token`

**Title:** Aws Session Token

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

## <a name="session_args"></a>7. Property `session_args`

**Title:** Session Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

**Description:** Additional arguments to pass to the boto3 session.

## <a name="pattern"></a>8. Property `pattern`

**Title:** Pattern

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `"**"`   |

----------------------------------------------------------------------------------------------------------------------------
