---
title: MongoSymbolicMemory
description: "Description of MongoSymbolicMemory component"
---

| Property                                               | Pattern | Type   | Deprecated | Definition | Title/Description       |
| ------------------------------------------------------ | ------- | ------ | ---------- | ---------- | ----------------------- |
| - [implementation](#implementation )                   | No      | const  | No         | -          | MongoSymbolicMemory     |
| - [mongo_connection_string](#mongo_connection_string ) | No      | string | No         | -          | Mongo Connection String |
| - [mongo_database_name](#mongo_database_name )         | No      | string | No         | -          | Mongo Database Name     |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** MongoSymbolicMemory

Specific value: `"MongoSymbolicMemory"`

## <a name="mongo_connection_string"></a>2. Property `mongo_connection_string`

**Title:** Mongo Connection String

|              |                                                      |
| ------------ | ---------------------------------------------------- |
| **Type**     | `string`                                             |
| **Required** | No                                                   |
| **Default**  | `"mongodb://localhost:27017/?directConnection=true"` |

**Description:** The connection string to the MongoDB instance.

## <a name="mongo_database_name"></a>3. Property `mongo_database_name`

**Title:** Mongo Database Name

|              |             |
| ------------ | ----------- |
| **Type**     | `string`    |
| **Required** | No          |
| **Default**  | `"eidolon"` |

**Description:** The name of the MongoDB database to use.

----------------------------------------------------------------------------------------------------------------------------
