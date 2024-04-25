---
publishDate: 2024-04-25T00:00:00Z
title: 'Testing GenAI Applications'
excerpt: "There are only two hard things in Computer Science: testing llm applications and naming things."
image: https://i.imgflip.com/8ny6dj.jpg
tags:
  - testing
  - LLM App Development
metadata:
  canonical: https://www.eidolonai.com/testing-llm-apps
---

Testing is a crucial step in deploying applications, ensuring their stability and increasing developer productivity. 
Testing LLM apps poses unique challenges not present in many software applications today. In this article, we'll explore
these challenges and provide practical solutions for successfully testing LLM applications.

## The Problems

### Non-deterministic nature of LLMs

LLMs are non-deterministic, meaning their output varies each time they process the same input. This makes it really 
challenging to write reliable tests. Even if your tests pass 99% of the time, which sounds great, and you have 100 
tests, which isn’t that many, this still means your test run will almost always fail! 73.4% of the time to be exact. 
That’s enough to bog down any organization.

### Slow to Run

An LLM is built from billions of parameters. I mean, we are computing thought as-a-service, so we can cut the LLMs some 
slack. But this simply doesn’t scale when it comes to testing. Even if we are to get around this problem by running 
tests in parallel, this creates yet another level of complexity (see the non-deterministic problem above). Even if you 
can manage this complexity, writing and debugging your tests will still be slow since the individual test takes so long 
to run. To put things lightly, it won’t be easy or fun.

### Expensive

10k tokens for a penny sounds decent at first, but anyone who has checked their OpenAI bill knows these tokens aren’t 
cheap. Paying to regenerate your test tokens tens or hundreds of times per day quickly burns through the Dev budget.

![if you could rerun those failing tests for me... that would be great](https://i.imgflip.com/8ny4mo.jpg "Office Space Meme")

## So What Now?

So what are we going to do about this? We know that ignoring testing will work for a while, but that’s a short-sighted 
strategy that quickly spirals out of control. Let’s take a step back and think about our goals as developers…

* _Ensure my PR doesn't break prod_

As a developer, that’s it. This is all I really care about. After all, I’m not on the hook for testing the LLM, just how 
my application interacts with it. As a developer, my prompts need to behave in a way that fits my application and this 
all needs to come together without any portion of the app falling over. The integration with a LLM is important, but the 
actual call to the LLM is not. This starts to smell a lot like a __recording__.

### The Power of Recordings in Testing

Devs have been using recordings to test service dependencies for a while now, and what is an LLM call other than another 
service dependency? It’s not sexy new technology, but as the adage goes: if it ain’t broke, don’t fix it.

At Eidolon we have been using vcrpy heavily for our internal testing. We record our LLM calls on the way out so we know 
our application is generating a valid request to the LLM and that our application can handle the response. We get to 
write our service level tests using real dependencies without mocks. This safety net gives me a huge amount of 
confidence when working on the project. What’s more, the test execution becomes fast, free, and doesn’t even require an 
API token.

### Not just for LLMs

Sophisticated genAI apps aren’t just using LLMs. Many of the related technologies (image generation/descriptions, 
voice/text, embeddings, etc.) share the same characteristics that make testing LLMs a real challenge. But here’s the 
great news: because recordings capture HTTP requests, they work here just as well as they do for LLM requests!

![Record all the things!](https://i.imgflip.com/8ny4uh.jpg "All The Things Meme")

## Considerations When Using Recordings

There's no free lunch, and recordings are no exception. Here are some things to keep in mind when using recordings.

### Ensure Stable LLM Requests

LLM requests must be identical between test runs to replay recordings. If a test's LLM request mutates between runs, the
test will fail because the recording is not valid for the new request. Many applications will run into this issue. For example,
in Eidolon we generate random IDs per-conversation that enter the LLM context when agents are talking to each other.
To work around this, we have to use stable ID's that increment per-test when testing.

### Maintain Test Reliability

Since these are recordings and not mocks, the tests still need to actually run in the absence of an existing recording. 
This means the test still needs to only validate relevant information. If anyone needs to re-record a test, the 
validation shouldn’t need to be rewritten. A flakey test that usually passes is ok (since hitting a failure when 
generating recordings can just be addressed by re-generating), but a validation on the exact LLM response means it will 
never pass again.

### Measure LLM/Prompt Performance Separately

Recordings alone are ineffective for capturing performance or accuracy metrics. Since you are effectively caching the 
response, you don’t have a good sense of the LLM or prompt’s performance. This is where performance benchmarking comes 
into play for evaluating the efficacy of your fine tuning or prompt engineering.

## Conclusion

Testing is critical for deploying production-ready LLM applications and enhancing developer productivity. This is hard 
to do. But recordings mitigate difficulties associated with testing generative AI applications. They are not a panacea, 
but certainly a valuable tool for the modern day LLM application developer.
