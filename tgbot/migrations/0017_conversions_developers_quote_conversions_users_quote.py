# Generated by Django 4.1.6 on 2023-02-19 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot', '0016_auto_20230218_2139'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversions',
            name='developers_quote',
            field=models.CharField(default='вопрос-ответ', max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='conversions',
            name='users_quote',
            field=models.CharField(default='вопрос-ответ', max_length=1000),
            preserve_default=False,
        ),
    ]