---
title: How to use with k8s
description: References - How can I use Eidolon AI with Kubernetes?
---

Eidolon AI is an amazing product that is easily integrated with any infrastructure. Kubernetes is a popular choice for deploying and managing containerized applications. This guide will show you how to use Eidolon AI with Kubernetes.

## Prerequisites

* The expectation is you have a local Kubernetes cluster running and are familiar with kubectl (the Kubernetes CLI). To help you get started please check out [this link][minikube]
* You have a basic familiarity with the Eidolon AI platform. If not, please check out the [Eidolon AI documentation](https://www.eidolonai.com/docs/)

### Get the sample project

1. Start off by deciding on an Eidolon example application. For this example we will be using the [eidolon quickstart][eqs] application.
2. Clone the example repo from `git clone git@github.com:eidolon-ai/eidolon-quickstart.git`

### Create a Namespace

If you are using Make you can skip this step, however, if you are using the Helm instructions you will probably want to use a namespace.

`kubectl create namespace eidolon-quickstart`

### Install Secrets

To access things like the OpenAI apis you will need to have access tokens. These access tokens will be stored using [Kubernetes secrets][k8ssecrets]. 
The name of the secret needs to be `eidolon`.

You can either install via an existing env file...

```sh
kubectl create secret generic eidolon --from-env-file=<location of your env file>/.env
```

or using an explicit command...

```sh
kubectl create secret generic eidolon \
  --from-literal=OLLAMA_URL=https://ollama.example.com \
  --from-literal=OPENAI_API_KEY=your-openai-api-key \
  --from-literal=MISTRAL_API_KEY=your-mistral-api-key \
  --from-literal=ANTHROPIC_API_KEY=your-anthropic-api-key
```

if you are using a namespace like the one recommended in the above section add `-n eidolon-quickstart`.

## Understand the Eidolon AI Operators

Eidolon uses the [Kubernetes Operator pattern][k8sop] to manage the lifecycle of the AI components. The operator is responsible for managing the Eidolon Reference resources.

There are 3 main operators that you need to be aware of:

- **Eidolon Machine Operator**: This operator is responsible for managing the Eidolon Machine resources.
- **Eidolon Agent Operator**: This operator is responsible for managing Eidolon Agent resources.
- **Eidolon Reference Operator**: This operator is responsible for managing Eidolon Reference resources.

With these operators, you can easily manage the lifecycle of the Eidolon AI components.

To use the secret in your deployment, you need to add the following to your deployment yaml file's `spec`:

    ```yaml
    envFrom:
      - secretRef:
          name: eidolon
    ```

## Getting Started

### Install The Operator

#### Using make

*Note: The main limitation of Make is everything will be installed in the default namespace.*

To install the operator using the makefile available in the [eidolon quickstart][eqs] run `make k8s-operator` from the root directory of the project. Once completed you should see 

    ```
    K8s environment is ready. You can now deploy your application.
    ```

#### New Installation

```sh
    helm repo add eidolon-operator https://eidolonai.com/charts 
    helm install eidolon eidolon-operator/eidolon-operator-chart --namespace eidolon-operator-system --create-namespace
```

*Remove and start over* 

If you already have added the repo, and you want to update it:

```sh
    helm uninstall eidolon --namespace eidolon-operator-system                  
```

if using Make the command is 

```shell
    helm uninstall eidolon
```
## Sample Deployment

### Make Deployment

Run all commands from the root of the [eidolon quickstart][eqs]

1. Run `make docker-build` to install the new container image.
2. Run `make k8s-serve` to deploy the same image to the Kubernetes cluster.

### Manual Deployment

1. Create the namespace `eidolon` in your Kubernetes cluster with `kubectl create namespace eidolon`
2. Enter the resources folder `cd eidolon-quickstart`
3. Create the machine with `kubectl apply -f resources/machine.eidolon.yaml -n eidolon-quickstart`
4. Create the agent with `kubectl apply -f resources/hello_world_agent.eidolon.yaml -n eidolon-quickstart`
5. Now make sure the agent is running `kubectl get pods -n eidolon-quickstart`

## Checking that it works 

1. First check that the pod is working with `kubectl get pods` make sure to add `-n eidolon-quickstart` if you are using the namespace.
2. If everything is good the next step is to `kubectl exec -it container-name -- /bin/bash` to get into the container.
   1. Once in you should be able to test the endpoint with `curl TODO`

## Cleaning up

To remove the resources from your Kubernetes cluster, you can run the following commands:

### Make 

```sh
make k8s-clean
```

### Kubectl
  
```sh
kubectl delete -f resources/hello_world_agent.eidolon.yaml -n eidolon-quickstart
kubectl delete -f resources/machine.eidolon.yaml -n eidolon-quickstart
```

[minikube]: https://kubernetes.io/docs/tutorials/hello-minikube/
[k8sop]: https://kubernetes.io/docs/concepts/extend-kubernetes/operator/
[k8ssecrets]: https://kubernetes.io/docs/concepts/configuration/secret/
[eqs]: https://github.com/eidolon-ai/eidolon-quickstar
