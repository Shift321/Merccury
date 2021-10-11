from django.contrib import admin

from .models import Contest


class ContestAdmin(admin.ModelAdmin):
    def date_expired(self, obj):
        date = obj.expired_date
        return date.strftime("%d %b, %Y")

    date_expired.short_description = "Дата окончания конкурса"

    def name(self, obj):
        return obj.name

    def price(self, obj):
        return obj.price

    list_display = ["date_expired", "name", "price"]


admin.site.register(Contest, ContestAdmin)
