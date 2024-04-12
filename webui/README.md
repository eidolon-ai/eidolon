# Eidolon Web UI

Eidolon Web UI is a powerful interface for interacting with the Eidolon project, designed to streamline your experience and enhance usability. Below you'll find concise
instructions to get your development environment set up and the server running smoothly.

## Running With Docker
If you are looking to get started quickly, we publish an image that you can use without needing to set a development environment.

We need to e
### mac
```bash
docker run -e "EIDOLON_SERVER=http://host.docker.internal:8080" -p 3000:3000 eidolonai/webui:latest
```
### linux
```bash
docker run --net=host eidolonai/webui:latest
```

🚨 Make sure you have an Eidolon machine running locally on port 8080. For instructions on how to run a machine, see our [getting started guide](https://www.eidolonai.com/docs/introduction/)

## Development Environment

### Installing PNPM

PNPM is a fast, disk space-efficient package manager. To install it, run the following command in your terminal:

```bash
npm install -g pnpm
```

Alternatively, you can check the [official PNPM installation guide](https://pnpm.io/installation) for more methods and detailed instructions.

### Installing Turbo Reop

Turbo Repo is a tool that helps you manage multiple repositories. To install it, run the following command in your terminal:

```bash
pnpm install turbo --global
```

Alternatively, you can check the [official Turbo Repo installation guide](https://turbo.build/repo) for more methods and detailed instructions.

### Running Eidolon Machine

You will also need a running Eidolon Machine. For instructions on how to run a machine, see our [getting started guide](https://www.eidolonai.com/docs/introduction/)

### Setting Up Your Environment

**Environment Configuration**:
You need to create a `.env` file in the **webui/app/eidolon-ui2** directory of the project. Copy
the contents of the 'template.env' file and paste it into the `.env` file.

The content are described in the template file.
You will need to change the defaults if you would like to enable authentication or are running the eidos on
a port other than 8080.

### Running the Server

To start the development server, run:

```bash
pnpm install
turbo run dev
```

This command will start the Eidolon Web UI on a local development server, usually accessible at [http://localhost:3000](http://localhost:3000).

Happy coding!
