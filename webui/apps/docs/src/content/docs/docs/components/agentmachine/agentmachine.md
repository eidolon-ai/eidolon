---
title: AgentMachine
description: "Description of AgentMachine component"
---
| Property                                                   | Pattern | Type                         | Deprecated | Definition | Title/Description                                                                 |
| ---------------------------------------------------------- | ------- | ---------------------------- | ---------- | ---------- | --------------------------------------------------------------------------------- |
| - [implementation](#implementation )                       | No      | const                        | No         | -          | -                                                                                 |
| - [symbolic_memory](#symbolic_memory )                     | No      | [Reference[SymbolicMemory]](/docs/components/symbolicmemory/overview)    | No         | -          | The Symbolic Memory implementation.                                               |
| - [file_memory](#file_memory )                             | No      | [Reference[FileMemory]](/docs/components/filememory/overview)        | No         | -          | The File Memory implementation.                                                   |
| - [similarity_memory](#similarity_memory )                 | No      | [Reference[SimilarityMemory]](/docs/components/similaritymemory/overview)  | No         | -          | The Vector Memory implementation.                                                 |
| - [security_manager](#security_manager )                   | No      | [Reference[SecurityManager]](/docs/components/securitymanager/overview)   | No         | -          | The Security Manager implementation.                                              |
| - [process_file_system](#process_file_system )             | No      | [Reference[ProcessFileSystem]](/docs/components/processfilesystem/overview) | No         | -          | The Process File System implementation. Used to store files related to processes. |
| - [fail_on_agent_start_error](#fail_on_agent_start_error ) | No      | boolean                      | No         | -          | Fail On Agent Start Error                                                         |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

Specific value: `"AgentMachine"`

## <a name="symbolic_memory"></a>2. Property `symbolic_memory`

|              |                                        |
| ------------ | -------------------------------------- |
| **Type**     | [`Reference[SymbolicMemory]`](/docs/components/symbolicmemory/overview)            |
| **Required** | No                                     |
| **Default**  | `{"implementation": "SymbolicMemory"}` |

**Description:** The Symbolic Memory implementation.

## <a name="file_memory"></a>3. Property `file_memory`

|              |                                    |
| ------------ | ---------------------------------- |
| **Type**     | [`Reference[FileMemory]`](/docs/components/filememory/overview)            |
| **Required** | No                                 |
| **Default**  | `{"implementation": "FileMemory"}` |

**Description:** The File Memory implementation.

## <a name="similarity_memory"></a>4. Property `similarity_memory`

|              |                                          |
| ------------ | ---------------------------------------- |
| **Type**     | [`Reference[SimilarityMemory]`](/docs/components/similaritymemory/overview)            |
| **Required** | No                                       |
| **Default**  | `{"implementation": "SimilarityMemory"}` |

**Description:** The Vector Memory implementation.

## <a name="security_manager"></a>5. Property `security_manager`

|              |                                         |
| ------------ | --------------------------------------- |
| **Type**     | [`Reference[SecurityManager]`](/docs/components/securitymanager/overview)            |
| **Required** | No                                      |
| **Default**  | `{"implementation": "SecurityManager"}` |

**Description:** The Security Manager implementation.

## <a name="process_file_system"></a>6. Property `process_file_system`

|              |                                           |
| ------------ | ----------------------------------------- |
| **Type**     | [`Reference[ProcessFileSystem]`](/docs/components/processfilesystem/overview)            |
| **Required** | No                                        |
| **Default**  | `{"implementation": "ProcessFileSystem"}` |

**Description:** The Process File System implementation. Used to store files related to processes.

## <a name="fail_on_agent_start_error"></a>7. Property `fail_on_agent_start_error`

**Title:** Fail On Agent Start Error

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `false`   |

**Description:** If true, the machine will fail to start if an agent fails to start. Default: False

----------------------------------------------------------------------------------------------------------------------------
