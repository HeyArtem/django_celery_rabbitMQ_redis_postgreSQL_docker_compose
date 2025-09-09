#!/usr/bin/env bash
set -e

# Ждём Postgres
echo "⏳ Waiting for Postgres at ${DB_HOST}:${DB_PORT} ..."
until nc -z ${DB_HOST} ${DB_PORT}; do
  sleep 1
done
echo "✅ Postgres is up."

# Применяем миграции
echo "🚀 Running migrations..."

python manage.py migrate --noinput
  #  Для collectstatic (стили в Docker)
  echo "📦 Collect static..."
  python manage.py collectstatic --noinput


# Создаем суперюзера, если нужно (один раз)
if [ "$CREATE_SUPERUSER" = "1" ]; then
  echo "👑 Creating superuser (if not exists)..."
  python - <<'PYCODE'
import os
from django.contrib.auth import get_user_model
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_celery_rabbitmq_docker.settings')
django.setup()
User = get_user_model()
u, created = User.objects.get_or_create(username='admin')
if created:
    u.set_password('admin')
    u.is_superuser = True
    u.is_staff = True
    u.save()
    print("Superuser created: admin / admin")
else:
    print("Superuser exists")
PYCODE
fi

echo "➡️ Exec: $@"
exec "$@"
