from django.db import models
import sys
import random
# sys.path.insert(0, "..")
# import  bankSystem
from djmoney.models.fields import MoneyField


CURRENCY_CHOICES = [('USD', 'USD $'), ('EUR', 'EUR €'), ('BYN', 'BYN')]
ACCOUNT_TYPE_CHOICE = [('Active', 'Активный'), ('Passive', 'Пассивный'), ('Active-Passive', 'Активно-Пассивный')]

# Create your models here.
class Deposit(models.Model):
    type = models.CharField(max_length=40, verbose_name="Вид депозита")
    term = models.DurationField(verbose_name="Продолжительность")
    currency = models.CharField(max_length=40, choices=CURRENCY_CHOICES)
    is_active = models.BooleanField(verbose_name = "Доступен", default=False)
    min_summ =  MoneyField(max_digits=10, decimal_places=2, default_currency='BYN', default=0)

class Interest(models.Model):
    deposit = models.ForeignKey("Deposit", verbose_name="Депозит", on_delete=models.CASCADE)
    value = models.FloatField(default=0, verbose_name="Сумма")
    rate = models.FloatField(default=0, verbose_name="Ставка")

class TermType(models.Model):
    type = models.CharField(max_length=15, verbose_name="Тип периода")


class ChartOfAccounts(models.Model):
    '''Список счетов'''
    number = models.CharField(max_length=4, verbose_name="Номер счета")
    name = models.CharField(max_length=50, verbose_name="Наименование счета")
    type =models.CharField(max_length=50, choices=ACCOUNT_TYPE_CHOICE)


class Contract(models.Model):
    '''Договор'''
    number = models.CharField(max_length=4, verbose_name="Номер договора", blank=True)
    customer = models.ForeignKey('bankSystem.Customer', verbose_name = "Клиент", on_delete=models.CASCADE)
    deposite = models.ForeignKey('Deposit', verbose_name = "Депозит", on_delete=models.CASCADE)
    start = models.DateField(verbose_name = "Дата начала договора")
    end = models.DateField(verbose_name = "Дата конца договора")
    sum = models.FloatField(max_length=4, verbose_name="Сумма договора")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.number:
            self.number = str(self.id  + 1).zfill(3)
        super().save(*args, **kwargs)


class BankAccount(models.Model):
    '''Класс банковских счетов'''
    number = models.CharField(max_length=13, verbose_name="Номер банковского счета", default="Касса")
    code = models.ForeignKey('ChartOfAccounts', verbose_name = "Код счета из плана счетов", on_delete=models.CASCADE)
    debits = models.FloatField(max_length=10, verbose_name="Дебет", default=0)
    credits = models.FloatField(max_length=10, verbose_name="Кредит", default=0)
    contract = models.OneToOneField('Contract', verbose_name = "Договор", on_delete=models.CASCADE, blank=True, null=True)

    @property
    def balance(self):
        return self.debits - self.credits if self.code.type == 'Active' else self.credits - self.debits

    def commmit_transaction(self, source_target, sum):
        transaction = {
            "Active":{
                "source": self.credits,
                "target": self.debits,      
            },
            "Passive": {
                "source": self.debits,
                "target": self.credits, 
            }
        }
        transaction[self.code.type][source_target] += sum
        self.save()

    def save(self, *args, **kwargs):
        if not self.number and contract:
            self.number = str(self.code.number) \
                          + str(self.contract.customer.id if self.contract else 11111).zfill(5) \
                          + str(self.contract.id).zfill(3)\
                          + str(random.range(10)) 
        super(models.Model, self).save(*args, **kwargs)


class Transaction(models.Model):
    ''''''
    source_acc = models.ForeignKey('BankAccount', verbose_name = "", on_delete=models.CASCADE, related_name='source_acc')
    target_acc = models.ForeignKey('BankAccount', verbose_name = "", on_delete=models.CASCADE, related_name='target_acc')
    date = models.DateTimeField(auto_now_add=True)
    sum = models.FloatField(max_length=10, verbose_name="Сумма договора")

    def save(self, *args, **kwargs):
        super(models.Model, self).save(*args, **kwargs)
        # далее идет двойная запись
        self.source_acc.commmit_transaction("source", self.sum)
        self.target_acc.commmit_transaction("target", self.sum)

