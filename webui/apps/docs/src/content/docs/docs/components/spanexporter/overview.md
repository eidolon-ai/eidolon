---
title: SpanExporter Overview
description: "Interface for exporting spans.

    Interface to be implemented by services that want to export spans recorded
    in their own format.

    To export data this MUST be registered to the :class`opentelemetry.sdk.trace.Tracer` using a
    `SimpleSpanProcessor` or a `BatchSpanProcessor`."
---
Interface for exporting spans.

    Interface to be implemented by services that want to export spans recorded
    in their own format.

    To export data this MUST be registered to the :class`opentelemetry.sdk.trace.Tracer` using a
    `SimpleSpanProcessor` or a `BatchSpanProcessor`.
## Builtins
* [NoopSpanExporter](/docs/components/spanexporter/noopspanexporter/) (default)
* [OTLPSpanExporter](/docs/components/spanexporter/otlpspanexporter/)