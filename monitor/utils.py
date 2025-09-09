import asyncio

import httpx
from django.core.mail import send_mail


def send_summary_email(results):
    """
    Отправляет общее письмо с результатами проверки сайтов
    """
    subject = " Результаты проверки сайтов"

    message_lines = []
    for res in results:
        status = "🟢 Онлайн" if res["is_online"] else "🔴 Оффлайн"
        line = (
            f"🌐 {res['url']}\n"
            f" Статус: {status}\n"
            f" Код ответа: {res['status_code']}\n"
            f" Время отклика: {res['response_time_ms']} мс\n"
        )
        message_lines.append(line)

    message = "\n\n".join(message_lines)

    send_mail(
        subject,
        message,
        from_email=None,  # использует DEFAULT_FROM_EMAIL
        recipient_list=["temka@example.com"],
    )


async def check_website(url: str, timeout=10):
    """
    Проверка сайтов
    """
    result = {
        "url": url,
        "status_code": None,
        "response_time_ms": None,
        "is_online": False,
    }

    try:
        async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
            start = asyncio.get_event_loop().time()
            response = await client.get(url)
            end = asyncio.get_event_loop().time()

            result["status_code"] = response.status_code
            result["response_time_ms"] = round((end - start) * 1000, 2)
            result["is_online"] = response.status_code < 400

    except httpx.RequestError:
        result["is_online"] = False

    return result
