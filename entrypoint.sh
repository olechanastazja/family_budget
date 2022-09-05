#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 1
    done

    echo "PostgreSQL started"
fi

python manage.py migrate
python manage.py loadfixtures
python manage.py createsuperuser --noinput
python manage.py runserver 0.0.0.0:8002