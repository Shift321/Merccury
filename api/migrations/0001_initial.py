# Generated by Django 3.2.7 on 2021-10-05 15:00

import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('name', models.CharField(max_length=255, verbose_name='Имя')),
                ('second_name', models.CharField(max_length=255, verbose_name='Фамилия')),
                ('patronymic', models.CharField(blank=True, max_length=255, verbose_name='Отчество')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Номер телефона')),
                ('date_of_registration', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата регистрации')),
                ('code_for_phone', models.CharField(blank=True, default='', max_length=6, verbose_name='код для телефона')),
                ('code_for_email', models.CharField(blank=True, default='', max_length=6, verbose_name='Код для почты')),
                ('username', models.CharField(db_index=True, max_length=255, unique=True, verbose_name='Логин')),
                ('email', models.EmailField(max_length=255, unique=True, validators=[django.core.validators.EmailValidator()], verbose_name='email')),
                ('id_of_invited', models.CharField(max_length=255, validators=[django.core.validators.validate_integer], verbose_name='ID пригласившего')),
                ('office', models.CharField(blank=True, default='', max_length=255, verbose_name='Офис')),
                ('town', models.CharField(blank=True, default='', max_length=255, verbose_name='Город')),
                ('description', models.CharField(blank=True, default='', max_length=255, verbose_name='Описание')),
                ('pasport_serial', models.CharField(blank=True, default='', max_length=255, verbose_name='Паспорт серия')),
                ('pasport_number', models.CharField(blank=True, default='', max_length=255, verbose_name='Паспорт номер')),
                ('pasport_date_of_gave', models.DateField(blank=True, default='1970-03-19', verbose_name='Паспорт дата выдачи')),
                ('pasport_who_gave', models.CharField(blank=True, default='', max_length=255, verbose_name='Гражданство')),
                ('citizenship', models.CharField(blank=True, default='', max_length=255, verbose_name='')),
                ('city_of_born', models.CharField(blank=True, default='', max_length=255, verbose_name='Город рождения')),
                ('date_of_birth', models.DateField(blank=True, default='1970-03-19', verbose_name='Дата рождения')),
                ('adress', models.CharField(blank=True, default='', max_length=255, verbose_name='Прописка')),
                ('adress_of_living', models.CharField(blank=True, default='', max_length=255, verbose_name='Адресс фактического проживания')),
                ('inn', models.CharField(blank=True, default='', max_length=255, verbose_name='ИНН')),
                ('snils', models.CharField(blank=True, default='', max_length=255, verbose_name='СНИЛС')),
                ('number_of_bank_cart', models.CharField(blank=True, default='', max_length=255, verbose_name='Номер банковской карты')),
                ('date_of_activate', models.DateField(blank=True, null=True, verbose_name='Дата активации')),
                ('is_staff', models.BooleanField(default=False)),
                ('is_verified_by_email', models.BooleanField(default=False)),
                ('is_verified_by_phone', models.BooleanField(default=False)),
                ('is_blocked', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('verification_choice', models.CharField(choices=[('absent', 'Отсутствует'), ('SMS', 'СМС'), ('email', 'email'), ('SMS_email', 'СМС + email')], default='0', max_length=255)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
