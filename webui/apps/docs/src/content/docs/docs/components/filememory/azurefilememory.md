---
title: AzureFileMemory
description: Description of AzureFileMemory component
---

| Property                                                       | Pattern | Type        | Deprecated | Definition | Title/Description           |
| -------------------------------------------------------------- | ------- | ----------- | ---------- | ---------- | --------------------------- |
| - [implementation](#implementation )                           | No      | const       | No         | -          | AzureFileMemory             |
| - [azure_ad_token_provider](#azure_ad_token_provider )         | No      | Combination | No         | -          | -                           |
| + [account_url](#account_url )                                 | No      | string      | No         | -          | Account Url                 |
| + [container](#container )                                     | No      | string      | No         | -          | Container                   |
| - [create_container_on_startup](#create_container_on_startup ) | No      | boolean     | No         | -          | Create Container On Startup |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** AzureFileMemory

Specific value: `"AzureFileMemory"`

## <a name="azure_ad_token_provider"></a>2. Property `azure_ad_token_provider`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

| Any of(Option)                                 |
| ---------------------------------------------- |
| [Reference](#azure_ad_token_provider_anyOf_i0) |
| [item 1](#azure_ad_token_provider_anyOf_i1)    |

### <a name="azure_ad_token_provider_anyOf_i0"></a>2.1. Property `Reference`

**Title:** Reference

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

**Description:** Used to create references to other classes. t is designed to be used with two type variables, `B` and `D` which are
the type bound and default type respectively. Neither are required, and if only one type is provided it is assumed
to be the bound. Bound is used as the default if no default is provided. default can also be a string which will be
looked up from the OS ReferenceResources.

Examples:
    Reference(implementation=fqn(Foo)                           # Returns an instance of Foo
    Reference[FooBase](implementation=fqn(Foo)).instantiate()   # Returns an instance of Foo
    Reference[FooBase](implementation=fqn(Bar))                 # Raises ValueError
    Reference[FooBase, Foo]().instantiate()                     # Returns an instance of Foo
    Reference[FooBase]().instantiate()                          # Returns an instance of FooBase

Attributes:
    _bound: This is a type variable `B` that represents the bound type of the reference. It defaults to `object`.
    _default: This is a type variable `D` that represents the default type of the reference. It defaults to `None`.
    implementation: This is a string that represents the fully qualified name of the class that the reference points to. It is optional and can be set to `None`.
    **extra: This is a dictionary that can hold any additional specifications for the reference. It is optional and can be set to `None`.

Methods:
    instantiate: This method is used to create an instance of the class that the reference points to.

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#azure_ad_token_provider_anyOf_i0_implementation ) | No      | string | No         | -          | Implementation    |
| - [](#azure_ad_token_provider_anyOf_i0_additionalProperties )         | No      | object | No         | -          | -                 |

#### <a name="azure_ad_token_provider_anyOf_i0_implementation"></a>2.1.1. Property `implementation`

**Title:** Implementation

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `null`   |

### <a name="azure_ad_token_provider_anyOf_i1"></a>2.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

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

----------------------------------------------------------------------------------------------------------------------------
