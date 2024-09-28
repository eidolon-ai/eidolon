---
title: MongoSymbolicMemory
description: "Description of MongoSymbolicMemory component"
---
# MongoSymbolicMemory

- [1. [Optional] Property implementation](#implementation)
- [2. [Optional] Property mongo_connection_string](#mongo_connection_string)
- [3. [Optional] Property mongo_database_name](#mongo_database_name)

**Title:** MongoSymbolicMemory

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

Specific value: `"MongoSymbolicMemory"`

</blockquote>
</details>

<details>
<summary>
<strong> <a name="mongo_connection_string"></a>2. [Optional] Property mongo_connection_string</strong>  

</summary>
<blockquote>

**Title:** Mongo Connection String

|              |                                                      |
| ------------ | ---------------------------------------------------- |
| **Type**     | `string`                                             |
| **Required** | No                                                   |
| **Default**  | `"mongodb://localhost:27017/?directConnection=true"` |

**Description:** The connection string to the MongoDB instance.

</blockquote>
</details>

<details>
<summary>
<strong> <a name="mongo_database_name"></a>3. [Optional] Property mongo_database_name</strong>  

</summary>
<blockquote>

**Title:** Mongo Database Name

|              |             |
| ------------ | ----------- |
| **Type**     | `string`    |
| **Required** | No          |
| **Default**  | `"eidolon"` |

**Description:** The name of the MongoDB database to use.

</blockquote>
</details>

----------------------------------------------------------------------------------------------------------------------------
