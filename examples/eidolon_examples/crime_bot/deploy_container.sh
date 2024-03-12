#!/bin/bash

# Load environment variables from .env file
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | awk '/=/ {print $1}')
else
    echo ".env file not found"
    exit 1
fi

# Now, use the environment variables in the az container create command

echo $CRIME_SQL_CONNECTION_STRING

az container create \
  --resource-group crime \
  --name $1 \
  --image harimasoor/my-backend-server-external-mongo37 \
  --dns-name-label $1 \
  --ports 443 \
  --environment-variables \
    MONGO_CONNECTION_STRING="" \
    OPENAI_API_KEY=$OPENAI_API_KEY \
    MONGO_DB_NAME=$MONGO_DB_NAME \
    CRIME_SQL_CONNECTION_STRING="" \
  --assign-identity
