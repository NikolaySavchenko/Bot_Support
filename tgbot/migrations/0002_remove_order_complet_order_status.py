# Generated by Django 4.1.6 on 2023-02-15 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='complet',
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('N', 'New'), ('W', 'In work'), ('C', 'Completed')], default=('N', 'New'), max_length=1, verbose_name='Статус заказа'),
            preserve_default=False,
        ),
    ]
