from django.contrib import admin


from .models import BlackList, User


class UserAdmin(admin.ModelAdmin):
    search_fields = ["id", "username", "second_name"]

    def id(self, obj):
        return [obj.id]

    def username(self, obj):
        return [obj.username]

    def email(self, obj):
        return obj.email

    def date_of_registration(self, obj):
        return obj.date_of_registration

    def phone_number(self, obj):
        return obj.phone_number

    def sponsor(self, obj):
        id_of_ivited = obj.id_of_invited
        sponsor = User.objects.get(id=id_of_ivited)
        return f"{sponsor.second_name} {sponsor.name} {sponsor.patronymic}"

    sponsor.short_description = "Спонсор"

    def user(self, obj):
        return f"{obj.second_name} {obj.name} {obj.patronymic}"

    user.short_description = "Контрагент"

    def date_of_activate(self, obj):
        return obj.date_of_activate

    list_display = [
        "id",
        "username",
        "email",
        "date_of_registration",
        "phone_number",
        "sponsor",
        "user",
        "date_of_activate",
    ]


admin.site.register(User, UserAdmin)
admin.site.register(BlackList)
