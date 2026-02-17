#!/bin/sh

python manage.py collectstatic --noinput
python manage.py migrate --noinput

# create superuser only if not exists
python manage.py shell -c "
from django.contrib.auth import get_user_model;
import os;
User=get_user_model();
u=os.environ.get('DJANGO_SUPERUSER_USERNAME');
p=os.environ.get('DJANGO_SUPERUSER_PASSWORD');
e=os.environ.get('DJANGO_SUPERUSER_EMAIL');
if u and p and not User.objects.filter(username=u).exists():
    User.objects.create_superuser(u,e,p)
"
exec "$@"
