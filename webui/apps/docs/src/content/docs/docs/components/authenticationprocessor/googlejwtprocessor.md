---
title: GoogleJWTProcessor
description: "Description of GoogleJWTProcessor component"
---
# GoogleJWTProcessor

- [1. [Optional] Property implementation](#implementation)
- [2. [Optional] Property jwks_url](#jwks_url)
- [3. [Optional] Property audience](#audience)
- [4. [Optional] Property issuer](#issuer)

**Title:** GoogleJWTProcessor

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

Specific value: `"GoogleJWTProcessor"`

</blockquote>
</details>

<details>
<summary>
<strong> <a name="jwks_url"></a>2. [Optional] Property jwks_url</strong>  

</summary>
<blockquote>

**Title:** Jwks Url

|              |                                                |
| ------------ | ---------------------------------------------- |
| **Type**     | `string`                                       |
| **Required** | No                                             |
| **Default**  | `"https://www.googleapis.com/oauth2/v3/certs"` |

**Description:** The URL to fetch the JWKS from. Defaults to https://www.googleapis.com/oauth2/v3/certs

</blockquote>
</details>

<details>
<summary>
<strong> <a name="audience"></a>3. [Optional] Property audience</strong>  

</summary>
<blockquote>

**Title:** Audience

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

**Description:** Your google client ID. Defaults to the environment variable GOOGLE_CLIENT_ID

</blockquote>
</details>

<details>
<summary>
<strong> <a name="issuer"></a>4. [Optional] Property issuer</strong>  

</summary>
<blockquote>

**Title:** Issuer

|              |                         |
| ------------ | ----------------------- |
| **Type**     | `string`                |
| **Required** | No                      |
| **Default**  | `"accounts.google.com"` |

**Description:** The issuer of the JWT. Defaults to accounts.google.com

</blockquote>
</details>

----------------------------------------------------------------------------------------------------------------------------
