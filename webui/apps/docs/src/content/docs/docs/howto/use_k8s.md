---
title: Deploy Eidolon AI with Kubernetes
description: Learn how to deploy and manage Eidolon AI in a Kubernetes environment
---

Running Eidolon AI on Kubernetes unlocks powerful deployment and scaling capabilities. This guide walks you through setting up Eidolon AI in your Kubernetes cluster.

## Prerequisites

- A running Kubernetes cluster and `kubectl` CLI ([Get started with Minikube][minikube])
- Basic familiarity with [Eidolon AI](https://www.eidolonai.com/docs/)

## Quick Setup

1. Clone the quickstart repo:
   ```bash
   git clone git@github.com:eidolon-ai/eidolon-quickstart.git
   ```

2. Create a namespace (optional for Make users):
   ```bash
   kubectl create namespace eidolon-quickstart
   ```

3. Set up API access tokens using Kubernetes secrets:
   ```bash
   # Option 1: From .env file
   kubectl create secret generic eidolon --from-env-file=.env

   # Option 2: Direct configuration
   kubectl create secret generic eidolon \
     --from-literal=OLLAMA_URL=https://ollama.example.com \
     --from-literal=OPENAI_API_KEY=your-openai-api-key \
     --from-literal=MISTRAL_API_KEY=your-mistral-api-key \
     --from-literal=ANTHROPIC_API_KEY=your-anthropic-api-key
   ```
   Add `-n eidolon-quickstart` if using a custom namespace.

## Eidolon Kubernetes Operators

Eidolon uses three Kubernetes operators to manage its components:

- **Machine Operator**: Manages core Eidolon infrastructure
- **Agent Operator**: Handles AI agent lifecycle
- **Reference Operator**: Controls resource references

To use your secrets in deployments, add this to your deployment YAML:
```yaml
envFrom:
  - secretRef:
      name: eidolon
```

## Installation

Choose **either** the Make-based or Helm-based installation method:

### Option 1: Using Make (Simplified Setup)

Make handles everything in the default namespace and is great for getting started quickly:

```bash
# Install operator and dependencies
make k8s-operator

# Build and deploy your application
make docker-build
make k8s-serve
```

### Option 2: Using Helm (Advanced Setup)

Helm installation gives you more control over namespaces and configuration:

1. Install the Eidolon operator:
   ```bash
   helm repo add eidolon-operator https://eidolonai.com/charts 
   helm install eidolon eidolon-operator/eidolon-operator-chart \
     --namespace eidolon-operator-system --create-namespace
   ```

2. Build your application container (if using the quickstart):
   ```bash
   docker build -t eidolon-quickstart .
   ```

3. Deploy the application components:
   ```bash
   kubectl create namespace eidolon-quickstart
   cd eidolon-quickstart
   kubectl apply -f resources/machine.eidolon.yaml -n eidolon-quickstart
   kubectl apply -f resources/hello_world_agent.eidolon.yaml -n eidolon-quickstart
   ```

## Verify Your Deployment

1. Check pod status:
   ```bash
   kubectl get pods -n eidolon-quickstart
   ```

2. Test the endpoint:
   ```bash
   kubectl exec -it <pod-name> -- /bin/bash
   curl localhost:8080/health  # Replace with actual endpoint
   ```

## Cleanup

Use the cleanup method that matches your installation path:

### Make Installation Cleanup

If you installed using Make:
```bash
make k8s-clean
```

### Helm Installation Cleanup

If you installed using Helm:
```bash
# Remove application components
kubectl delete -f resources/hello_world_agent.eidolon.yaml -n eidolon-quickstart
kubectl delete -f resources/machine.eidolon.yaml -n eidolon-quickstart

# Remove the operator
helm uninstall eidolon --namespace eidolon-operator-system

# Optional: Remove the namespace
kubectl delete namespace eidolon-quickstart
```

[minikube]: https://kubernetes.io/docs/tutorials/hello-minikube/
[k8sop]: https://kubernetes.io/docs/concepts/extend-kubernetes/operator/
[k8ssecrets]: https://kubernetes.io/docs/concepts/configuration/secret/
[eqs]: https://github.com/eidolon-ai/eidolon-quickstart
