# Generated by Django 3.2.6 on 2021-09-23 16:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0002_auto_20210914_1354'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='historyoftopup',
            options={'verbose_name': 'История пополнения пользователя', 'verbose_name_plural': 'История пополнения пользователей'},
        ),
        migrations.AlterModelOptions(
            name='histroyofсonsumption',
            options={'verbose_name': 'История расхода пользователя', 'verbose_name_plural': 'История расхода пользователей'},
        ),
        migrations.AlterModelOptions(
            name='index',
            options={'verbose_name': 'Индекс', 'verbose_name_plural': 'Индексы'},
        ),
        migrations.AlterModelOptions(
            name='userfinance',
            options={'verbose_name': 'Финансовая информация пользователей', 'verbose_name_plural': 'Финансовая информация пользователей'},
        ),
    ]
