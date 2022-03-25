from django.db import models


class Office(models.Model):
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    adress = models.CharField(max_length=255)
    # phone_number = models.PhoneNumberField()
    email = models.EmailField()
    longitude = models.CharField(max_length=255)
    latitude = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Офис"
        verbose_name_plural = "Офисы"
