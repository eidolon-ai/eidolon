---
title: LocalFileMemory
description: Description of the LocalFileMemory component
---

| Property                             | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------ | ------- | ------ | ---------- | ---------- | ----------------- |
| + [implementation](#implementation ) | No      | const  | No         | -          | Implementation    |
| - [root_dir](#root_dir )             | No      | string | No         | -          | Root Dir          |

## <a name="implementation"></a>1. Property `implementation`

**Title:** Implementation

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | Yes     |

Specific value: `"LocalFileMemory"`

## <a name="root_dir"></a>2. Property `root_dir`

**Title:** Root Dir

|              |                              |
| ------------ | ---------------------------- |
| **Type**     | `string`                     |
| **Required** | No                           |
| **Default**  | `"/tmp/eidolon/file_memory"` |

**Description:** The root directory to store files in.

----------------------------------------------------------------------------------------------------------------------------
