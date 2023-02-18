# Generated by Django 4.1.7 on 2023-02-18 16:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot', '0007_remove_company_paid_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(blank=True, max_length=200, verbose_name='Название компании'),
        ),
        migrations.AlterField(
            model_name='company',
            name='orders_paid',
            field=models.IntegerField(blank=True, verbose_name='Оплаченных заказов осталось'),
        ),
        migrations.AlterField(
            model_name='company',
            name='phone',
            field=models.CharField(blank=True, max_length=200, verbose_name='Телефон'),
        ),
        migrations.AlterField(
            model_name='company',
            name='tariff',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='users', to='tgbot.tariff'),
        ),
    ]