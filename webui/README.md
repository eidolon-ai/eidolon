# Eidolon Web UI

Eidolon Web UI is a powerful interface for interacting with the Eidolon project, designed to streamline your experience and enhance usability. Below you'll find concise
instructions to get your development environment set up and the server running smoothly.

## Prerequisites

Before you start, ensure you have `pnpm` installed on your system. If not, follow the installation instructions below.

### Installing PNPM

PNPM is a fast, disk space-efficient package manager. To install it, run the following command in your terminal:

```bash
npm install -g pnpm
```

Alternatively, you can check the [official PNPM installation guide](https://pnpm.io/installation) for more methods and detailed instructions.

### Running Eidolon Macnien

You will also need a running Eidolon Machine. For instructions on how to run a machine, see our [getting started guide](https://www.eidolonai.com/getting_started/quickstart/)

## Setting Up Your Environment

**Environment Configuration**:
You need to create a `.env` file in the weibui directory of the project. Copy
the contents of the 'template.env' file and paste it into the `.env` file.

```zsh
cp template.env .env
```

The content are described in the template file.
You will need to change the defaults if you would like to enable authentication or are running the eidos on
a port other than 8080.

## Running the Server

To start the development server, run:

```bash
pnpm install
pnpm run dev
```

This command will start the Eidolon Web UI on a local development server, usually accessible at `http://localhost:3000`.

Happy coding!
