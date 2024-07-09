# k8s-operator
K8s operator for the [Eidolon project](http://www.eidolonai.com)

## Description
Three k8s operators are implemented in this project:
- **Eidolon Machine Operator**: This operator is responsible for managing the Eidolon Machine resources.
- **Eidolon Agent Operator**: This operator is responsible for managing Eidolon Agent resources.
- **Eidolon Reference Operator**: This operator is responsible for managing Eidolon Reference resources.

## Getting Started

### Prerequisites
- go version v1.20.0+
- docker version 17.03+.
- kubectl version v1.11.3+.
- Access to a Kubernetes v1.11.3+ cluster.


### Local machine development
We recommend minikube for local development.  You can find the minikube installation instructions [here](https://minikube.sigs.k8s.io/docs/start/).

We develop on a Mac, so we have the following instructions for Mac users.  If you are on a different OS, please refer to the minikube documentation.

1. Install minikube
```sh
brew install minikube
minikube start --driver qemu --network socket_vmnet  —disk 100g
alias kubectl="minikube kubectl --"   
eval $(minikube docker-env)
minikube addons enable ingress 
```

2. Install the operator-sdk
```sh
brew install operator-sdk
```

3. Install your secrets

A secret with the needed credentials for your Eidolon deployment. The name of the secret is `eidolon`.

See the [Eidolon documentation](https://www.eidolonai.com) for more information on what keys you need. 
However, typically this will be a secret with the following keys:
- `OLLAMA_URL` - the URL for your Ollama deployment if you are using ollama.
- `OPENAI_API_KEY` - your OpenAI API key if you are using OpenAI.
- `MISTRAL_API_KEY` - your Mistral API key if you are using Mistral.
- `ANTHROPIC_API_KEY` - your Anthropic API key if you are using Anthropic.

If you already have a .env file with these keys, you can create the secret with the following command:
- `kubectl create secret generic eidolon --from-env-file=<location of your env file>/.env`

### Development
If you are developing the operator, you will need to rebuild a few things if you modify the CRD or the controller.

After modifying the CRD, you will need to run the following command to update the generated code for that resource:

```sh
make generate
```

After modifying the controller, you will need to run the following command to rebuild the controller binary:

```sh
make manifests
```

### To test the operator

```sh
make test
```

### To Deploy on the cluster

**\<WARNING>**
<br/>
**WARNING:** You MUST use the minikube docker to build the Eidolon image if you are developing the SDK locally. No need to do this if you are pulling the image from a repository.
<br/>
**\</WARNING>**

```sh 

To deploy locally to the cluster you can use the following commands:

```sh
make docker-build deploy
```

**UnDeploy the controller from the cluster:**

```sh
make undeploy
```

### Run resources

Create a machine and agent resources. We have sample resources in the `config/samples` directory.
**Apply the resources in `config/samples/conversational_chatbot/resources` directory**

```sh
kubectl apply -f config/samples/conversational_chatbot/resources
```

### To build the bundle and release it

To build the bundle and release it, you can use the following commands:

```sh
make build docker-build docker-push bundle bundle-build bundle-push
```

## To build a catalog for the bundle

```sh
make catalog-build catalog-push
```
