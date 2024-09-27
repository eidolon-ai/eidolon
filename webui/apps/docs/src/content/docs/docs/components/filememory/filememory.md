---
title: FileMemory
description: "Description of FileMemory component"
---
# Schema Docs

- [1. Property `implementation`](#implementation)
- [2. Property `root_dir`](#root_dir)

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

| Property                             | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------ | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#implementation ) | No      | const  | No         | -          | -                 |
| - [root_dir](#root_dir )             | No      | string | No         | -          | Root Dir          |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

Specific value: `"FileMemory"`

## <a name="root_dir"></a>2. Property `root_dir`

**Title:** Root Dir

|              |                              |
| ------------ | ---------------------------- |
| **Type**     | `string`                     |
| **Required** | No                           |
| **Default**  | `"/tmp/eidolon/file_memory"` |

**Description:** The root directory to store files in.

----------------------------------------------------------------------------------------------------------------------------
