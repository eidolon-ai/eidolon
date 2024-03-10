---
title: Pluggable Resources
description: References - Pluggable Resources
---

### Including Pluggable References in Configuration
Agents can include pluggable references to various components like CPUs. Let's use gpt 3.5 instead of 4 to save money and lower the temperature some for more repeatable results.

_qa_agent.yaml_
```yaml
apiVersion: eidolon/v1
kind: Agent
metadata:
  name: qa

spec:
  implementation: getting_started.qa.QualityAssurance
  agent_refs: ["hello_world"]
  cpu:
    spec:
      llm_unit:
        spec:
          force_json: 'True'
          max_tokens: '3000'
          model: gpt-3.5-turbo-1106
          temperature: '.1'
      max_num_function_calls: '20'
```

### Named References
This is pretty verbose in our qa_agent.yaml, and would be redundant if we wanted other agents to run with the same cpu. Let's create a named resource `cpu.frugal` which we can reuse for our agents.

_frugal_cpu.yaml_
```yaml
apiVersion: eidolon/v1
kind: Reference
metadata:
  name: frugal_cpu

spec:
  implementation: "eidolon_ai_sdk.cpu.conversational_agent_cpu.ConversationalAgentCPU"
  cpu:
    spec:
      llm_unit:
        spec:
          force_json: 'True'
          max_tokens: '3000'
          model: gpt-3.5-turbo-1106
          temperature: '.1'
      max_num_function_calls: '20'
```

_qa_agent.yaml_
```yaml
apiVersion: eidolon/v1
kind: Agent
metadata:
  name: qa

spec:
  implementation: getting_started.qa.QualityAssurance
  agent_refs: ["hello_world"]
  cpu: frugal_cpu
```

We refer to our named resource as `{kind}.{metadata.name}`, or in this case `CPU.default`. We can create named resources 
for any type of `Reference` within a spec. For example, we could have created a named reference for the llm_unit instead 
(or in addition to) of the cpu.