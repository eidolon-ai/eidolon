# Project Setup

## Frontend
1. Navigate to the `webui` directory.
2. Run `pnpm install` to install the dependencies.
3. Run `pnpm run start` to get the frontend working.

## Backend
1. Run `poetry shell` to get a new shell for the backend.
2. Run `poetry install` to install the backend dependencies.
3. Run `poetry run eidolon-server resources/ -m local_dev` to start the backend server.

## Configuration
1. Replace the contents of the `sample.env` file with the actual API Keys.

## Technologies Used
- Stripe
- Google Auth
- MySQL Azure DB
- SQL Azure DB
- OpenAI

## Deployment
### Server
1. Use the `Dockerfile.crime_bot` file to build the server Docker image.
2. Use the `crimebot.yml` file in `.github/workflows` to deploy the server.

### WebUI
1. Use the `deploy_container.sh` script to deploy the WebUI container to an Azure Container Instance.



