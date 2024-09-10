---
title: SpanProcessor Overview
description: Interface which allows hooks for SDK's `Span` start and end method
    invocations.

    Span processors can be registered directly using
    :func:`TracerProvider.add_span_processor` and they are invoked
    in the same order as they were registered.
---
Interface which allows hooks for SDK's `Span` start and end method
    invocations.

    Span processors can be registered directly using
    :func:`TracerProvider.add_span_processor` and they are invoked
    in the same order as they were registered.
## Builtins
* [BatchSpanProcessor](/docs/components/spanprocessor/batchspanprocessor/) (default)