---
title: AgentMachine
description: "Description of AgentMachine component"
---

| Property                                                   | Pattern | Type    | Deprecated | Definition | Title/Description                                                                 |
| ---------------------------------------------------------- | ------- | ------- | ---------- | ---------- | --------------------------------------------------------------------------------- |
| - [implementation](#implementation )                       | No      | const   | No         | -          | -                                                                                 |
| - [symbolic_memory](#symbolic_memory )                     | No      | object  | No         | In         | The Symbolic Memory implementation.                                               |
| - [file_memory](#file_memory )                             | No      | object  | No         | In         | The File Memory implementation.                                                   |
| - [similarity_memory](#similarity_memory )                 | No      | object  | No         | In         | The Vector Memory implementation.                                                 |
| - [security_manager](#security_manager )                   | No      | object  | No         | In         | The Security Manager implementation.                                              |
| - [process_file_system](#process_file_system )             | No      | object  | No         | In         | The Process File System implementation. Used to store files related to processes. |
| - [fail_on_agent_start_error](#fail_on_agent_start_error ) | No      | boolean | No         | -          | Fail On Agent Start Error                                                         |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

Specific value: `"AgentMachine"`

## <a name="symbolic_memory"></a>2. Property `symbolic_memory`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            |                                                                           |

**Description:** The Symbolic Memory implementation.

## <a name="file_memory"></a>3. Property `file_memory`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            |                                                                           |

**Description:** The File Memory implementation.

## <a name="similarity_memory"></a>4. Property `similarity_memory`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            |                                                                           |

**Description:** The Vector Memory implementation.

## <a name="security_manager"></a>5. Property `security_manager`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            |                                                                           |

**Description:** The Security Manager implementation.

## <a name="process_file_system"></a>6. Property `process_file_system`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            |                                                                           |

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
