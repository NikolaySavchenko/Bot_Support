# Generated by Django 4.1.6 on 2023-02-17 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot', '0004_merge_20230216_2042'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='unp',
            field=models.IntegerField(default=1, unique=True, verbose_name='УНП компании'),
            preserve_default=False,
        ),
    ]