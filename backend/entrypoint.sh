#!/bin/bash
set -e

echo "Starting backend on Render free..."

# Ждём Supabase Postgres (он стартует медленно)
echo "Waiting for Supabase PostgreSQL..."
for i in {1..60}; do
    if python -c "import os, psycopg2; psycopg2.connect(os.getenv('DATABASE_URL'))" 2>/dev/null; then
        echo "PostgreSQL ready!"
        break
    fi
    echo "   Still waiting... ($i/60)"
    sleep 2
done

# Если не дождались — выходим
if ! python -c "import os, psycopg2; psycopg2.connect(os.getenv('DATABASE_URL'))" >/dev/null 2>&1; then
    echo "Supabase not ready after 120s"
    exit 1
fi

echo "Running migrations..."
python manage.py migrate --noinput

echo "Creating superuser..."
python manage.py createsu || echo "Superuser already exists"

echo "Collecting static..."
python manage.py collectstatic --noinput --clear

echo "Starting Gunicorn..."
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -