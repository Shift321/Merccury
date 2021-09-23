from django.contrib import admin


from .models import User


class UserAdmin(admin.ModelAdmin):
    search_fields = ["id", "username", "second_name"]

    # def user_status(self, obj):
    #     if obj.is_blocked() == "True":
    #         return (
    #             '<div style="width:100%%; height:100%%; background-color:red;">%s</div>'
    #             % obj.status()
    #         )
    #     return obj.is_blocked()

    # user_status.allow_tags = True
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

    phone_number.allow_tags = True

    def sponsor(self, obj):
        id_of_ivited = obj.id_of_invited
        sponsor = User.objects.get(id=id_of_ivited)
        return f"{sponsor.second_name} {sponsor.name} {sponsor.patronymic}"

    list_display = [
        "id",
        "username",
        "email",
        "date_of_registration",
        "phone_number",
        "sponsor",
    ]


admin.site.register(User, UserAdmin)
