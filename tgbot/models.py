from enum import unique

from django.db import models


class Tariff(models.Model):
    title = models.CharField('Название тарифа', max_length=200)
    max_requests = models.IntegerField('Максимальное кол-во обращений в месяц')
    max_time_for_ansver = models.TimeField('Максимальное время ответа на заявку')
    booking_the_developer = models.BooleanField('Возможность закрепить Подрядчика')
    developer_contact = models.BooleanField('Возможность получить контакты Подрядчика')

    def __str__(self):
        return self.title


class Company(models.Model):
    name = models.CharField('Название компании', max_length=200, blank=True)
    unp = models.IntegerField('УНП компании', unique=True)
    phone = models.CharField('Телефон', max_length=200, blank=True)
    tariff = models.ForeignKey(Tariff, related_name='users', on_delete=models.PROTECT, null=True)
    # paid_to = models.DateField('Оплачено до:', blank=True, null=True)
    # Поле должно быть высчитываемым, но пока не знаю как сделать, оставлю просто число.
    orders_paid = models.IntegerField('Оплаченных заказов осталось', default=0)

    def __str__(self):
        return self.name

class User(models.Model):
    company = models.ForeignKey(Company, related_name='users', on_delete=models.PROTECT, null=True)
    name = models.CharField('ФИО пользователя', max_length=200)
    phone = models.CharField('Телефон', max_length=200, null=True, blank=True)
    telegram = models.CharField('Телеграм', max_length=200, unique=True)
    state = models.CharField('Состояние бота', max_length=200, blank=True)

    def __str__(self):
        return self.name


class Developer(models.Model):
    name = models.CharField('ФИО разработчика', max_length=200)
    phone = models.CharField('Телефон', max_length=200, null=True, blank=True)
    telegram = models.CharField('Телеграм', max_length=200, unique=True)
    access_to_orders = models.BooleanField('Есть ли доступ к заказам')
    state = models.CharField('Состояние бота', max_length=200, blank=True)

    def __str__(self):
        return self.name


class Manager(models.Model):
    name = models.CharField('ФИО менеджера', max_length=200)
    phone = models.CharField('Телефон', max_length=200, null=True, blank=True)
    telegram = models.CharField('Телеграм', max_length=200, unique=True)
    state = models.CharField('Состояние бота', max_length=200, blank=True)

    def __str__(self):
        return self.name


class Owner(models.Model):
    name = models.CharField('ФИО пользователя', max_length=200)
    phone = models.CharField('Телефон', max_length=200, null=True, blank=True)
    telegram = models.CharField('Телеграм', max_length=200, unique=True)
    state = models.CharField('Состояние бота', max_length=200, blank=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders', on_delete=models.PROTECT)
    description = models.TextField('Описание заказа')
    order_time = models.DateTimeField('Время получения заказ', auto_now_add=True)
    # Должно ставиться автоматически при приеме в работу
    answer_time = models.DateTimeField('Время ответа на заказ')
    developer = models.ForeignKey(Developer, related_name='orders', on_delete=models.PROTECT)
    STATUS_CHOICES = [('N', 'New'), ('W', 'In work'), ('C', 'Completed')]
    status = models.CharField('Статус заказа', choices=STATUS_CHOICES, max_length=1)
    # Должно ставиться автоматичеки при завершении заказа
    comleted_time = models.DateTimeField('Время выполнения')


class Conversions(models.Model):
    order = models.ForeignKey(Order, related_name='conversations', on_delete=models.PROTECT)
    user = models.ForeignKey(User, related_name='details', on_delete=models.PROTECT)
    developer = models.ForeignKey(Developer, related_name='questions', on_delete=models.PROTECT)



