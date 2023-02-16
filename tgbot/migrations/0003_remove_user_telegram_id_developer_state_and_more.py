# Generated by Django 4.1 on 2023-02-16 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot', '0002_user_state_user_telegram_id_alter_user_company'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='telegram_id',
        ),
        migrations.AddField(
            model_name='developer',
            name='state',
            field=models.CharField(blank=True, max_length=200, verbose_name='Состояние бота'),
        ),
        migrations.AddField(
            model_name='manager',
            name='state',
            field=models.CharField(blank=True, max_length=200, verbose_name='Состояние бота'),
        ),
        migrations.AddField(
            model_name='owner',
            name='state',
            field=models.CharField(blank=True, max_length=200, verbose_name='Состояние бота'),
        ),
        migrations.AlterField(
            model_name='developer',
            name='telegram',
            field=models.CharField(max_length=200, unique=True, verbose_name='Телеграм'),
        ),
        migrations.AlterField(
            model_name='manager',
            name='telegram',
            field=models.CharField(max_length=200, unique=True, verbose_name='Телеграм'),
        ),
        migrations.AlterField(
            model_name='owner',
            name='telegram',
            field=models.CharField(max_length=200, unique=True, verbose_name='Телеграм'),
        ),
        migrations.AlterField(
            model_name='user',
            name='telegram',
            field=models.CharField(max_length=200, unique=True, verbose_name='Телеграм'),
        ),
    ]
