from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Клиент")
    surname = models.CharField(max_length=40, verbose_name="Фамилия")
    first_name = models.CharField(max_length=40, verbose_name="Имя")
    middle_name = models.CharField(max_length=40, verbose_name="Отчество")
    telephone = models.CharField(max_length= 15, verbose_name = "Телефон", null = True)
    birthday = models.DateField(verbose_name = "Дата рождения")

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return 'ФИО: {0} {1} {2}'.format( self.first_name, self.middle_name, self.surname)