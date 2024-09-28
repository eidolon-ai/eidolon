---
title: AzureLoader
description: "Description of AzureLoader component"
---
# AzureLoader

- [1. [Optional] Property implementation](#implementation)
- [2. [Optional] Property azure_ad_token_provider](#azure_ad_token_provider)
  - [2.1. [Optional] Property implementation](#azure_ad_token_provider_implementation)
- [3. [Required] Property account_url](#account_url)
- [4. [Required] Property container](#container)
- [5. [Optional] Property create_container_on_startup](#create_container_on_startup)
- [6. [Optional] Property pattern](#pattern)

**Title:** AzureLoader

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

Specific value: `"AzureLoader"`

</blockquote>
</details>

<details>
<summary>
<strong> <a name="azure_ad_token_provider"></a>2. [Optional] Property azure_ad_token_provider</strong>  

</summary>
<blockquote>

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | #/$defs/Reference                                                         |

<details>
<summary>
<strong> <a name="azure_ad_token_provider_implementation"></a>2.1. [Optional] Property implementation</strong>  

</summary>
<blockquote>

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

</blockquote>
</details>

</blockquote>
</details>

<details>
<summary>
<strong> <a name="account_url"></a>3. [Required] Property account_url</strong>  

</summary>
<blockquote>

**Title:** Account Url

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** The URL of the Azure storage account of the form https://<OAUTH_STORAGE_ACCOUNT_NAME>.blob.core.windows.net.

</blockquote>
</details>

<details>
<summary>
<strong> <a name="container"></a>4. [Required] Property container</strong>  

</summary>
<blockquote>

**Title:** Container

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** The name of the container to use.

</blockquote>
</details>

<details>
<summary>
<strong> <a name="create_container_on_startup"></a>5. [Optional] Property create_container_on_startup</strong>  

</summary>
<blockquote>

**Title:** Create Container On Startup

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `false`   |

**Description:** If true, the container will be created on startup if not already present.

</blockquote>
</details>

<details>
<summary>
<strong> <a name="pattern"></a>6. [Optional] Property pattern</strong>  

</summary>
<blockquote>

**Title:** Pattern

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `"**"`   |

</blockquote>
</details>

----------------------------------------------------------------------------------------------------------------------------
