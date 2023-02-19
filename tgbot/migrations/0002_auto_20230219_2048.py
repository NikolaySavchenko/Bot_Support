# Generated by Django 4.1.6 on 2023-02-19 17:48

from django.db import migrations
import datetime


def add_tariff(apps, schema_editor):
    tariffs_in_db = apps.get_model('tgbot', 'Tariff')
    tariffs = [{'title': 'Эконом', 'max_requests': 5, 'max_time_for_ansver': datetime.timedelta(hours=24),
                'booking_the_developer': False, 'developer_contact': False, 'price': 100},
               {'title': 'Стандарт', 'max_requests': 15, 'max_time_for_ansver': datetime.timedelta(hours=1),
                'booking_the_developer': True, 'developer_contact': False, 'price': 200},
               {'title': 'VIP', 'max_requests': 60, 'max_time_for_ansver': datetime.timedelta(hours=1),
                'booking_the_developer': True, 'developer_contact': True, 'price': 300}]

    for tariff in tariffs:
        try:
            tariffs_in_db.objects.update_or_create(title=tariff['title'], max_requests=tariff['max_requests'],
                                         max_time_for_ansver=tariff['max_time_for_ansver'],
                                         booking_the_developer=tariff['booking_the_developer'],
                                         developer_contact=tariff['developer_contact'],
                                         price=tariff['price'])
        except:
            continue

class Migration(migrations.Migration):

    dependencies = [
        ('tgbot', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_tariff),
    ]
