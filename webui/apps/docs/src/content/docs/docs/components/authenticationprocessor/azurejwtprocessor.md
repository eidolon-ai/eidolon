---
title: AzureJWTProcessor
description: "Description of AzureJWTProcessor component"
---

| Property                             | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------ | ------- | ------ | ---------- | ---------- | ----------------- |
| + [implementation](#implementation ) | No      | const  | No         | -          | AzureJWTProcessor |
| - [client_id](#client_id )           | No      | string | No         | -          | Client Id         |
| - [tenant_id](#tenant_id )           | No      | string | No         | -          | Tenant Id         |
| - [issuer_prefix](#issuer_prefix )   | No      | string | No         | -          | Issuer Prefix     |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | Yes     |

**Description:** AzureJWTProcessor

Specific value: `"AzureJWTProcessor"`

## <a name="client_id"></a>2. Property `client_id`

**Title:** Client Id

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

**Description:** Your azure client or application ID. Defaults to the environment variable AZURE_CLIENT_ID

## <a name="tenant_id"></a>3. Property `tenant_id`

**Title:** Tenant Id

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

**Description:** The tenant id of the JWT. Defaults to the environment variable AZURE_TENANT_ID

## <a name="issuer_prefix"></a>4. Property `issuer_prefix`

**Title:** Issuer Prefix

|              |                             |
| ------------ | --------------------------- |
| **Type**     | `string`                    |
| **Required** | No                          |
| **Default**  | `"https://sts.windows.net"` |

**Description:** The issuer prefix of the JWT. Defaults to sts.windows.net.  The tenant id will be appended to this value.  For example, sts.windows.net/your_tenant_id

----------------------------------------------------------------------------------------------------------------------------
