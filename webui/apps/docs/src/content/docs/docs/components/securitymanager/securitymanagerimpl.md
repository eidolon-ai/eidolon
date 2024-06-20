---
title: SecurityManagerImpl
description: Description of SecurityManagerImpl component
---

| Property                                                 | Pattern | Type            | Deprecated | Definition                                       | Title/Description                              |
| -------------------------------------------------------- | ------- | --------------- | ---------- | ------------------------------------------------ | ---------------------------------------------- |
| - [implementation](#implementation )                     | No      | const           | No         | -                                                | SecurityManagerImpl                            |
| - [authentication_processor](#authentication_processor ) | No      | object          | No         | In [AuthenticationProcessor](/docs/components/authenticationprocessor/overview) | Overview of AuthenticationProcessor components |
| - [functional_authorizer](#functional_authorizer )       | No      | object          | No         | In [FunctionalAuthorizer](/docs/components/functionalauthorizer/overview)    | Overview of FunctionalAuthorizer components    |
| - [process_authorizer](#process_authorizer )             | No      | object          | No         | In [ProcessAuthorizer](/docs/components/processauthorizer/overview)       | Overview of ProcessAuthorizer components       |
| - [safe_paths](#safe_paths )                             | No      | array of string | No         | -                                                | Safe Paths                                     |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** SecurityManagerImpl

Specific value: `"SecurityManagerImpl"`

## <a name="authentication_processor"></a>2. Property `authentication_processor`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{"implementation": "NoopAuthProcessor"}`                                 |
| **Defined in**            | [AuthenticationProcessor](/docs/components/authenticationprocessor/overview)                             |

**Description:** Overview of AuthenticationProcessor components

| Any of(Option)                                                |
| ------------------------------------------------------------- |
| [AzureJWTProcessor.json](#authentication_processor_anyOf_i0)  |
| [GoogleJWTProcessor.json](#authentication_processor_anyOf_i1) |
| [NoopAuthProcessor.json](#authentication_processor_anyOf_i2)  |

### <a name="authentication_processor_anyOf_i0"></a>2.1. Property `AzureJWTProcessor.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./AzureJWTProcessor.json                                             |

| Property                                                               | Pattern | Type   | Deprecated | Definition | Title/Description |
| ---------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#authentication_processor_anyOf_i0_implementation ) | No      | const  | No         | -          | AzureJWTProcessor |
| - [client_id](#authentication_processor_anyOf_i0_client_id )           | No      | string | No         | -          | Client Id         |
| - [tenant_id](#authentication_processor_anyOf_i0_tenant_id )           | No      | string | No         | -          | Tenant Id         |
| - [issuer_prefix](#authentication_processor_anyOf_i0_issuer_prefix )   | No      | string | No         | -          | Issuer Prefix     |

#### <a name="authentication_processor_anyOf_i0_implementation"></a>2.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AzureJWTProcessor

Specific value: `"AzureJWTProcessor"`

#### <a name="authentication_processor_anyOf_i0_client_id"></a>2.1.2. Property `client_id`

**Title:** Client Id

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

**Description:** Your azure client or application ID. Defaults to the environment variable AZURE_CLIENT_ID

#### <a name="authentication_processor_anyOf_i0_tenant_id"></a>2.1.3. Property `tenant_id`

**Title:** Tenant Id

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

**Description:** The tenant id of the JWT. Defaults to the environment variable AZURE_TENANT_ID

#### <a name="authentication_processor_anyOf_i0_issuer_prefix"></a>2.1.4. Property `issuer_prefix`

**Title:** Issuer Prefix

|              |                             |
| ------------ | --------------------------- |
| **Type**     | `string`                    |
| **Required** | No                          |
| **Default**  | `"https://sts.windows.net"` |

**Description:** The issuer prefix of the JWT. Defaults to sts.windows.net.  The tenant id will be appended to this value.  For example, sts.windows.net/your_tenant_id

### <a name="authentication_processor_anyOf_i1"></a>2.2. Property `GoogleJWTProcessor.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./GoogleJWTProcessor.json                                            |

| Property                                                               | Pattern | Type   | Deprecated | Definition | Title/Description  |
| ---------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ------------------ |
| - [implementation](#authentication_processor_anyOf_i1_implementation ) | No      | const  | No         | -          | GoogleJWTProcessor |
| - [jwks_url](#authentication_processor_anyOf_i1_jwks_url )             | No      | string | No         | -          | Jwks Url           |
| - [audience](#authentication_processor_anyOf_i1_audience )             | No      | string | No         | -          | Audience           |
| - [issuer](#authentication_processor_anyOf_i1_issuer )                 | No      | string | No         | -          | Issuer             |

#### <a name="authentication_processor_anyOf_i1_implementation"></a>2.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** GoogleJWTProcessor

Specific value: `"GoogleJWTProcessor"`

#### <a name="authentication_processor_anyOf_i1_jwks_url"></a>2.2.2. Property `jwks_url`

**Title:** Jwks Url

|              |                                                |
| ------------ | ---------------------------------------------- |
| **Type**     | `string`                                       |
| **Required** | No                                             |
| **Default**  | `"https://www.googleapis.com/oauth2/v3/certs"` |

**Description:** The URL to fetch the JWKS from. Defaults to https://www.googleapis.com/oauth2/v3/certs

#### <a name="authentication_processor_anyOf_i1_audience"></a>2.2.3. Property `audience`

**Title:** Audience

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

**Description:** Your google client ID. Defaults to the environment variable GOOGLE_CLIENT_ID

#### <a name="authentication_processor_anyOf_i1_issuer"></a>2.2.4. Property `issuer`

**Title:** Issuer

|              |                         |
| ------------ | ----------------------- |
| **Type**     | `string`                |
| **Required** | No                      |
| **Default**  | `"accounts.google.com"` |

**Description:** The issuer of the JWT. Defaults to accounts.google.com

### <a name="authentication_processor_anyOf_i2"></a>2.3. Property `NoopAuthProcessor.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./NoopAuthProcessor.json                                             |

| Property                                                               | Pattern | Type  | Deprecated | Definition | Title/Description |
| ---------------------------------------------------------------------- | ------- | ----- | ---------- | ---------- | ----------------- |
| - [implementation](#authentication_processor_anyOf_i2_implementation ) | No      | const | No         | -          | NoopAuthProcessor |

#### <a name="authentication_processor_anyOf_i2_implementation"></a>2.3.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** NoopAuthProcessor

Specific value: `"NoopAuthProcessor"`

## <a name="functional_authorizer"></a>3. Property `functional_authorizer`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{"implementation": "NoopFunctionalAuth"}`                                |
| **Defined in**            | [FunctionalAuthorizer](/docs/components/functionalauthorizer/overview)                                |

**Description:** Overview of FunctionalAuthorizer components

| Any of(Option)                                                          |
| ----------------------------------------------------------------------- |
| [GlobPatternFunctionalAuthorizer.json](#functional_authorizer_anyOf_i0) |
| [NoopFunctionalAuth.json](#functional_authorizer_anyOf_i1)              |

### <a name="functional_authorizer_anyOf_i0"></a>3.1. Property `GlobPatternFunctionalAuthorizer.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./GlobPatternFunctionalAuthorizer.json                               |

| Property                                                            | Pattern | Type  | Deprecated | Definition | Title/Description               |
| ------------------------------------------------------------------- | ------- | ----- | ---------- | ---------- | ------------------------------- |
| - [implementation](#functional_authorizer_anyOf_i0_implementation ) | No      | const | No         | -          | GlobPatternFunctionalAuthorizer |

#### <a name="functional_authorizer_anyOf_i0_implementation"></a>3.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** GlobPatternFunctionalAuthorizer

Specific value: `"GlobPatternFunctionalAuthorizer"`

### <a name="functional_authorizer_anyOf_i1"></a>3.2. Property `NoopFunctionalAuth.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./NoopFunctionalAuth.json                                            |

| Property                                                            | Pattern | Type  | Deprecated | Definition | Title/Description  |
| ------------------------------------------------------------------- | ------- | ----- | ---------- | ---------- | ------------------ |
| - [implementation](#functional_authorizer_anyOf_i1_implementation ) | No      | const | No         | -          | NoopFunctionalAuth |

#### <a name="functional_authorizer_anyOf_i1_implementation"></a>3.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** NoopFunctionalAuth

Specific value: `"NoopFunctionalAuth"`

## <a name="process_authorizer"></a>4. Property `process_authorizer`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{"implementation": "PrivateAuthorizer"}`                                 |
| **Defined in**            | [ProcessAuthorizer](/docs/components/processauthorizer/overview)                                   |

**Description:** Overview of ProcessAuthorizer components

| Any of(Option)                                         |
| ------------------------------------------------------ |
| [PrivateAuthorizer.json](#process_authorizer_anyOf_i0) |

### <a name="process_authorizer_anyOf_i0"></a>4.1. Property `PrivateAuthorizer.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./PrivateAuthorizer.json                                             |

| Property                                                         | Pattern | Type  | Deprecated | Definition | Title/Description |
| ---------------------------------------------------------------- | ------- | ----- | ---------- | ---------- | ----------------- |
| - [implementation](#process_authorizer_anyOf_i0_implementation ) | No      | const | No         | -          | PrivateAuthorizer |

#### <a name="process_authorizer_anyOf_i0_implementation"></a>4.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** PrivateAuthorizer

Specific value: `"PrivateAuthorizer"`

## <a name="safe_paths"></a>5. Property `safe_paths`

**Title:** Safe Paths

|              |                                                                |
| ------------ | -------------------------------------------------------------- |
| **Type**     | `array of string`                                              |
| **Required** | No                                                             |
| **Default**  | `["/system/health", "/openapi.json", "/docs", "/favicon.ico"]` |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | True               |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be       | Description |
| ------------------------------------- | ----------- |
| [safe_paths items](#safe_paths_items) | -           |

### <a name="autogenerated_heading_2"></a>5.1. safe_paths items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

----------------------------------------------------------------------------------------------------------------------------
