# Monitoring Configuration Guide

## Overview

This document provides instructions on how to configure monitoring for your application using OpenTelemetry and Jaeger. By following these steps, you will set up a local instance of Jaeger to visualize tracing data.

## Adding OpenTelemetry Reference

OpenTelemetry is enabled by default, without an exporter. So to configure monitoring, you must add an exporter to your resources. 
The following example configures the exporter to hit a locally running Jaeger instance.

```yaml
apiVersion: eidolon/v1
kind: Reference
metadata:
  name: SpanExporter
spec:
  implementation: OTLPSpanExporter
  endpoint: http://localhost:4317
  insecure: true
```

## Starting Jaeger with Docker

Run the following command in your terminal to start a Jaeger instance on your local machine:

```bash
docker run --rm --name jaeger -p 4317:4317 -p 16686:16686 jaegertracing/all-in-one:1.55
```

## Accessing Jaeger UI

After running the above command, you can access the Jaeger UI by navigating to: [http://localhost:16686](http://localhost:16686/search)

## Viewing Traces

Interact with your server as you normally would. You should see traces populated in the Jaeger UI, which allows you to monitor and analyze the behavior of your application.