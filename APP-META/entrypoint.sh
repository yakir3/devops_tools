#!/bin/bash
if [ "$1" = 'test' ];then
  exec sleep infinity
elif [ "$1" = 'runserver' ];then
  # exec python manage.py runserver 0.0.0.0:${EXPOSE_PORT}

  # python manage.py collectstatic --noinput && \
  mkdir logs && \
  python manage.py makemigrations && \
  python manage.py migrate && \
  uwsgi --ini uwsgi.ini && \
  tail -f logs/uwsgi.log
fi

exec "$@"