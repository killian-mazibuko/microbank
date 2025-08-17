#!/bin/sh
set -e

echo "Applying database migrations..."
python manage.py makemigrations users
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting server..."
exec "$@"
