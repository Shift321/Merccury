from django.db import models


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    anwser = models.CharField(max_length=255)


class Review(models.Model):
    user = models.ForeignKey("api.User", verbose_name="user", on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
