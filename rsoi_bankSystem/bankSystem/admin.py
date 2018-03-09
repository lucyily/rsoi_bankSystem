from django.contrib import admin
from . import models

admin.site.register(models.Customer)
admin.site.register(models.City)
admin.site.register(models.Sex)
admin.site.register(models.Status)
admin.site.register(models.Citizenship)
admin.site.register(models.Disability)
admin.site.register(models.Pensioner)
admin.site.register(models.Reservist)
