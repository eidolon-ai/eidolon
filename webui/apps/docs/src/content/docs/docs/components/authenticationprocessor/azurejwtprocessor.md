---
title: AzureJWTProcessor
description: "Description of AzureJWTProcessor component"
---
# AzureJWTProcessor

- [1. [Optional] Property implementation](#implementation)
- [2. [Optional] Property client_id](#client_id)
- [3. [Optional] Property tenant_id](#tenant_id)
- [4. [Optional] Property issuer_prefix](#issuer_prefix)

**Title:** AzureJWTProcessor

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

Specific value: `"AzureJWTProcessor"`

</blockquote>
</details>

<details>
<summary>
<strong> <a name="client_id"></a>2. [Optional] Property client_id</strong>  

</summary>
<blockquote>

**Title:** Client Id

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

**Description:** Your azure client or application ID. Defaults to the environment variable AZURE_CLIENT_ID

</blockquote>
</details>

<details>
<summary>
<strong> <a name="tenant_id"></a>3. [Optional] Property tenant_id</strong>  

</summary>
<blockquote>

**Title:** Tenant Id

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

**Description:** The tenant id of the JWT. Defaults to the environment variable AZURE_TENANT_ID

</blockquote>
</details>

<details>
<summary>
<strong> <a name="issuer_prefix"></a>4. [Optional] Property issuer_prefix</strong>  

</summary>
<blockquote>

**Title:** Issuer Prefix

|              |                             |
| ------------ | --------------------------- |
| **Type**     | `string`                    |
| **Required** | No                          |
| **Default**  | `"https://sts.windows.net"` |

**Description:** The issuer prefix of the JWT. Defaults to sts.windows.net.  The tenant id will be appended to this value.  For example, sts.windows.net/your_tenant_id

</blockquote>
</details>

----------------------------------------------------------------------------------------------------------------------------
