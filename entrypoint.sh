#!/bin/sh

python manage.py migrate
python manage.py loadfixtures
python manage.py createsuperuser --noinput
python manage.py runserver 0.0.0.0:8002