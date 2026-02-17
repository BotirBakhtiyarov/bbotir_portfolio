#!/bin/sh

python manage.py collectstatic --noinput
python manage.py migrate --noinput

# create superuser only if not exists
python create_superuser.py

exec "$@"
