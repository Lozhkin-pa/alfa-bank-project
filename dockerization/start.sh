#!/bin/bash

python manage.py migrate
python manage.py create_mock_users
python manage.py collectstatic --noinput
gunicorn --workers=2 ipr.wsgi:application --bind 0.0.0.0:8000