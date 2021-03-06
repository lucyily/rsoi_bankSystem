from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from djmoney.models.fields import MoneyField


class City(models.Model):
    name = models.CharField(max_length=40, verbose_name="Название")

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"

    def __str__(self): 
        return self.name


class Sex(models.Model):
    name = models.CharField(max_length=40, verbose_name="Пол")

    class Meta:
        verbose_name = "Пол"
        verbose_name_plural = "Пол"

    def __str__(self): 
        return self.name


class Status(models.Model):
    status = models.TextField(max_length=100, verbose_name="Семейной положение")

    class Meta:
        verbose_name = "Семейной положение"
        verbose_name_plural = "Семейные положения"

    def __str__(self):
        return self.status


class Citizenship(models.Model):
    country_name = models.CharField(max_length=60, verbose_name="Гражданство")

    class Meta:
        verbose_name = "Гражданство"
        verbose_name_plural = "Гражданства"

    def __str__(self):
        return self.country_name


class Disability(models.Model):
    type_of_disability = models.CharField(max_length=60, verbose_name="Вид инвалидности")

    class Meta:
        verbose_name = "Инвалидность"
        verbose_name_plural = "Инвалидности"

    def __str__(self):
        return self.type_of_disability


# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Клиент")
    surname = models.CharField(max_length=40, verbose_name="Фамилия")
    first_name = models.CharField(max_length=40, verbose_name="Имя")
    middle_name = models.CharField(max_length=40, verbose_name="Отчество")
    telephone = models.CharField(max_length= 15, verbose_name = "Телефон", null = True)
    mobile_phone = models.CharField(max_length= 15, verbose_name = "Мобильный телефон", null = True)
    birthday = models.DateField(verbose_name = "Дата рождения")
    birth_place = models.TextField(max_length=200, verbose_name="Место рождения")
    sex = models.ForeignKey('Sex', verbose_name = "Пол", on_delete=models.CASCADE)
    city = models.ForeignKey('City', verbose_name = "Город факт. проживания", on_delete=models.CASCADE)
    address = models.TextField(max_length=200, verbose_name="Адрес факт. проживания")
    email = models.CharField(max_length=80, verbose_name="E-mail")
    status = models.ForeignKey('Status', verbose_name = "Семейное положение", on_delete=models.CASCADE)
    citizenship = models.ForeignKey('Citizenship', verbose_name = "Гражданство", on_delete=models.CASCADE)
    disability = models.ForeignKey('Disability', verbose_name = "Инвалидность", on_delete=models.CASCADE)
    pensioner  = models.BooleanField(verbose_name = "Пенсионер", default=False)
    reservist  = models.BooleanField(verbose_name = "Военнообязанный", default=False)
    month_income = MoneyField(max_digits=10, decimal_places=2, default_currency='BYN', default=0)



    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return 'ФИО: {0} {1} {2}'.format( self.first_name, self.middle_name, self.surname)
