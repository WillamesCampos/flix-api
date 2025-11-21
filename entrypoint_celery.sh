#!/bin/sh

set -e

echo "⏳Awaiting Redis at $CELERY_BROKER_URL ..."

# Extract host and port from CELERY_BROKER_URL
REDIS_HOST=$(echo $CELERY_BROKER_URL | sed -E 's|redis://([^:/]+):([0-9]+)/.*|\1|')
REDIS_PORT=$(echo $CELERY_BROKER_URL | sed -E 's|redis://([^:/]+):([0-9]+)/.*|\2|')

# Loop until Redis is ready
while ! nc -z $REDIS_HOST $REDIS_PORT; do
    echo "⏳ Redis not ready... waiting..."
    sleep 1
done

echo "✅Redis ready! Starting Celery Worker..."

# Run Celery Worker
exec celery -A app worker --loglevel=info
