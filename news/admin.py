from django.contrib import admin
from .models import News


class NewsAdmin(admin.ModelAdmin):
    def date_expired(self, obj):
        date = obj.expired
        return date.strftime("%d %b, %Y")

    date_expired.short_description = "Дата окончания новости"

    def name(self, obj):
        return obj.name

    def date_of_create(self, obj):
        date = obj.created_at
        return date.strftime("%d %b, %Y")

    date_of_create.short_description = "Дата создания новости"

    list_display = ["date_expired", "name", "date_of_create"]


admin.site.register(News, NewsAdmin)
