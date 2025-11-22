# syntax=docker/dockerfile:1.6
FROM python:3.12-slim

# Устанавливаем системные зависимости (psycopg2)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем только то, что нужно для установки зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Делаем entrypoint исполняемым
RUN chmod +x entrypoint.sh

# Запускаем наш скрипт
CMD ["./entrypoint.sh"]