#!/bin/sh

MAX_RETRIES=30
RETRY_COUNT=0

echo "Checking for PostgreSQL..."

while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  echo "Waiting for PostgreSQL at $POSTGRES_HOST:$POSTGRES_PORT..."
  sleep 1
  RETRY_COUNT=$((RETRY_COUNT+1))
  if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
    echo "Error: PostgreSQL did not start in time."
    exit 1
  fi
done

echo "PostgreSQL is available."

RETRY_COUNT=0
echo "Checking for Redis..."

while ! nc -z redis 6379; do
  echo "Waiting for Redis..."
  sleep 1
  RETRY_COUNT=$((RETRY_COUNT+1))
  if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
    echo "Error: Redis did not start in time."
    exit 1
  fi
done

echo "Redis is available."

echo "Starting Celery worker..."
exec celery -A web_project worker --loglevel=DEBUG --concurrency=4
