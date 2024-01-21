from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    photo = models.ImageField(
        upload_to="users/%Y/%m/%d/", blank=True, null=True, verbose_name="Фото"
    )
    patronymic = models.CharField(max_length=200, verbose_name="Отчество")
    position = models.CharField(max_length=500, verbose_name="Должность")
    superior = models.BooleanField(default=False, verbose_name="Руководитель")
    subordinates = models.BooleanField(default=True, verbose_name="Рядовой сотрудник")
