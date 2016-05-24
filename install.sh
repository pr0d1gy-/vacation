#!/bin/sh

. .env/bin/activate

pip install -q -r requirements.txt

./manage.py migrate
./manage.py collectstatic --noinput

exit 0
