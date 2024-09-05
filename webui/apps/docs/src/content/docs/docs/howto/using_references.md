---
title: How to Use References
description: References - Working with and Creating Custom References
---

References make up the backbone of Eidolon's runtime dependency injection. Defining references in a component's spec allows your custom attributes to be injected dynamically through yaml configuration files.

## Why

When customizing or building your own [AgentTemplates](docs/howto/build_custom_agents/), [LogicUnits](/docs/components/logicunit/overview/), or other components, you may want to extend Eidolon's built-in components, or even create your own interfaces that can be expanded in the future. 

Eidolon has the concept of **References** which dynamically injects dependencies from resources defined in yaml files. References are fundamental to Eidolon's pluggable architecture.

## What

At its simplest, a **reference** is a class. Any object within your python environment can be _referenced_ by its fully qualified name (FQN).

A **spec** is a [Pydantic model](https://docs.pydantic.dev/latest/concepts/models/).

## How

In Eidolon, you define the _spec_ for a _reference_ in python code. This allows you to configure runtime attributes external to the code through yaml files. The specable attributes for Eidolon built-in components are automatically published in the online documentation.

### Defining a Reference with a Spec

Custom components of any kind can define a spec. This is what defines the component's configuration which can be 
defined or overridden in yaml.  We can then define our resource to use this spec.

```python
class CustomResourceSpec(BaseModel):
    question: str = "what is the meaning of life"
    answer: int = 42

class CustomResource(Specable[CustomResourceSpec]):
    def solve(self):
        return f"{self.spec.question} + {self.spec.answer}" 
```

In simple examples, you can also define our spec within the resource itself. It will be wired up the same as above.

```python
class CustomResource(BaseModel):
    question: str = "what is the meaning of life"
    answer: int = 42
    def solve(self):
        return f"{self.question} + {self.answer}"
```

### Using References within a Spec

What if you want to use a reference within a reference? 

- Eidolon has a **Reference** type that wires the references up at runtime. 

- The **AnnotatedReference** type defines the default factory for you.

Below is an example of a resource that uses an APU as a custom resource. Notice that the reference will not actually be an instance of the APU, but a factory that will create the APU when the resource is initialized.

```python
class CustomResourceSpec(BaseModel):
      question: str = "what is the meaning of life"
      oracle: AnnotatedReference[APU]

class CustomResource(Specable[CustomResourceSpec]):
    def __init__(self):
        self.apu = self.spec.oracle.initialize()
  
    def solve(self):
        ... 
```
