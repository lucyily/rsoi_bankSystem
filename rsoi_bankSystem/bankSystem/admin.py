from django.contrib import admin
import sys
from . import models
sys.path.insert(0, "..")
from deposits.models import Deposit, Contract, ChartOfAccounts
# from ..deposit import models as deposit

admin.site.register(models.Customer)
admin.site.register(models.City)
admin.site.register(models.Sex)
admin.site.register(models.Status)
admin.site.register(models.Citizenship)
admin.site.register(models.Disability)
admin.site.register(Deposit)
admin.site.register(Contract)
admin.site.register(ChartOfAccounts)