import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-key-if-empty")
DEBUG = os.getenv("DEBUG", "").lower() in ["1", "true", "yes"]
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

BASE_DIR = Path(__file__).resolve().parent.parent

# For Docker
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "heyartem.ru,www.heyartem.ru").split(
    ","
)

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "monitor.apps.MonitorConfig",
    "django_celery_beat",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Для collectstatic (стили в Docker) <— сразу после SecurityMiddleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "django_celery_rabbitmq_docker.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "django_celery_rabbitmq_docker.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE", "django.db.backends.postgresql"),
        "NAME": os.getenv("DB_NAME", ""),
        "USER": os.getenv("DB_USER", ""),
        "PASSWORD": os.getenv("DB_PASSWORD", ""),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "ru-ru"  # проблема с django-celery-beat + cron-descriptor на macOS.
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"  # Для collectstatic (стили в Docker)

# Красивая и быстрая отдача статики (стили в Docker)
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"  # пока тестируем письма будут выводиться в терминал

EMAIL_HOST = "smtp.example.com"  # заменить на реальный smtp
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# Бэкэнд для хранения результатов
# В продакшене лучше использовать что-то другое (например, Redis или базу данных),
# но для разработки FileSystemCache отлично подойдёт
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")

# Временная зона
CELERY_TIMEZONE = os.getenv("CELERY_TIMEZONE")

# Сериализация задач и результатов
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ["json"]

# Отправляем задачи в фоновом режиме
CELERY_TASK_ALWAYS_EAGER = False

# Задачи, которые должны автоматически импортироваться
CELERY_IMPORTS = ("monitor.tasks",)


# settings.py
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers.DatabaseScheduler"

# проблема с django-celery-beat + cron-descriptor на macOS (Раздел Crontabs в админке).
os.environ["LANG"] = "en_US.UTF-8"
os.environ["LC_ALL"] = "en_US.UTF-8"


# # Celery Beat — это планировщик задач, для периодических задач `каждый день`, `каждый час`
# CELERY_BEAT_SCHEDULE = {
#     'run-site-checks-every-10-minutes': {
#         'task': 'monitor.tasks.run_checks',
#         'schedule': crontab(minute='*/10'),  # каждые 10 минут
#     },
# }

# CSRF_TRUSTED_ORIGINS (для админки по http)
CSRF_TRUSTED_ORIGINS = [
    "https://heyartem.ru",
    "https://www.heyartem.ru",
]

# За прокси: говорить Django, что HTTPS пришёл через X-Forwarded-Proto
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True

# (Рекомендовано в проде)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
