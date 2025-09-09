import os

from celery import Celery

# Устанавливаем переменную окружения для настроек Django
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "django_celery_rabbitmq_docker.settings"
)

# Создаём экземпляр приложения Celery
app = Celery("django_celery_rabbitmq_docker")

# Загружаем настройки из файла Django settings.py
app.config_from_object("django.conf:settings", namespace="CELERY")

# Автоматически находим и регистрируем задачи в приложениях
app.autodiscover_tasks()

app.conf.timezone = "Europe/Moscow"
app.conf.enable_utc = False


# Эта функция полезна для отладки
@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
