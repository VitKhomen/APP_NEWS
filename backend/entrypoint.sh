#!/bin/bash
set -e

echo "🚀 Starting Render entrypoint script..."

# Ждём, пока база станет доступна (важно на Render)
python << END
import time
import os
from urllib.parse import urlparse
import psycopg2

db_url = os.getenv("DATABASE_URL")
if db_url and db_url.startswith("postgres"):
    parsed = urlparse(db_url)
    print("⏳ Waiting for PostgreSQL to be ready...")
    for _ in range(30):
        try:
            psycopg2.connect(
                host=parsed.hostname,
                port=parsed.port,
                user=parsed.username,
                password=parsed.password,
                dbname=parsed.path[1:]
            )
            print("✅ Database is ready!")
            break
        except Exception as e:
            print("   ⏳ Still waiting... (30 sec max)")
            time.sleep(1)
    else:
        print("❌ Database not ready in 30s")
        exit(1)
END

echo "📦 Applying migrations..."
python manage.py migrate --noinput

echo "👤 Creating superuser (if not exists)..."
python manage.py createsu || echo "Superuser already exists or failed (non-critical)"

echo "🗂️  Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "🌍 Starting Gunicorn on 0.0.0.0:\$PORT ..."
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --log-level=info \
    --access-logfile - \
    --error-logfile -