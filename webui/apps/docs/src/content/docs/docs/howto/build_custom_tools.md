---
title: How to Build Custom Tools
description: Reference - Building Tools
---
Eidolon defines several useful built-in [Tools](/docs/components/logicunit/overview) out of the box, but if you need 
capabilities that are not covered by the built-ins, you may need to create your own.

## What are tools?
Tools are the capabilities your agent has to interact with the world. They can be as simple as a calculator or as 
complex as you can imagine. Tools can be in-memory calculations, data manipulation, or even API-calls.

## Should I implement a new Agent or tool?
Sometimes it is hard to distinguish between an agent and a tool. Both can implement logic and have no constraints on how
they interact with the world. Agents are typically meant to be interacted with by users (or other agents) and usually 
use an LLM internally to plan / execute action. On the other hand, Tools are capabilities that are given to agents so 
that they can interact with the outside world programmatically.

## Building a Tool
### Defining a Tool

To create a new tool, extend the `ToolBuilder` class and decorate the methods you would like to expose as actions.

```python
from eidolon_ai_sdk.system.tool_builder import ToolBuilder

class Add(ToolBuilder):
  pass

@Add.tool()
def add(a: int, b: int):
  """Add two numbers together."""
  return a + b
```


When adding a tool to a `ToolBuilder` class, you can optionally define the `name`, `description`, and `parameters` 
(json schema) of the tool. These values are derived from the function name, docstring, and function signature by default.

In this example, the following values are inferred from the function definition:
```python
name="add", 
description="Add two numbers together", 
parameters=dict(
  type="object", 
  properties=dict(a=dict(type="integer"), b=dict(type="integer")), 
  required=["a", "b"]
)
```


### Multiple Tools on a Single Builder

You can define multiple tools in the same class by using the `tool` decorator multiple times.

```python
class Calculator(ToolBuilder):
  pass

@Calculator.tool()
def add(a: int, b: int):
  """Add two numbers together."""
  return a + b

@Calculator.tool()
def subtract(a: int, b: int):
  """Subtract two numbers."""
  return a - b
```

Now when an agent is given the `Calculator` tool bundle, it will have two tools, `add` and `subtract`.


### Configurable Tools

Some tools will need to be configured when they are added to an agent. Perhaps they are hitting an API and need an API 
key, or they need to know the location of a file. To add configuration to a tool, add attributes to the ToolBuilder 
class. It is just a pydantic model, so head over to the [pydantic documentation](https://docs.pydantic.dev/latest/) for 
more information. Remember that this defines the configuration for the tool reference when specified in the yaml file. 

```python
class Add(ToolBuilder):
  max_number: Optional[int] = None

@Add.tool()
def add(a: int, b: int, spec: Add):
  """Add two numbers together."""
  if a > spec.max_number:
    raise Exception(f"{a} is too big!")
  return a + b
```


In this example we added a `max_number` attribute to the `Add` tool. This attribute can be set when the tool is added to 
an agent. The `spec` parameter is a reference to the tool instance, so you can access any attributes defined on the tool.
Note that the json schema created for the LLM will not include the `spec` parameter, it is a special keyword.

### Building Tools Dynamically

Similarly, you can dynamically construct tools by using the `@ToolBuilder.dynamic_contract` decorator to use 
configuration (or even the conversation history or agent state) to determine what tools will be available to the agent.

```python
class Calculator(ToolBuilder):
  operations: List[str] = ["add"]

@Calculator.dynamic_contract
def math_tools(spec: Calculator):

  if "add" in spec.operations:
    @Calculator.tool()
    def add(a: int, b: int):
      """Add two numbers together."""
      return a + b
  
  if "subtract" in spec.operations:
    @Calculator.tool()
    def subtract(a: int, b: int):
      """Subtract two numbers."""
      return a - b
  
  if "multiply" in spec.operations:
    @Calculator.tool()
    def multiply(a: int, b: int):
      """Multiply two numbers."""
      return a * b
```

### Asynchronous Tools
We know that some tools may need to be asynchronous, so we have added support for that. Just add the `async` keyword to 
your tool definition and we will take care of it for you. Similarly, you can use async functions to define your 
`dymamic_contact` function as well.

```python
class AsyncAdd(ToolBuilder):
  pass

AsyncAdd.tool()
async def add(a: int, b: int):
  """Add two numbers together."""
  return await io_bound_add(a, b)
```
