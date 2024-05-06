---
title: How to use References
description: References - Using References
---

References make up the backbone of Eidolon's yaml driven dependency injection. Defining them in a component's spec 
allows that reference to be injected dynamically through configuration files.

## Why

When building custom AgentTemplates, LogicUnits, or other components, you may want to use built in pluggable compoenents,
or even create your own interfaces that can be expanded in the future. Eidolon has the concept of **References** which
will dynamically inject dependencies from the resources you have defined in your yaml files. 

## How

Custom components of any kind can define a **spec**. This is what defines the component's configuration which can be 
defined or overridden in yaml. The spec is just a **Pydantic** model. We can then define our resource to use this spec.

```python
class CustomResourceSpec(BaseModel):
    question: str = "what is the meaning of life"
    answer: int = 42

class CustomResource(Specable[CustomResourceSpec]):
    def solve(self):
        return f"{self.spec.question} + {self.spec.answer}" 
```

In simple examples, we can also just define our spec within the resource itself. It will be wired up the same as above.
```python
class CustomResource(BaseModel):
    question: str = "what is the meaning of life"
    answer: int = 42
    def solve(self):
        return f"{self.question} + {self.answer}"
```

### Using References within References
So that is all well and good, but what if we want to use a reference within a reference? We have a **Reference** type 
that is what wires the references up at runtime. There is also an **AnnotatedReference** type that defines the default 
factory for you.

Below is an example of a resource that uses an apu as a custom resources. Notice that the reference will not actually 
be an instance of the apu, but a factory that will create the apu when the resource is initialized.


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
