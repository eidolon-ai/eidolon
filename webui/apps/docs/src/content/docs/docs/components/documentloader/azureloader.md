---
title: AzureLoader
description: Description of the AzureLoader component
---

**Description:** Loads documents from an azure storage container.

| Property                                                       | Pattern | Type    | Deprecated | Definition            | Title/Description           |
| -------------------------------------------------------------- | ------- | ------- | ---------- | --------------------- | --------------------------- |
| + [implementation](#implementation )                           | No      | const   | No         | -                     | Implementation              |
| - [azure_ad_token_provider](#azure_ad_token_provider )         | No      | object  | No         | In #/$defs/_Reference | -                           |
| + [account_url](#account_url )                                 | No      | string  | No         | -                     | Account Url                 |
| + [container](#container )                                     | No      | string  | No         | -                     | Container                   |
| - [create_container_on_startup](#create_container_on_startup ) | No      | boolean | No         | -                     | Create Container On Startup |
| - [pattern](#pattern )                                         | No      | string  | No         | -                     | Pattern                     |

## <a name="implementation"></a>1. Property `implementation`

**Title:** Implementation

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | Yes     |

Specific value: `"AzureLoader"`

## <a name="azure_ad_token_provider"></a>2. Property `azure_ad_token_provider`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | #/$defs/_Reference                                                        |

| Property                                                     | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------ | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#azure_ad_token_provider_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#azure_ad_token_provider_additionalProperties )         | No      | object | No         | -          | -                 |

### <a name="azure_ad_token_provider_implementation"></a>2.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

## <a name="account_url"></a>3. Property `account_url`

**Title:** Account Url

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** The URL of the Azure storage account of the form https://<OAUTH_STORAGE_ACCOUNT_NAME>.blob.core.windows.net.

## <a name="container"></a>4. Property `container`

**Title:** Container

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** The name of the container to use.

## <a name="create_container_on_startup"></a>5. Property `create_container_on_startup`

**Title:** Create Container On Startup

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `false`   |

**Description:** If true, the container will be created on startup if not already present.

## <a name="pattern"></a>6. Property `pattern`

**Title:** Pattern

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `"**"`   |

----------------------------------------------------------------------------------------------------------------------------
