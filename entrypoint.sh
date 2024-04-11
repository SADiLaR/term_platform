#!/bin/sh
set -e
set -o pipefail
set -x

python manage.py migrate --no-input
python manage.py collectstatic --no-input

gunicorn app.wsgi:application --bind 0.0.0.0:8000
