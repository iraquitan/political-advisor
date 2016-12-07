#!/bin/sh

/usr/local/bin/python manage.py collectstatic --noinput
/usr/local/bin/gunicorn mainsite.wsgi:application -w 2 -b :8000
