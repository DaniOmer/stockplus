#!/bin/sh

# Execute migrations
echo "Applying database migrations"
python3 manage.py migrate --noinput

# Collect static files
echo "Collecting static files"
python3 manage.py collectstatic --noinput

# Start gunicorn
echo "Starting Gunicorn"
exec gunicorn configuration.wsgi:application --bind 0.0.0.0:8000
