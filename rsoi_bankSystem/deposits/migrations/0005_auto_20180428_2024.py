# Generated by Django 2.0.3 on 2018-04-28 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deposits', '0004_auto_20180422_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankaccount',
            name='number',
            field=models.CharField(blank=True, max_length=13, verbose_name='Номер банковского счета'),
        ),
    ]