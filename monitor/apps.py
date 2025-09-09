from django.apps import AppConfig
from django.db.models.signals import post_migrate


def create_periodic_task(sender, **kwargs):
    # Импорты здесь, чтобы таблицы точно были после миграций
    from django_celery_beat.models import IntervalSchedule, PeriodicTask

    """
    При первом запуске Django, сразу создается задача
    в админке Celery Beat (не нужно руками добавлять её)
    """

    schedule, _ = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.HOURS,  # раз в час
    )

    PeriodicTask.objects.get_or_create(
        interval=schedule,
        name="Запуск проверки сайтов",
        task="monitor.tasks.run_checks",
    )


class MonitorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "monitor"

    def ready(self):
        # Привязываем создание задачи к моменту "после миграций"
        post_migrate.connect(create_periodic_task, sender=self)
