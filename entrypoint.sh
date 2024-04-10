#!/bin/sh

#if [ "$DATABASE" = "postgres" ]
#then
#    echo "Waiting for postgres..."
#
#    while ! nc -z $SQL_HOST $SQL_PORT; do
#      sleep 0.1
#    done
#
#    echo "PostgreSQL started"
#fi
#
#python manage.py flush --no-input
#python manage.py migrate --no-input
#python manage.py check --deploy
#
#gunicorn app.wsgi:application --bind 0.0.0.0:8000

#exec "$@"

python manage.py migrate --no-input
python manage.py collectstatic --no-input

#DJANGO_SUPERUSER_PASSWORD=$SUPER_USER_PASSWORD python manage.py createsuperuser --username $SUPER_USER_NAME --email $SUPER_USER_EMAIL --noinput

gunicorn app.wsgi:application --bind 0.0.0.0:8000
