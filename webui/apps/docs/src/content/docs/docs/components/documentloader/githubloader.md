---
title: GitHubLoader
description: Description of GitHubLoader component
---

**Description:** Loads files from a GitHub repository. Note that you will likely hit rate limits on all but the smallest repositories
unless a TOKEN is provided

| Property                       | Pattern | Type        | Deprecated | Definition | Title/Description |
| ------------------------------ | ------- | ----------- | ---------- | ---------- | ----------------- |
| + [owner](#owner )             | No      | string      | No         | -          | Owner             |
| + [repo](#repo )               | No      | string      | No         | -          | Repo              |
| - [client_args](#client_args ) | No      | object      | No         | -          | Client Args       |
| - [root_path](#root_path )     | No      | Combination | No         | -          | Root Path         |
| - [pattern](#pattern )         | No      | Combination | No         | -          | Pattern           |
| - [exclude](#exclude )         | No      | Combination | No         | -          | Exclude           |
| - [token](#token )             | No      | Combination | No         | -          | Token             |

## <a name="owner"></a>1. Property `owner`

**Title:** Owner

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

## <a name="repo"></a>2. Property `repo`

**Title:** Repo

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

## <a name="client_args"></a>3. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

## <a name="root_path"></a>4. Property `root_path`

**Title:** Root Path

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                |
| ----------------------------- |
| [item 0](#root_path_anyOf_i0) |
| [item 1](#root_path_anyOf_i1) |

### <a name="root_path_anyOf_i0"></a>4.1. Property `item 0`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

### <a name="root_path_anyOf_i1"></a>4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

## <a name="pattern"></a>5. Property `pattern`

**Title:** Pattern

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"**/*"`                                                                  |

| Any of(Option)              |
| --------------------------- |
| [item 0](#pattern_anyOf_i0) |
| [item 1](#pattern_anyOf_i1) |

### <a name="pattern_anyOf_i0"></a>5.1. Property `item 0`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

### <a name="pattern_anyOf_i1"></a>5.2. Property `item 1`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of string` |
| **Required** | No                |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be         | Description |
| --------------------------------------- | ----------- |
| [item 1 items](#pattern_anyOf_i1_items) | -           |

#### <a name="autogenerated_heading_2"></a>5.2.1. item 1 items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

## <a name="exclude"></a>6. Property `exclude`

**Title:** Exclude

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `[]`                                                                      |

| Any of(Option)              |
| --------------------------- |
| [item 0](#exclude_anyOf_i0) |
| [item 1](#exclude_anyOf_i1) |

### <a name="exclude_anyOf_i0"></a>6.1. Property `item 0`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

### <a name="exclude_anyOf_i1"></a>6.2. Property `item 1`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of string` |
| **Required** | No                |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be         | Description |
| --------------------------------------- | ----------- |
| [item 1 items](#exclude_anyOf_i1_items) | -           |

#### <a name="autogenerated_heading_3"></a>6.2.1. item 1 items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

## <a name="token"></a>7. Property `token`

**Title:** Token

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

**Description:** Github token, can also be set via envar 'GITHUB_TOKEN'

| Any of(Option)            |
| ------------------------- |
| [item 0](#token_anyOf_i0) |
| [item 1](#token_anyOf_i1) |

### <a name="token_anyOf_i0"></a>7.1. Property `item 0`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

### <a name="token_anyOf_i1"></a>7.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

----------------------------------------------------------------------------------------------------------------------------
