# Generated by Django 4.1.6 on 2023-02-18 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot', '0009_alter_company_orders_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='paid_to',
            field=models.DateField(blank=True, null=True, verbose_name='Оплачено до:'),
        ),
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Название компании'),
        ),
        migrations.AlterField(
            model_name='company',
            name='phone',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Телефон'),
        ),
    ]
