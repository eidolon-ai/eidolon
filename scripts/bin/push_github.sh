#!/bin/bash

# Check if all required arguments are provided
if [ $# -ne 4 ]; then
  echo "Usage: $0 <repo> <access_token> <api_key> <project_key>"
  exit 1
fi

# Variables
REPO="$1"
ACCESS_TOKEN="$2"
API_KEY="$3"
PROJECT_KEY="$4"

# Run the commands
poetry run push_stats --repo $REPO --access-token $ACCESS_TOKEN --api-key $API_KEY --project-key $PROJECT_KEY
poetry run push_gh_stars --repo $REPO --access-token $ACCESS_TOKEN --api-key $API_KEY --project-key $PROJECT_KEY
poetry run push_gh_forks --repo $REPO --access-token $ACCESS_TOKEN --api-key $API_KEY --project-key $PROJECT_KEY
