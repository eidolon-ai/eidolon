#!/bin/bash

# Check if the repository name is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <repo>"
  exit 1
fi

# Variables
REPO="$1"
ACCESS_TOKEN="${{ secrets.GH_PAT }}"
API_KEY="${{ secrets.POSTHOG_API_KEY }}"
PROJECT_KEY="${{ secrets.POSTHOG_PROJECT_KEY }}"

# Run the commands
poetry run push_stats --repo $REPO --access-token $ACCESS_TOKEN --api-key $API_KEY --project-key $PROJECT_KEY
poetry run push_gh_stars --repo $REPO --access-token $ACCESS_TOKEN --api-key $API_KEY --project-key $PROJECT_KEY
poetry run push_gh_forks --repo $REPO --access-token $ACCESS_TOKEN --api-key $API_KEY --project-key $PROJECT_KEY
