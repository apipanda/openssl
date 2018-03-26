#!/bin/bash

# Check if rabbit and redis are up and running before starting the service.
until nc -z ${REDIS_URL}; do
    echo "$(date) - waiting for redis..."
    sleep 1
done

# Start Supervisor, with Nginx and uWSGI
/usr/bin/supervisord