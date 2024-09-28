---
title: AgentMachine
description: "Description of AgentMachine component"
---
# AgentMachine

- [1. [Optional] Property implementation](#implementation)
- [2. [Optional] Property symbolic_memory](#symbolic_memory)
- [3. [Optional] Property file_memory](#file_memory)
- [4. [Optional] Property similarity_memory](#similarity_memory)
- [5. [Optional] Property security_manager](#security_manager)
- [6. [Optional] Property process_file_system](#process_file_system)
- [7. [Optional] Property fail_on_agent_start_error](#fail_on_agent_start_error)

**Title:** AgentMachine

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

Specific value: `"AgentMachine"`

</blockquote>
</details>

<details>
<summary>
<strong> <a name="symbolic_memory"></a>2. [Optional] Property symbolic_memory</strong>  

</summary>
<blockquote>

|              |                                        |
| ------------ | -------------------------------------- |
| **Type**     | [`Reference[SymbolicMemory]`](/docs/components/symbolicmemory/overview)            |
| **Required** | No                                     |
| **Default**  | `{"implementation": "SymbolicMemory"}` |

**Description:** The Symbolic Memory implementation.

</blockquote>
</details>

<details>
<summary>
<strong> <a name="file_memory"></a>3. [Optional] Property file_memory</strong>  

</summary>
<blockquote>

|              |                                    |
| ------------ | ---------------------------------- |
| **Type**     | [`Reference[FileMemory]`](/docs/components/filememory/overview)            |
| **Required** | No                                 |
| **Default**  | `{"implementation": "FileMemory"}` |

**Description:** The File Memory implementation.

</blockquote>
</details>

<details>
<summary>
<strong> <a name="similarity_memory"></a>4. [Optional] Property similarity_memory</strong>  

</summary>
<blockquote>

|              |                                          |
| ------------ | ---------------------------------------- |
| **Type**     | [`Reference[SimilarityMemory]`](/docs/components/similaritymemory/overview)            |
| **Required** | No                                       |
| **Default**  | `{"implementation": "SimilarityMemory"}` |

**Description:** The Vector Memory implementation.

</blockquote>
</details>

<details>
<summary>
<strong> <a name="security_manager"></a>5. [Optional] Property security_manager</strong>  

</summary>
<blockquote>

|              |                                         |
| ------------ | --------------------------------------- |
| **Type**     | [`Reference[SecurityManager]`](/docs/components/securitymanager/overview)            |
| **Required** | No                                      |
| **Default**  | `{"implementation": "SecurityManager"}` |

**Description:** The Security Manager implementation.

</blockquote>
</details>

<details>
<summary>
<strong> <a name="process_file_system"></a>6. [Optional] Property process_file_system</strong>  

</summary>
<blockquote>

|              |                                           |
| ------------ | ----------------------------------------- |
| **Type**     | [`Reference[ProcessFileSystem]`](/docs/components/processfilesystem/overview)            |
| **Required** | No                                        |
| **Default**  | `{"implementation": "ProcessFileSystem"}` |

**Description:** The Process File System implementation. Used to store files related to processes.

</blockquote>
</details>

<details>
<summary>
<strong> <a name="fail_on_agent_start_error"></a>7. [Optional] Property fail_on_agent_start_error</strong>  

</summary>
<blockquote>

**Title:** Fail On Agent Start Error

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `false`   |

**Description:** If true, the machine will fail to start if an agent fails to start. Default: False

</blockquote>
</details>

----------------------------------------------------------------------------------------------------------------------------
