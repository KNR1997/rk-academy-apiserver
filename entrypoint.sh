#!/bin/sh
set -e

echo "Waiting for PostgreSQL..."

while ! nc -z $POSTGRES_HOST 5432; do
  sleep 0.5
done

echo "PostgreSQL started"

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn academy.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3
