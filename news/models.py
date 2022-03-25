from django.db import models


class News(models.Model):
    name = models.CharField(max_length=255, verbose_name="Заголовок")
    text = models.CharField(max_length=255, verbose_name="Текст")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    expired = models.DateTimeField(verbose_name="Дата окончания новости")
    avatar = models.ImageField(blank=True, null=True, verbose_name="Аватар")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
