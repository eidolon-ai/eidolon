---
title: S3Loader
description: Description of S3Loader component
---

**Description:** Loads documents from an S3 bucket.

| Property                                           | Pattern | Type        | Deprecated | Definition | Title/Description     |
| -------------------------------------------------- | ------- | ----------- | ---------- | ---------- | --------------------- |
| + [bucket](#bucket )                               | No      | string      | No         | -          | Bucket                |
| - [region_name](#region_name )                     | No      | Combination | No         | -          | Region Name           |
| - [aws_access_key_id](#aws_access_key_id )         | No      | Combination | No         | -          | Aws Access Key Id     |
| - [aws_secret_access_key](#aws_secret_access_key ) | No      | Combination | No         | -          | Aws Secret Access Key |
| - [aws_session_token](#aws_session_token )         | No      | Combination | No         | -          | Aws Session Token     |
| - [session_args](#session_args )                   | No      | object      | No         | -          | Session Args          |
| - [pattern](#pattern )                             | No      | string      | No         | -          | Pattern               |

## <a name="bucket"></a>1. Property `bucket`

**Title:** Bucket

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

## <a name="region_name"></a>2. Property `region_name`

**Title:** Region Name

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                  |
| ------------------------------- |
| [item 0](#region_name_anyOf_i0) |
| [item 1](#region_name_anyOf_i1) |

### <a name="region_name_anyOf_i0"></a>2.1. Property `item 0`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

### <a name="region_name_anyOf_i1"></a>2.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

## <a name="aws_access_key_id"></a>3. Property `aws_access_key_id`

**Title:** Aws Access Key Id

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                        |
| ------------------------------------- |
| [item 0](#aws_access_key_id_anyOf_i0) |
| [item 1](#aws_access_key_id_anyOf_i1) |

### <a name="aws_access_key_id_anyOf_i0"></a>3.1. Property `item 0`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

### <a name="aws_access_key_id_anyOf_i1"></a>3.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

## <a name="aws_secret_access_key"></a>4. Property `aws_secret_access_key`

**Title:** Aws Secret Access Key

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                            |
| ----------------------------------------- |
| [item 0](#aws_secret_access_key_anyOf_i0) |
| [item 1](#aws_secret_access_key_anyOf_i1) |

### <a name="aws_secret_access_key_anyOf_i0"></a>4.1. Property `item 0`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

### <a name="aws_secret_access_key_anyOf_i1"></a>4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

## <a name="aws_session_token"></a>5. Property `aws_session_token`

**Title:** Aws Session Token

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                        |
| ------------------------------------- |
| [item 0](#aws_session_token_anyOf_i0) |
| [item 1](#aws_session_token_anyOf_i1) |

### <a name="aws_session_token_anyOf_i0"></a>5.1. Property `item 0`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

### <a name="aws_session_token_anyOf_i1"></a>5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

## <a name="session_args"></a>6. Property `session_args`

**Title:** Session Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

**Description:** Additional arguments to pass to the boto3 session.

## <a name="pattern"></a>7. Property `pattern`

**Title:** Pattern

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `"**"`   |

----------------------------------------------------------------------------------------------------------------------------
