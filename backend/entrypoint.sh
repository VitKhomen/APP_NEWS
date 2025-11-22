sh#!/bin/sh
set -e

echo "Waiting for PostgreSQL to be ready (max 300 sec)..."

# Ждём пока база не ответит
timeout=300
counter=0
until python <<EOF
import sys
import os
from urllib.parse import urlparse
import psycopg2
from django.db import connection

# Попытка простого подключения через psycopg2
try:
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        print("DATABASE_URL not set")
        sys.exit(1)
    parsed = urlparse(db_url)
    conn = psycopg2.connect(
        host=parsed.hostname,
        port=parsed.port or 5432,
        user=parsed.username,
        password=parsed.password,
        database=parsed.path[1:] or 'postgres',
        connect_timeout=5
    )
    conn.close()
    print("PostgreSQL is ready!")
    sys.exit(0)
except Exception as e:
    print("Still waiting for PostgreSQL... (error: %s)" % e)
    sys.exit(1)
EOF
do
    if [ $counter -ge $timeout ]; then
        echo "Database not ready after ${timeout}s. Giving up."
        exit 1
    fi
    counter=$((counter + 3))
    sleep 3
done

echo "Running migrations..."
python manage.py migrate --noinput

echo "Creating superuser (if not exists)..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser(
        username='admin',
        email=os.getenv('ADMIN_EMAIL', 'admin@example.com'),
        password=os.getenv('ADMIN_PASSWORD', 'admin123')
    )
    print("Superuser created")
else:
    print("Superuser already exists")
EOF

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Starting Gunicorn..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120