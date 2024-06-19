---
title: DocumentManager
description: Description of DocumentManager component
---

**Description:** Manages a collection of documents and provides search functionality. Automatically embeds and syncs documents (
provided by loader) into similarity memory where they can be searched.

| Property                                   | Pattern | Type    | Deprecated | Definition                                 | Title/Description                        |
| ------------------------------------------ | ------- | ------- | ---------- | ------------------------------------------ | ---------------------------------------- |
| - [implementation](#implementation )       | No      | const   | No         | -                                          | DocumentManager                          |
| + [name](#name )                           | No      | string  | No         | -                                          | Name                                     |
| - [recheck_frequency](#recheck_frequency ) | No      | integer | No         | -                                          | Recheck Frequency                        |
| - [loader](#loader )                       | No      | object  | No         | In [DocumentLoader](/docs/components/documentloader/overview)    | Overview of DocumentLoader components    |
| - [doc_processor](#doc_processor )         | No      | object  | No         | In [DocumentProcessor](/docs/components/documentprocessor/overview) | Overview of DocumentProcessor components |
| - [concurrency](#concurrency )             | No      | integer | No         | -                                          | Concurrency                              |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** DocumentManager

Specific value: `"DocumentManager"`

## <a name="name"></a>2. Property `name`

**Title:** Name

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** The name of the document manager (used to name database collections).

## <a name="recheck_frequency"></a>3. Property `recheck_frequency`

**Title:** Recheck Frequency

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `60`      |

**Description:** The number of seconds between checks.

## <a name="loader"></a>4. Property `loader`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"FilesystemLoader"`                                                      |
| **Defined in**            | [DocumentLoader](/docs/components/documentloader/overview)                                      |

**Description:** Overview of DocumentLoader components

| One of(Option)                            |
| ----------------------------------------- |
| [FilesystemLoader.json](#loader_oneOf_i0) |
| [GitHubLoader.json](#loader_oneOf_i1)     |
| [S3Loader.json](#loader_oneOf_i2)         |

### <a name="loader_oneOf_i0"></a>4.1. Property `FilesystemLoader.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./FilesystemLoader.json                                              |

| Property                                             | Pattern | Type   | Deprecated | Definition | Title/Description |
| ---------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#loader_oneOf_i0_implementation ) | No      | const  | No         | -          | FilesystemLoader  |
| + [root_dir](#loader_oneOf_i0_root_dir )             | No      | string | No         | -          | Root Dir          |
| - [pattern](#loader_oneOf_i0_pattern )               | No      | string | No         | -          | Pattern           |

#### <a name="loader_oneOf_i0_implementation"></a>4.1.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** FilesystemLoader

Specific value: `"FilesystemLoader"`

#### <a name="loader_oneOf_i0_root_dir"></a>4.1.2. Property `root_dir`

**Title:** Root Dir

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

#### <a name="loader_oneOf_i0_pattern"></a>4.1.3. Property `pattern`

**Title:** Pattern

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `"**/*"` |

### <a name="loader_oneOf_i1"></a>4.2. Property `GitHubLoader.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./GitHubLoader.json                                                  |

**Description:** Loads files from a GitHub repository. Note that you will likely hit rate limits on all but the smallest repositories
unless a TOKEN is provided

| Property                                             | Pattern | Type        | Deprecated | Definition | Title/Description |
| ---------------------------------------------------- | ------- | ----------- | ---------- | ---------- | ----------------- |
| - [implementation](#loader_oneOf_i1_implementation ) | No      | const       | No         | -          | GitHubLoader      |
| + [owner](#loader_oneOf_i1_owner )                   | No      | string      | No         | -          | Owner             |
| + [repo](#loader_oneOf_i1_repo )                     | No      | string      | No         | -          | Repo              |
| - [client_args](#loader_oneOf_i1_client_args )       | No      | object      | No         | -          | Client Args       |
| - [root_path](#loader_oneOf_i1_root_path )           | No      | Combination | No         | -          | Root Path         |
| - [pattern](#loader_oneOf_i1_pattern )               | No      | Combination | No         | -          | Pattern           |
| - [exclude](#loader_oneOf_i1_exclude )               | No      | Combination | No         | -          | Exclude           |
| - [token](#loader_oneOf_i1_token )                   | No      | Combination | No         | -          | Token             |

#### <a name="loader_oneOf_i1_implementation"></a>4.2.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** GitHubLoader

Specific value: `"GitHubLoader"`

#### <a name="loader_oneOf_i1_owner"></a>4.2.2. Property `owner`

**Title:** Owner

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

#### <a name="loader_oneOf_i1_repo"></a>4.2.3. Property `repo`

**Title:** Repo

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

#### <a name="loader_oneOf_i1_client_args"></a>4.2.4. Property `client_args`

**Title:** Client Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

#### <a name="loader_oneOf_i1_root_path"></a>4.2.5. Property `root_path`

**Title:** Root Path

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                |
| --------------------------------------------- |
| [item 0](#loader_oneOf_i1_root_path_anyOf_i0) |
| [item 1](#loader_oneOf_i1_root_path_anyOf_i1) |

##### <a name="loader_oneOf_i1_root_path_anyOf_i0"></a>4.2.5.1. Property `item 0`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

##### <a name="loader_oneOf_i1_root_path_anyOf_i1"></a>4.2.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="loader_oneOf_i1_pattern"></a>4.2.6. Property `pattern`

**Title:** Pattern

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"**"`                                                                    |

| Any of(Option)                              |
| ------------------------------------------- |
| [item 0](#loader_oneOf_i1_pattern_anyOf_i0) |
| [item 1](#loader_oneOf_i1_pattern_anyOf_i1) |

##### <a name="loader_oneOf_i1_pattern_anyOf_i0"></a>4.2.6.1. Property `item 0`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

##### <a name="loader_oneOf_i1_pattern_anyOf_i1"></a>4.2.6.2. Property `item 1`

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

| Each item of this array must be                         | Description |
| ------------------------------------------------------- | ----------- |
| [item 1 items](#loader_oneOf_i1_pattern_anyOf_i1_items) | -           |

###### <a name="autogenerated_heading_2"></a>4.2.6.2.1. item 1 items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

#### <a name="loader_oneOf_i1_exclude"></a>4.2.7. Property `exclude`

**Title:** Exclude

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `[]`                                                                      |

| Any of(Option)                              |
| ------------------------------------------- |
| [item 0](#loader_oneOf_i1_exclude_anyOf_i0) |
| [item 1](#loader_oneOf_i1_exclude_anyOf_i1) |

##### <a name="loader_oneOf_i1_exclude_anyOf_i0"></a>4.2.7.1. Property `item 0`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

##### <a name="loader_oneOf_i1_exclude_anyOf_i1"></a>4.2.7.2. Property `item 1`

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

| Each item of this array must be                         | Description |
| ------------------------------------------------------- | ----------- |
| [item 1 items](#loader_oneOf_i1_exclude_anyOf_i1_items) | -           |

###### <a name="autogenerated_heading_3"></a>4.2.7.2.1. item 1 items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

#### <a name="loader_oneOf_i1_token"></a>4.2.8. Property `token`

**Title:** Token

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

**Description:** Github token, can also be set via envar 'GITHUB_TOKEN'

| Any of(Option)                            |
| ----------------------------------------- |
| [item 0](#loader_oneOf_i1_token_anyOf_i0) |
| [item 1](#loader_oneOf_i1_token_anyOf_i1) |

##### <a name="loader_oneOf_i1_token_anyOf_i0"></a>4.2.8.1. Property `item 0`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

##### <a name="loader_oneOf_i1_token_anyOf_i1"></a>4.2.8.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

### <a name="loader_oneOf_i2"></a>4.3. Property `S3Loader.json`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | file:./S3Loader.json                                                      |

**Description:** Loads documents from an S3 bucket.

| Property                                                           | Pattern | Type        | Deprecated | Definition | Title/Description     |
| ------------------------------------------------------------------ | ------- | ----------- | ---------- | ---------- | --------------------- |
| - [implementation](#loader_oneOf_i2_implementation )               | No      | const       | No         | -          | S3Loader              |
| + [bucket](#loader_oneOf_i2_bucket )                               | No      | string      | No         | -          | Bucket                |
| - [region_name](#loader_oneOf_i2_region_name )                     | No      | Combination | No         | -          | Region Name           |
| - [aws_access_key_id](#loader_oneOf_i2_aws_access_key_id )         | No      | Combination | No         | -          | Aws Access Key Id     |
| - [aws_secret_access_key](#loader_oneOf_i2_aws_secret_access_key ) | No      | Combination | No         | -          | Aws Secret Access Key |
| - [aws_session_token](#loader_oneOf_i2_aws_session_token )         | No      | Combination | No         | -          | Aws Session Token     |
| - [session_args](#loader_oneOf_i2_session_args )                   | No      | object      | No         | -          | Session Args          |
| - [pattern](#loader_oneOf_i2_pattern )                             | No      | string      | No         | -          | Pattern               |

#### <a name="loader_oneOf_i2_implementation"></a>4.3.1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** S3Loader

Specific value: `"S3Loader"`

#### <a name="loader_oneOf_i2_bucket"></a>4.3.2. Property `bucket`

**Title:** Bucket

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

#### <a name="loader_oneOf_i2_region_name"></a>4.3.3. Property `region_name`

**Title:** Region Name

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                  |
| ----------------------------------------------- |
| [item 0](#loader_oneOf_i2_region_name_anyOf_i0) |
| [item 1](#loader_oneOf_i2_region_name_anyOf_i1) |

##### <a name="loader_oneOf_i2_region_name_anyOf_i0"></a>4.3.3.1. Property `item 0`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

##### <a name="loader_oneOf_i2_region_name_anyOf_i1"></a>4.3.3.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="loader_oneOf_i2_aws_access_key_id"></a>4.3.4. Property `aws_access_key_id`

**Title:** Aws Access Key Id

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                        |
| ----------------------------------------------------- |
| [item 0](#loader_oneOf_i2_aws_access_key_id_anyOf_i0) |
| [item 1](#loader_oneOf_i2_aws_access_key_id_anyOf_i1) |

##### <a name="loader_oneOf_i2_aws_access_key_id_anyOf_i0"></a>4.3.4.1. Property `item 0`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

##### <a name="loader_oneOf_i2_aws_access_key_id_anyOf_i1"></a>4.3.4.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="loader_oneOf_i2_aws_secret_access_key"></a>4.3.5. Property `aws_secret_access_key`

**Title:** Aws Secret Access Key

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                            |
| --------------------------------------------------------- |
| [item 0](#loader_oneOf_i2_aws_secret_access_key_anyOf_i0) |
| [item 1](#loader_oneOf_i2_aws_secret_access_key_anyOf_i1) |

##### <a name="loader_oneOf_i2_aws_secret_access_key_anyOf_i0"></a>4.3.5.1. Property `item 0`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

##### <a name="loader_oneOf_i2_aws_secret_access_key_anyOf_i1"></a>4.3.5.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="loader_oneOf_i2_aws_session_token"></a>4.3.6. Property `aws_session_token`

**Title:** Aws Session Token

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `null`                                                                    |

| Any of(Option)                                        |
| ----------------------------------------------------- |
| [item 0](#loader_oneOf_i2_aws_session_token_anyOf_i0) |
| [item 1](#loader_oneOf_i2_aws_session_token_anyOf_i1) |

##### <a name="loader_oneOf_i2_aws_session_token_anyOf_i0"></a>4.3.6.1. Property `item 0`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

##### <a name="loader_oneOf_i2_aws_session_token_anyOf_i1"></a>4.3.6.2. Property `item 1`

|              |        |
| ------------ | ------ |
| **Type**     | `null` |
| **Required** | No     |

#### <a name="loader_oneOf_i2_session_args"></a>4.3.7. Property `session_args`

**Title:** Session Args

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `{}`                                                                      |

**Description:** Additional arguments to pass to the boto3 session.

#### <a name="loader_oneOf_i2_pattern"></a>4.3.8. Property `pattern`

**Title:** Pattern

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |
| **Default**  | `"**"`   |

## <a name="doc_processor"></a>5. Property `doc_processor`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `combining`                                                               |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Default**               | `"DocumentProcessor"`                                                     |
| **Defined in**            | [DocumentProcessor](/docs/components/documentprocessor/overview)                                   |

**Description:** Overview of DocumentProcessor components

## <a name="concurrency"></a>6. Property `concurrency`

**Title:** Concurrency

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |
| **Default**  | `8`       |

**Description:** The number of concurrent tasks to run.

----------------------------------------------------------------------------------------------------------------------------
