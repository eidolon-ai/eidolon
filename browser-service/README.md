# Eidolon Browser Service
This is a playwright wrapper that allows you to run browser automation for AI Agents. It exposes a restapi to create new 
pages, execute javascript code on a page, and get the page content. It supports OpenAPI and hosts a swagger UI on /docs.

To use this service as a client pip install. There is an optional extra 'server' that includes the dependencies needed 
to run the server, keeping this library as a lightweight client.

## Running the server
```shell
docker run -p 7468:7468 eidolonai/browser_service:latest
```
