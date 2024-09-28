---
title: S3FileMemory
description: "Description of S3FileMemory component"
---
# S3FileMemory

- [1. [Optional] Property implementation](#implementation)
- [2. [Required] Property bucket](#bucket)
- [3. [Optional] Property region_name](#region_name)
- [4. [Optional] Property aws_access_key_id](#aws_access_key_id)
- [5. [Optional] Property aws_secret_access_key](#aws_secret_access_key)
- [6. [Optional] Property aws_session_token](#aws_session_token)
- [7. [Optional] Property session_args](#session_args)
- [8. [Optional] Property create_bucket_on_startup](#create_bucket_on_startup)

**Title:** S3FileMemory

|                           |                                                         |
| ------------------------- | ------------------------------------------------------- |
| **Type**                  | `object`                                                |
| **Required**              | No                                                      |
| **Additional properties** | [[Not allowed]](# "Additional Properties not allowed.") |

<details>
<summary>
<strong> <a name="implementation"></a>1. [Optional] Property implementation</strong>  

</summary>
<blockquote>

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

Specific value: `"S3FileMemory"`

</blockquote>
</details>

<details>
<summary>
<strong> <a name="bucket"></a>2. [Required] Property bucket</strong>  

</summary>
<blockquote>

**Title:** Bucket

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

</blockquote>
</details>

<details>
<summary>
<strong> <a name="region_name"></a>3. [Optional] Property region_name</strong>  

</summary>
<blockquote>

**Title:** Region Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

</blockquote>
</details>

<details>
<summary>
<strong> <a name="aws_access_key_id"></a>4. [Optional] Property aws_access_key_id</strong>  

</summary>
<blockquote>

**Title:** Aws Access Key Id

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

</blockquote>
</details>

<details>
<summary>
<strong> <a name="aws_secret_access_key"></a>5. [Optional] Property aws_secret_access_key</strong>  

</summary>
<blockquote>

**Title:** Aws Secret Access Key

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

</blockquote>
</details>

<details>
<summary>
<strong> <a name="aws_session_token"></a>6. [Optional] Property aws_session_token</strong>  

</summary>
<blockquote>

**Title:** Aws Session Token

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

</blockquote>
</details>

<details>
<summary>
<strong> <a name="session_args"></a>7. [Optional] Property session_args</strong>  

</summary>
<blockquote>

**Title:** Session Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

**Description:** Additional arguments to pass to the boto3 session.

</blockquote>
</details>

<details>
<summary>
<strong> <a name="create_bucket_on_startup"></a>8. [Optional] Property create_bucket_on_startup</strong>  

</summary>
<blockquote>

**Title:** Create Bucket On Startup

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `false`   |

</blockquote>
</details>

----------------------------------------------------------------------------------------------------------------------------
