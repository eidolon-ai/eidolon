---
title: How to Build Custom Tools
description: Reference - Building Tools
---
Eidolon defines several useful built-in [Tools](/docs/components/logicunit/overview) out of the box, but if you need 
capabilities that are not covered by the built-ins, you may need to create your own.

## What are tools?
Tools are the capabilities your agent has to interact with the world. They can be as simple as a calculator or as 
complex as you can imagine. Tools can be in-memory calculations, data manipulation, or even API-calls.

## Is it an Agent or a tool?
Sometimes it is hard to distinguish between an agent and a tool. Both can implement logic and have no constraints on how
they interact with the world. Agents are typically meant to be interacted with by users, while tools are capabilities 
that can given to enhance an agent's capabilities.

## Defining a Tool

To create a new tool, extend the `ToolBuilder` class and decorate the methods you would like to expose as actions.

```python
from eidolon_ai_sdk.system.tool_builder import ToolBuilder


class Add(ToolBuilder):
  pass


@Add.tool()
async def add(a: int, b: int):
  """Add two numbers together."""
  return a + b
```


When the Add ToolBuilder is added to an agent, the agent will see a tool named `add` with the description "Add two numbers together."
The json-schema for the tool will be automatically generated based on the type hints of the function. In this case the schema will be:

```json
{
  "type": "object",
  "properties": {
    "a": {
      "type": "integer"
    },
    "b": {
      "type": "integer"
    }
  },
  "required": ["a", "b"]
}
```

### Defining configuration

Some tools will need to be configured when they are added to an agent. Perhaps they are hitting an API and need an API 
key, or they need to know the location of a file. To add configuration to a tool, add attributes to the ToolBuilder 
class. It is just a pydantic model, so head over to the [pydantic documentation](https://docs.pydantic.dev/latest/) for 
more information. Remember that this defines the configuration for the tool when specified in the yaml file. 

```python
class Add(ToolBuilder):
  max_number: Optional[int] = None


@Add.tool()
async def add(a: int, b: int, spec: Add):
  """Add two numbers together."""
  if a > spec.max_number:
    raise Exception(f"{a} is too big!")
  return a + b
```


In this example we added a `max_number` attribute to the `Add` tool. This attribute can be set when the tool is added to 
an agent. The `spec` parameter is a reference to the tool instance, so you can access any attributes defined on the tool.
Note that the json schema created for the LLM will not include the `spec` parameter, it is a special keyword.

### Defining multiple tools

You can define multiple tools in the same class by using the `@ToolBuilder.tool` decorator multiple times.

```python
@Math.tool()
async def add(a: int, b: int):
  """Add two numbers together."""
  return a + b

@Math.tool()
async def subtract(a: int, b: int):
  """Subtract two numbers."""
  return a - b
```

Now when an agent is given the `SimpleMath` tool bundle, it will have two tools, `add` and `subtract`.

### Dynamically constructing tools

Similarly, you can dynamically construct tools by using the `@ToolBuilder.dynamic_contract` decorator to use 
configuration (or even the conversation history or agent state) to determine what tools will be available to the agent.

```python
class DynamicMath(ToolBuilder):
  operations: List[str] = ["add"]

@DynamicMath.dynamic_contract(spec: DynamicMath)
def math_tools(spec: DynamicMath):
  for operation in spec.operations:
    if operation == "add":
      @DynamicMath.tool()
      async def add(a: int, b: int):
        """Add two numbers together."""
        return a + b
    elif operation == "subtract":
      @DynamicMath.tool()
      async def subtract(a: int, b: int):
        """Subtract two numbers."""
        return a - b
    elif operation == "multiply":
      @DynamicMath.tool()
      def multiply(a: int, b: int):
        """Multiply two numbers."""
        return a * b
```

### Overriding Default Behavior
Tool name, description, and schema can be overridden by passing them as arguments to the `@ToolBuilder.tool` decorator.

```python
@Add.tool(name="add_numbers", description="Add two numbers together", schema={"type": "object", "properties": {"a": {"type": "integer"}, "b": {"type": "integer"}}, "required": ["a", "b"]})
async def _fn(a, b):
  return a + b
```
