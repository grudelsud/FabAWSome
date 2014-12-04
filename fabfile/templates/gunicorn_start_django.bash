#!/bin/bash
# Starts the Gunicorn server
set -e

# Activate the virtualenv for this project
%(ACTIVATE)s

# Start gunicorn
exec gunicorn --log-file=- \
  --env DJANGO_SETTINGS_MODULE='%(DJANGO_SETTINGS_MODULE)s' \
  %(DJANGO_PROJECT_NAME)s.wsgi:application \
  -c %(WSGI_PROJECT_BASE_DIR)s/gunicorn.conf.py
