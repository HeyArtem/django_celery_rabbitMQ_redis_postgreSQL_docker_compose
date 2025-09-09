import os

from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

load_dotenv()
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "django_celery_rabbitmq_docker.settings"
)
application = get_wsgi_application()
