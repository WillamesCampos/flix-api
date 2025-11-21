#!/bin/sh

set -e

echo "⏳ Awaiting Postgres..."
while ! nc -z "$POSTGRES_HOST" 5432; do
  sleep 1
done
echo "✅ Postgres ready!"

echo "⏳ Awaiting Redis..."
while ! nc -z redis 6379; do
  sleep 1
done
echo "✅ Redis ready! Starting migrations..."

echo "🛠️ Running migrations..."
python manage.py migrate --noinput

echo "🚀 Starting Django server..."
python manage.py runserver 0.0.0.0:8000
