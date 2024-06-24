#!/bin/bash

set -e
set -o pipefail
set -x

python manage.py check --deploy --database default
python manage.py migrate --no-input
python manage.py collectstatic --no-input
python manage.py compilemessages

gunicorn app.wsgi:application --bind 0.0.0.0:8000 --config gunicorn.conf.py
