from asgiref.sync import async_to_sync
from celery import shared_task

from .models import Check, Website
from .utils import check_website, send_summary_email


@shared_task
def run_checks():
    """
    Вызывает проверку сайтов.
    Вызавает отправку майла с результатами проверки
    """

    summary_results = []
    for website in Website.objects.all():
        print(f"🔍 Проверка: {website.url}")

        try:
            result = async_to_sync(check_website)(website.url)

            # Сохраняем результат в БД
            Check.objects.create(
                website=website,
                status_code=result["status_code"],
                response_time_ms=result["response_time_ms"],
                is_online=result["is_online"],
            )

            summary_results.append(result)

        except Exception as e:
            print(f"❌ Ошибка проверки {website.url}: {e}")

    send_summary_email(summary_results)
    return "✅ Проверки завершены, письмо отправлено "
