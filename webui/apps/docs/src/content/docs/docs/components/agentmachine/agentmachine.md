---
title: AgentMachine
description: "Description of AgentMachine component"
---
# Schema Docs

- [1. Property `implementation`](#implementation)
- [2. Property `symbolic_memory`](#symbolic_memory)
  - [2.1. Property `implementation`](#symbolic_memory_implementation)
- [3. Property `file_memory`](#file_memory)
  - [3.1. Property `implementation`](#file_memory_implementation)
- [4. Property `similarity_memory`](#similarity_memory)
  - [4.1. Property `implementation`](#similarity_memory_implementation)
- [5. Property `security_manager`](#security_manager)
  - [5.1. Property `implementation`](#security_manager_implementation)
- [6. Property `process_file_system`](#process_file_system)
  - [6.1. Property `implementation`](#process_file_system_implementation)
- [7. Property `fail_on_agent_start_error`](#fail_on_agent_start_error)

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

| Property                                                   | Pattern | Type    | Deprecated | Definition | Title/Description                                                                 |
| ---------------------------------------------------------- | ------- | ------- | ---------- | ---------- | --------------------------------------------------------------------------------- |
| - [implementation](#implementation )                       | No      | const   | No         | -          | -                                                                                 |
| - [symbolic_memory](#symbolic_memory )                     | No      | object  | No         | -          | The Symbolic Memory implementation.                                               |
| - [file_memory](#file_memory )                             | No      | object  | No         | -          | The File Memory implementation.                                                   |
| - [similarity_memory](#similarity_memory )                 | No      | object  | No         | -          | The Vector Memory implementation.                                                 |
| - [security_manager](#security_manager )                   | No      | object  | No         | -          | The Security Manager implementation.                                              |
| - [process_file_system](#process_file_system )             | No      | object  | No         | -          | The Process File System implementation. Used to store files related to processes. |
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

**Description:** The Symbolic Memory implementation.

| Property                                             | Pattern | Type   | Deprecated | Definition | Title/Description |
| ---------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#symbolic_memory_implementation ) | No      | string | No         | -          | -                 |
| - [](#symbolic_memory_additionalProperties )         | No      | object | No         | -          | -                 |

### <a name="symbolic_memory_implementation"></a>2.1. Property `implementation`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

## <a name="file_memory"></a>3. Property `file_memory`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

**Description:** The File Memory implementation.

| Property                                         | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------ | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#file_memory_implementation ) | No      | string | No         | -          | -                 |
| - [](#file_memory_additionalProperties )         | No      | object | No         | -          | -                 |

### <a name="file_memory_implementation"></a>3.1. Property `implementation`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

## <a name="similarity_memory"></a>4. Property `similarity_memory`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

**Description:** The Vector Memory implementation.

| Property                                               | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------ | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#similarity_memory_implementation ) | No      | string | No         | -          | -                 |
| - [](#similarity_memory_additionalProperties )         | No      | object | No         | -          | -                 |

### <a name="similarity_memory_implementation"></a>4.1. Property `implementation`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

## <a name="security_manager"></a>5. Property `security_manager`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

**Description:** The Security Manager implementation.

| Property                                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| ----------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#security_manager_implementation ) | No      | string | No         | -          | -                 |
| - [](#security_manager_additionalProperties )         | No      | object | No         | -          | -                 |

### <a name="security_manager_implementation"></a>5.1. Property `implementation`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

## <a name="process_file_system"></a>6. Property `process_file_system`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

**Description:** The Process File System implementation. Used to store files related to processes.

| Property                                                 | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [implementation](#process_file_system_implementation ) | No      | string | No         | -          | -                 |
| - [](#process_file_system_additionalProperties )         | No      | object | No         | -          | -                 |

### <a name="process_file_system_implementation"></a>6.1. Property `implementation`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

## <a name="fail_on_agent_start_error"></a>7. Property `fail_on_agent_start_error`

**Title:** Fail On Agent Start Error

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `false`   |

**Description:** If true, the machine will fail to start if an agent fails to start. Default: False

----------------------------------------------------------------------------------------------------------------------------
