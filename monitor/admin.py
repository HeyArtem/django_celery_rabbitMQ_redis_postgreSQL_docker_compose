from django.contrib import admin, messages

from .models import Check, Website
from .tasks import run_checks


def run_checks_action(modeladmin, request, queryset):
    """
    В действиях Запустить проверку сайтов
    """
    run_checks.delay()
    messages.success(request, "Запущена проверка сайтов через Celery")


run_checks_action.short_description = "🚀 Запустить проверку всех сайтов"


@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    list_display = ("id", "url", "total_checks", "last_check", "is_online_status")

    # Кликабельность в шапке
    list_display_links = (
        "id",
        "url",
    )

    # По каким полям можно осущ-ять поиск (только CharField или TextField)
    search_fields = ("url",)

    # Сортирока порядок
    ordering = ("id",)

    # Всего проверок
    def total_checks(self, obj):
        return obj.checks.count()

    total_checks.short_description = "Проверок"

    # Последняя проверка
    def last_check(self, obj):
        last = obj.checks.order_by("-created_at").first()
        return last.created_at if last else "—"

    last_check.short_description = "Последняя проверка"

    def is_online_status(self, obj):
        last = obj.checks.order_by("-created_at").first()
        return "✅" if last and last.is_online else "❌"

    is_online_status.short_description = "Онлайн"

    # Запустить проверку выбранных сайтов
    actions = [run_checks_action]


@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    # Подписи в шапке
    list_display = (
        "id",
        "website",
        "status_code",
        "response_time_ms",
        "created_at",
        "is_online",
    )

    # Кликабельность в шапке
    list_display_links = (
        "id",
        "website",
    )

    # Справа Фильтр
    list_filter = (
        "is_online",
        "website",
    )

    # По каким полям можно осущ-ять поиск (только CharField или TextField)
    search_fields = ("website__url",)

    # Пагинация
    list_per_page = 50
