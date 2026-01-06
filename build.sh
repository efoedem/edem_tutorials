#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate
# This will create a superuser automatically if it doesn't exist
python manage.py createsuperuser --noinput || true