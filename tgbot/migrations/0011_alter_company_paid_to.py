# Generated by Django 4.1.6 on 2023-02-18 18:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot', '0010_company_paid_to_alter_company_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='paid_to',
            field=models.DateField(blank=True, default=datetime.datetime(2023, 2, 18, 21, 6, 55, 523244), null=True, verbose_name='Оплачено до:'),
        ),
    ]