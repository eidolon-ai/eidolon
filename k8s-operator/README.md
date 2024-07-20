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
- Access to a Kubernetes v1.11.3+ cluster.
- OLM.  The instructions for our operator on operatorhub.io will install OLM for you.
 
### Installation
*TODO* - once we are accepted on operatorhub.io

### Local machine deployment
We recommend minikube for local development.  You can find the minikube installation instructions [here](https://minikube.sigs.k8s.io/docs/start/).

We develop on a Mac, so we have the following instructions for Mac users.  If you are on a different OS, please refer to the minikube documentation.

* Install minikube
    ```sh
    brew install minikube
    minikube start --driver qemu --network socket_vmnet  —disk 100g
    alias kubectl="minikube kubectl --"   
    eval $(minikube docker-env)
    ```

* Install your secrets

    A secret with the needed credentials for your Eidolon deployment. The name of the secret is `eidolon`.

    See the [Eidolon documentation](https://www.eidolonai.com) for more information on what keys you need. 
    However, typically this will be a secret with the following keys:
    - `OLLAMA_URL` - the URL for your Ollama deployment if you are using ollama.
    - `OPENAI_API_KEY` - your OpenAI API key if you are using OpenAI.
    - `MISTRAL_API_KEY` - your Mistral API key if you are using Mistral.
    - `ANTHROPIC_API_KEY` - your Anthropic API key if you are using Anthropic.

    If you already have a .env file with these keys, you can create the secret with the following command:
    ```sh
    kubectl create secret generic eidolon --from-env-file=<location of your env file>/.env
    ```

    ⚠️ To use the secret in your deployment, you need to add the following to your deployment yaml file's `spec`:
    ```yaml
    envFrom:
      - secretRef:
          name: eidolon
    ```

* Install the eidolon operator
    ```sh
    helm repo add eidolon-operator https://eidolonai.com/charts 
    helm install eidolon-operator eidolon-operator/eidolon-operator-chart --namespace eidolon-operator-system --create-namespace
    ```

    If you already have added the repo and you want to update it:
    ```sh
    helm repo update
    helm uninstall eidolon-operator -n eidolon-operator-system                  
    helm install eidolon-operator eidolon-operator/eidolon-operator-chart --namespace eidolon-operator-system --create-namespace
    ```

### Development
Now you can deploy your resources in your k8s cluster. To apply your machine resource:
```sh
kubectl apply -f <your machine location>.<your machine>.yaml
```
Just like any other k8s resource, you can apply the machine to any namespace. Use the -n flag on kubectl to specify the namespace.

**NOTE: Only one machine can run per namespace**

Now you can apply your agent resource:
```sh
kubectl apply -f <your agent location>.<your agent>.yaml
```

Make sure to apply the agent to the same namespace as the machine.

### Exposing a machine locally
There are many ways to expose a minikube service locally. 
One way is to create a load balancer service which will then be exposed on your local computer. 

To create a load balancer service for the eidolon server:
```sh
kubectl expose deployment eidolon-deployment --type=LoadBalancer --name=eidolon-server --port 8080
```

To get the IP address of the eidolon server service:
```sh
minikube service eidolon-server --url
```

You can use this URL to access your eidolon server.

### Running the web UI
To start the webui, you can use the following command:
```sh
kubectl apply -f config/samples/webui.yaml
```

To expose the webui service we need to create a load balancer service, get the URL, and update the nextjs config map with the URL.:
```sh
# Get the URL from minikube
API_URL=$(minikube service eidolon-webui --url)

# Update the ConfigMap
kubectl create configmap eidolon-webui-config --from-literal=NEXT_PUBLIC_API_URL=$API_URL -o yaml --dry-run=client | kubectl apply -f -

# Restart the deployment to pick up the new ConfigMap value
kubectl rollout restart deployment eidolon-webui-deployment

echo "Web UI is available at $API_URL"
```
