from django.utils import timezone

from tgbot.models import Company, Tariff, Order, User


def get_company(company_unp: int):
    try:
        company = Company.objects.get(unp=int(company_unp))
        return company
    except:
        return False

def create_company(company_unp: int):
    company, created = Company.objects.get_or_create(unp=int(company_unp))
    return company


def get_tariff_list():
    tariffs = Tariff.objects.all()
    return tariffs

def get_tariff(tariff_id: str):
    tariff = Tariff.objects.get(id=int(tariff_id))
    return tariff

def get_tariff_message():
    tariffs = Tariff.objects.all()
    message = 'Выберите тариф:'
    for tariff in tariffs:
        message += f'\n{tariff.title}:'
        message += f'\nМаксимальное кол-во обращений в месяц: {tariff.max_requests}'
        message += f'\nМаксимальное время ответа на заявку: {tariff.max_time_for_ansver}'
        if tariff.booking_the_developer:
            message += '\nВозможность закрепить Подрядчика'
        if tariff.developer_contact:
            message += '\nВозможность получить контакты Подрядчика'
        message += '\n'
    return message

def create_order(user: User, order_description: str):
	tariff = user.company.tariff
	answer_time = timezone.now() + tariff.max_time_for_ansver
	order = Order.objects.create(
		user=user,
		description=order_description,
		answer_time=answer_time,
		status='N',

	)
	return order
