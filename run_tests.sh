#!/bin/bash

# Start the Docker containers
docker compose up -d

# Wait for the PostgreSQL service to be ready
echo "Waiting for PostgreSQL to be ready..."
sleep 10

# Run the tests
pytest snews_db/tests

# Stop the Docker containers
#docker compose down -v