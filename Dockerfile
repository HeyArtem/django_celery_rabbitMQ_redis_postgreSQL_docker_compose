# 1. Базовый образ с Python
FROM python:3.11-slim

# 2. Системные пакеты (pg_config для psycopg2)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# 3. Рабочая директория
WORKDIR /app

# 4. Зависимости
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 5. Код
COPY . /app

# 6. Entrypoint-скрипт
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# 7. Порт для web
EXPOSE 8000

# По умолчанию — просто покажем help
CMD ["bash", "-c", "echo 'Set command in docker-compose (web/worker/beat)' && tail -f /dev/null"]
