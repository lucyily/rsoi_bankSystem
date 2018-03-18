from django.db import models
import sys
# sys.path.insert(0, "..")
# import  bankSystem
from djmoney.models.fields import MoneyField


CURRENCY_CHOICES = [('USD', 'USD $'), ('EUR', 'EUR €'), ('BYN', 'BYN')]
ACCOUNT_TYPE_CHOICE = [('Active', 'Активный'), ('Passive', 'Пассивный')]

# Create your models here.
class Deposit(models.Model):
	type = models.CharField(max_length=40, verbose_name="Вид депозита")
	interest_rate = models.FloatField(max_length=5, verbose_name="Процентная ставка")
	term = models.DurationField(verbose_name="Продолжительность")
	currency = models.CharField(max_length=40, choices=CURRENCY_CHOICES)
	is_active = models.BooleanField(verbose_name = "Доступен", default=False)
	min_summ =  MoneyField(max_digits=10, decimal_places=2, default_currency='BYN', default=0)

class TermType(models.Model):
	type = models.CharField(max_length=15, verbose_name="Тип периода")


class ChartOfAccounts(models.Model):
	number = models.CharField(max_length=4, verbose_name="Номер счета")
	name = models.CharField(max_length=50, verbose_name="Наименование счета")
	type =models.CharField(max_length=50, choices=ACCOUNT_TYPE_CHOICE)

class Contract(models.Model):
	number = models.CharField(max_length=4, verbose_name="Номер договора")
	customer = models.ForeignKey('bankSystem.Customer', verbose_name = "Клиент", on_delete=models.CASCADE)
	deposite = models.ForeignKey('Deposit', verbose_name = "Депозит", on_delete=models.CASCADE)
	start = models.DateField(verbose_name = "Дата начала договора")
	end = models.DateField(verbose_name = "Дата конца договора")
	summ = models.FloatField(max_length=4, verbose_name="Сумма договора")