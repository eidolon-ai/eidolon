# Monitoring Configuration Guide

## Overview

This document provides instructions on how to configure monitoring for your application using OpenTelemetry and Jaeger. By following these steps, you will set up a local instance of Jaeger to visualize tracing data.

## Adding OpenTelemetry Reference

To configure the monitoring, you must first add an OpenTelemetry reference to set the default `OpenTelemetryManager`. This step ensures that the telemetry data is collected and managed properly.

```yaml
apiVersion: eidolon/v1
kind: Reference
metadata:
  name: LifecycleManager
spec: OpenTelemetryManager
```

## Starting Jaeger with Docker

Run the following command in your terminal to start a Jaeger instance on your local machine:

```bash
docker run --rm --name jaeger \
  -e COLLECTOR_ZIPKIN_HOST_PORT=:9411 \
  -p 6831:6831/udp \
  -p 6832:6832/udp \
  -p 5778:5778 \
  -p 16686:16686 \
  -p 4317:4317 \
  -p 4318:4318 \
  -p 14250:14250 \
  -p 14268:14268 \
  -p 14269:14269 \
  -p 9411:9411 \
  jaegertracing/all-in-one:1.55
```

## Accessing Jaeger UI

After running the above command, you can access the Jaeger UI by navigating to: [http://localhost:16686](http://localhost:16686/search)

## Viewing Traces

Interact with your server as you normally would. You should see traces populated in the Jaeger UI, which allows you to monitor and analyze the behavior of your application.