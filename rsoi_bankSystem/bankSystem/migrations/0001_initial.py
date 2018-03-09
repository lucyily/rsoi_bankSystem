# Generated by Django 2.0.3 on 2018-03-09 12:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(max_length=40, verbose_name='Фамилия')),
                ('first_name', models.CharField(max_length=40, verbose_name='Имя')),
                ('middle_name', models.CharField(max_length=40, verbose_name='Отчество')),
                ('telephone', models.CharField(max_length=15, null=True, verbose_name='Телефон')),
                ('birthday', models.DateField(verbose_name='Дата рождения')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Клиент')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
            },
        ),
    ]
