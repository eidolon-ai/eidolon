---
title: GoogleJWTProcessor
description: "Description of GoogleJWTProcessor component"
---
# Schema Docs

- [1. Property `implementation`](#implementation)
- [2. Property `jwks_url`](#jwks_url)
- [3. Property `audience`](#audience)
- [4. Property `issuer`](#issuer)

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

| Property                             | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------ | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#implementation ) | No      | const  | No         | -          | -                 |
| - [jwks_url](#jwks_url )             | No      | string | No         | -          | Jwks Url          |
| - [audience](#audience )             | No      | string | No         | -          | Audience          |
| - [issuer](#issuer )                 | No      | string | No         | -          | Issuer            |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

Specific value: `"GoogleJWTProcessor"`

## <a name="jwks_url"></a>2. Property `jwks_url`

**Title:** Jwks Url

|              |                                                |
| ------------ | ---------------------------------------------- |
| **Type**     | `string`                                       |
| **Required** | No                                             |
| **Default**  | `"https://www.googleapis.com/oauth2/v3/certs"` |

**Description:** The URL to fetch the JWKS from. Defaults to https://www.googleapis.com/oauth2/v3/certs

## <a name="audience"></a>3. Property `audience`

**Title:** Audience

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

**Description:** Your google client ID. Defaults to the environment variable GOOGLE_CLIENT_ID

## <a name="issuer"></a>4. Property `issuer`

**Title:** Issuer

|              |                         |
| ------------ | ----------------------- |
| **Type**     | `string`                |
| **Required** | No                      |
| **Default**  | `"accounts.google.com"` |

**Description:** The issuer of the JWT. Defaults to accounts.google.com

----------------------------------------------------------------------------------------------------------------------------
