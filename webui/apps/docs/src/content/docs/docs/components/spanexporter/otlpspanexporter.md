---
title: OTLPSpanExporter
description: "Description of OTLPSpanExporter component"
---

**Description:** OTLP span exporter

    Args:
        endpoint: OpenTelemetry Collector receiver endpoint
        insecure: Connection type
        credentials: Credentials object for server authentication
        headers: Headers to send when exporting
        timeout: Backend request timeout in seconds
        compression: gRPC compression method to use

| Property                             | Pattern | Type  | Deprecated | Definition | Title/Description |
| ------------------------------------ | ------- | ----- | ---------- | ---------- | ----------------- |
| - [implementation](#implementation ) | No      | const | No         | -          | OTLPSpanExporter  |

## <a name="implementation"></a>1. Property `implementation`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

**Description:** OTLPSpanExporter

Specific value: `"OTLPSpanExporter"`

----------------------------------------------------------------------------------------------------------------------------
