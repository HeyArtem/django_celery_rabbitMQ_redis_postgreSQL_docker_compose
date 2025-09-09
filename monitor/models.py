from django.db import models


class Website(models.Model):
    url = models.URLField(verbose_name="Адрес сайта", unique=True)

    def __str__(self):
        return self.url

    class Meta:
        db_table = "website"
        verbose_name = "Сайт"
        verbose_name_plural = "Сайты"


class Check(models.Model):
    website = models.ForeignKey(
        Website, on_delete=models.CASCADE, related_name="checks", verbose_name="Сайт"
    )
    status_code = models.IntegerField(verbose_name="Код ответа", null=True, blank=True)
    response_time_ms = models.FloatField(
        verbose_name="Время ответа (мс.)", null=True, blank=True
    )
    is_online = models.BooleanField(verbose_name="Онлайн", default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата запроса")

    def __str__(self):
        return f"{self.website} @ {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"

    class Meta:
        db_table = "check"
        verbose_name = "Результат проверки"
        verbose_name_plural = "Результаты проверок"
        ordering = ["-created_at"]
