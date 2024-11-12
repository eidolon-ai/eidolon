---
title: LocalFileMemory
description: Description of the LocalFileMemory component
---

**Description:** Retrieve documents from a local file system. Note that this is the file system where the Eidolon application is
running. This means building the files onto the runtime image, or mounting a volume to the container.

[Docker volume](https://docs.docker.com/engine/storage/volumes/#use-a-volume-with-docker-compose)
[Build the files into the runtime image](https://docs.docker.com/reference/dockerfile/#copy)
[Kubernetes volumes](https://kubernetes.io/docs/concepts/storage/volumes/)

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
