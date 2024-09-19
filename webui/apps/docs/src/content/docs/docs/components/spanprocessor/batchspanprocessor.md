---
title: BatchSpanProcessor
description: "Description of BatchSpanProcessor component"
---

**Description:** Batch span processor implementation.

    `BatchSpanProcessor` is an implementation of `SpanProcessor` that
    batches ended spans and pushes them to the configured `SpanExporter`.

    `BatchSpanProcessor` is configurable with the following environment
    variables which correspond to constructor parameters:

    - :envvar:`OTEL_BSP_SCHEDULE_DELAY`
    - :envvar:`OTEL_BSP_MAX_QUEUE_SIZE`
    - :envvar:`OTEL_BSP_MAX_EXPORT_BATCH_SIZE`
    - :envvar:`OTEL_BSP_EXPORT_TIMEOUT`

| Property                             | Pattern | Type  | Deprecated | Definition | Title/Description  |
| ------------------------------------ | ------- | ----- | ---------- | ---------- | ------------------ |
| + [implementation](#implementation ) | No      | const | No         | -          | BatchSpanProcessor |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | Yes     |

**Description:** BatchSpanProcessor

Specific value: `"BatchSpanProcessor"`

----------------------------------------------------------------------------------------------------------------------------
