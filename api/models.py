import jwt

from datetime import datetime
from datetime import timedelta

from django.db import models
from django.conf import settings
from django.db import models
from django.core import validators
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.contrib.auth.models import PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField

VERIFICATION_CHOICES = (
    ("absent", "Отсутствует"),
    ("SMS", "СМС"),
    ("email", "email"),
    ("SMS_email", "СМС + email"),
)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255, verbose_name="Имя")
    second_name = models.CharField(max_length=255, verbose_name="Фамилия")
    patronymic = models.CharField(max_length=255, blank=True, verbose_name="Отчество")
    phone_number = PhoneNumberField(verbose_name="Номер телефона")
    date_of_registration = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name="Дата регистрации"
    )
    code_for_phone = models.CharField(
        max_length=6, blank=True, default="", verbose_name="код для телефона"
    )
    code_for_email = models.CharField(
        max_length=6, blank=True, default="", verbose_name="Код для почты"
    )
    username = models.CharField(
        max_length=255, unique=True, db_index=True, verbose_name="Логин"
    )
    email = models.EmailField(
        max_length=255,
        unique=True,
        validators=[validators.validate_email],
        blank=False,
        verbose_name="email",
    )
    id_of_invited = models.CharField(
        max_length=255,
        validators=[validators.validate_integer],
        verbose_name="ID пригласившего",
    )

    office = models.CharField(
        max_length=255, blank=True, default="", verbose_name="Офис"
    )
    town = models.CharField(
        max_length=255, blank=True, default="", verbose_name="Город"
    )
    description = models.CharField(
        max_length=255, blank=True, default="", verbose_name="Описание"
    )

    pasport_serial = models.CharField(
        max_length=255, blank=True, default="", verbose_name="Паспорт серия"
    )
    pasport_number = models.CharField(
        max_length=255, blank=True, default="", verbose_name="Паспорт номер"
    )
    pasport_date_of_gave = models.DateField(
        blank=True, default="1970-03-19", verbose_name="Паспорт дата выдачи"
    )
    pasport_who_gave = models.CharField(
        max_length=255, blank=True, default="", verbose_name="Гражданство"
    )
    citizenship = models.CharField(
        max_length=255, blank=True, default="", verbose_name=""
    )
    city_of_born = models.CharField(
        max_length=255, blank=True, default="", verbose_name="Город рождения"
    )
    date_of_birth = models.DateField(
        blank=True, default="1970-03-19", verbose_name="Дата рождения"
    )
    adress = models.CharField(
        max_length=255, blank=True, default="", verbose_name="Прописка"
    )
    adress_of_living = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="Адресс фактического проживания",
    )
    inn = models.CharField(max_length=255, blank=True, default="", verbose_name="ИНН")
    snils = models.CharField(
        max_length=255, blank=True, default="", verbose_name="СНИЛС"
    )
    number_of_bank_cart = models.CharField(
        max_length=255, blank=True, default="", verbose_name="Номер банковской карты"
    )
    date_of_activate = models.DateField(
        auto_now=False,
        auto_now_add=False,
        verbose_name="Дата активации",
        blank=True,
        null=True,
    )

    is_staff = models.BooleanField(default=False)
    is_verified_by_email = models.BooleanField(default=False)
    is_verified_by_phone = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    verification_choice = models.CharField(
        max_length=255, default="0", choices=VERIFICATION_CHOICES
    )
    USERNAME_FIELD = "username"

    REQUIRED_FIELDS = (
        "name",
        "second_name",
        "email",
        "id_of_invited",
        "office",
        "town",
        "description",
        "pasport_serial",
        "pasport_number",
        "pasport_date_of_gave",
        "pasport_who_gave",
        "citizenship",
        "city_of_born",
        "date_of_birth",
        "adress",
        "adress_of_living",
        "inn",
        "snils",
        "number_of_bank_cart",
    )

    objects = UserManager()

    def __str__(self):
        return self.username

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return f"{self.name} {self.second_name} {self.patronymic}"

    def get_short_name(self):
        return self.name

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)
        some_data = {"id": self.pk, "exp": 1916239022}
        token = jwt.encode(some_data, settings.SECRET_KEY, algorithm="HS256")
        return token.decode("utf-8")

    class Meta:
        verbose_name_plural = "Пользователи"
        verbose_name = "Пользователь"


class UserManager(BaseUserManager):
    def _create_user(
        self,
        username,
        email,
        name,
        second_name,
        id_of_invited,
        patronymic,
        phone_number,
        password="",
        **extra_fields,
    ):
        if not username:
            raise ValueError("Указаное имя пользователя должно быть установлено")
        if not email:
            raise ValueError("Данный адрес электронной почты должен быть установлен")
        if not name:
            raise ValueError("Нужно ввести имя")
        if not second_name:
            raise ValueError("Нужно ввести фамилию")
        if not id_of_invited:
            raise ValueError("Введите id пригласившего вас")

        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            name=name,
            second_name=second_name,
            patronymic=patronymic,
            phone_number=phone_number,
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(
        self,
        username,
        email,
        name,
        second_name,
        id_of_invited,
        patronymic,
        phone_number,
        password,
        **extra_fields,
    ):

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_super", False)

        return self._create_user(
            username,
            email,
            name,
            second_name,
            id_of_invited,
            patronymic,
            password,
            phone_number ** extra_fields,
        )

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_super", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=True.")
        if extra_fields.get("is_super") is not True:
            raise ValueError("Суперпользователь должен иметь is_super=True.")

        return self._create_user(username, password, **extra_fields)
