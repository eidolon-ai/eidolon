---
title: Swapping LLMs
description: References - How to Swap LLM providers or models
---

In Eidolon your choice of LLM is a configuration choice. This means you can easily swap out the underlying LLM model or 
even LLM provider without needing to change any code.

This document will show you how to swap out the LLM component within your agent.

---
## 1. Find the APU Component
Head over to the [builtin APU component list](/docs/components/apu/overview) to find a list of APUs available out of the box.

Can't find the find the apu you are looking for? Check out [Defining a Custom APU](#defining-a-custom-apu).

* <small>The APU is a little more than just an LLM. It also contains enhancements to allow capabilities such as 
JSON mode or image processing (even for small models that can't support it natively). To read more check out 
[What is an APU and how does it work?](https://www.eidolonai.com/what_is_apu).</small>


## 2. Update Your Agent
So now you have chosen the APU you want to use. For this example we will choose `ClaudeOpus`.

To update your agent, all you need to do is update the `apu` field in your agent's spec.

```yaml
apiVersion: eidolon/v1
kind: Agent
metadata:
  name: claudey-mcclaudagent
spec: 
  apu: ClaudeOpus
```


* <small>When choosing an LLM from a different provider, you will need to update your auth information accordingly. See
  the specific APU documentation for more details or check out our how to on [LLM Authentication](/docs/howto/llm_authentication).</small>
* <small>For more information on customizing components (including changing machine wide defaults), see [Customize Builtins](/docs/howto/customize_builtins).</small>

---
## Defining a Custom APU
We try to keep common models in the builtin APUs, but sometimes you need to define your own. This is especially true 
when you are using a model that is not supported by the builtin APUs.

For this example let's imagine we are using a custom model from OpenAI called `gpt-sam`. It is a highly specialized model,
and works by directly texting Sam Altman, so not many people have access to it.

We can specify the model inline within our agent's configuration.

```yaml
apiVersion: eidolon/v1
kind: Agent
metadata:
  name: qa
spec:
  apu: 
    llm_unit:
      implementation: OpenAIGPT  # this must match the LLM provider
      model:
        human_name: "Sam the Man"
        name: "gpt-sam"
```

* <small>For specifics on how to customize an APU, check out the [docs for your chosen provider's apu](/docs/components/apu/overview).</small>
