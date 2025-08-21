#!/bin/sh
set -e

until nc -z postgres_db 5432; do
  sleep 1
done

alembic upgrade head

exec python app.py