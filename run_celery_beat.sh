#!/bin/sh

cd "$(dirname "$0")"

. .env/bin/activate

exec ./manage.py celery beat

