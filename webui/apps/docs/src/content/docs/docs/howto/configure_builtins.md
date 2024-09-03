---
title: How to Configure Built-in Components
description: Reference - Configuring Pluggable Resources
---
In a multi-agent system, agents will have vastly different needs. For example, system prompts can be vague or preciese, or you may want to use a variety of LLM models. 

Eidolon allows you to configure agents without ever needing to jump into code. You can override deeply nested configuration default, as well as define new custom resources to use as templates.

## Why
LLM applications require a ton of tweaking 🔨. Jumping into code for each and every code means this fiddling is slower 
and more error-prone. That is why at Eidolon 👻 we separated prompting and system configuration into simple 
kubernetes-like yaml files that can be modified without needing to open up a code editor 🔡. 

Beyond simply speeding up cycle time 🚀, this also allows more personas 🧑‍🚒🧑‍🏫🧑‍🎨 to work on
the application without needing deep understanding of the codebase 🔡. This allows different personas to focus on 
architecture, fine-tuning, model selection, and prompt engineering so each person can focus on their domain expertise 
without getting bogged down.

## How
### Spec Configuration

In Eidolon's agent yaml files, you can have probably noticed the `spec` field. This is where you can customize portions 
of the component's configuration.

```yaml
apiVersion: eidolon/v1
kind: Agent
metadata:
  name: qa
spec: ...
```

#### Field Configuration

You can override component defaults at the individual field or attribute level.

```yaml
spec:
  title_generation_mode: "none"   # 🔎 overrides the component's default title_generation_mode
```

#### Overriding Implementation Defaults

Most components have a default implementation. Check the Built-in Components "Overview" and child pages to see the defaults. For example, agents use the [SimpleAgent template by default](https://www.eidolonai.com/docs/components/agents/overview). 

You can override implementation defaults, but remember the new contents need to match the new implementation's spec pattern.

```yaml
spec:
  implementation: RetrieverAgent  # 🔎 defines the new component to use
  loader_pattern: "**/*.test"     # 🔎 overrides the component's default loader_pattern
#  title_generation_mode: "none"  # 🚨 removed since it is now invalid
```

#### Nested Spec Customization
Components can also make [References](/docs/howto/using_references/) to other components. These subcomponents can be customized as well.
```yaml
spec:
  apu:                            # 🔎 modify the component's default apu
    allow_tool_errors: false      # 🔎 by overriding a portion of the apu spec
```

#### Nested Implementation Customization
Of course you can also override nested implementations.
```yaml
spec:
  apu:
    implementation: ConversationalAPU
```

This implementation pointer override is quite common, so we have added as shortcut for it. If you just specify a string 
for the reference, we will treat it as an implementation override.

```yaml
spec:
  apu: ConversationalAPU
```

### Reusable References
Now component customization is nice for experimentation, but it can get quite verbose if we need to constantly make the 
same customization to multiple components. For this reason, we have added **References**. These are reusable 
configurations that can be referenced by multiple components.

Let's create a named resource `frugal_apu` so we can easily point to an older model for some agents.

_frugal_apu.yaml_
```yaml
apiVersion: eidolon/v1
kind: Reference
metadata:
  name: frugal_apu

spec:
  implementation: 'ConversationalAPU'
  llm_unit:
    force_json: 'True'
    max_tokens: '3000'
    model: gpt-3.5-turbo-1106
    temperature: .1
  max_num_function_calls: 20
```

Now within our agent's spec we can just reference this reference by name like we would any other component.
```yaml
spec:
  apu: frugal_apu
```

We can continue to override sub components as you would expect.
```yaml
spec:
  apu: 
    implementation: frugal_apu
    max_num_function_calls: 10
```

### Changing Default Components
Now what if you are a lean startup, and want to use the frugal_apu for all of your agents unless specified otherwise?
You would prefer not to override the apu of every agent, you just want to set frugal_apu as the default apu.

```yaml
apiVersion: eidolon/v1
kind: Reference
metadata:
  name: APU

spec: frugal_apu
```

This reference resource will change any component that references the APU to use our new frugal_apu instead of the 
default (ConversationalAPU).

## Recipes
Most recipes will have some form of customization. Here are a few examples that use it more heavily.

##### [GitHub Repo Expert](/docs/recipes/repo-expert)
The [RepoSearch](/docs/recipes/repo-expert#repo-search) overrides its loader with a different implementation to be able
to read from github. On top of this it then customizes the files this loader can read.
