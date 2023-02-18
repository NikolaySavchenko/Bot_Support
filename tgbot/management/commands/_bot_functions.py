from ._keyboards import (
    choose_group_keyboard,
    owner_menu_keyboard,
    choose_tariff_keyboard,
)

from ._func_for_user import (
    get_user,
    create_user,
    create_developer,
    add_user_name,
    add_user_phone,
)

from ._func_for_company import (
    get_company,
    create_company,
    get_tariff_list,
    get_tariff,
)


def start(update, context):
    chat_id = update.message.chat.id

    context.bot.send_message(
        chat_id=chat_id,
        text='Добро пожаловать в нашу тех.поддержку! Кто ты?',
        reply_markup=choose_group_keyboard()
    )

    return 'INPUT_NAME'

def input_name(update, context):
    query = update.callback_query
    chat_id = query.message.chat.id
    username = query.message.chat.username

    if query.data == 'add_client':
        if create_user(username):
            context.bot.send_message(
                chat_id=chat_id,
                text='Как вас зовут?'
            )
            return 'INPUT_PHONE_NUMBER'
        else:
            return '/start'

    if query.data == 'add_developer':
        if create_developer(username):
            context.bot.send_message(
                chat_id=chat_id,
                text='Как вас зовут?'
            )
            # TODO: вести прогера по его ветке
            return 'INPUT_PHONE_NUMBER'
        else:
            return '/start'


def input_phone_number(update, context):
    chat_id = update.message.chat_id
    name = update.message.text
    username = update.message.chat.username
    user = get_user(username)

    if add_user_name(user, name):
        context.bot.send_message(
            chat_id=chat_id,
            text='Введите номер телефона (пример: +79001234567):',
        )
        return 'INPUT_COMPANY_UNP'


def input_company_unp(update, context):
    chat_id = update.message.chat_id
    phone = update.message.text
    username = update.message.chat.username
    user = get_user(username)

    if add_user_phone(user, phone):
        context.bot.send_message(
            chat_id=chat_id,
            text='Введите УНП вашей компании:',
        )
        return 'INPUT_COMPANY_NAME'


def input_company_name(update, context):
    chat_id = update.message.chat_id
    company_unp = update.message.text
    username = update.message.chat.username
    user = get_user(username)

    if get_company(company_unp):
        return 'CHECK_ACTIVE_TARIFf'
    else:
        company = create_company(company_unp)
        user.company = company
        user.save()
        context.bot.send_message(
            chat_id=chat_id,
            text='Введите название вашей компании:',
        )
        return 'CHOOSE_TARIFF'

def choose_tariff(update, context):
    chat_id = update.message.chat_id
    company_name = update.message.text
    username = update.message.chat.username
    user = get_user(username)

    if user.company:
        user.company.name = company_name
        user.company.save()

        tariffs = get_tariff_list()
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
        context.bot.send_message(
            chat_id=chat_id,
            text=message,
            reply_markup=choose_tariff_keyboard()
        )
        return 'SEND_BILL'
    else:
        return 'INPUT_COMPANY_UNP'


def send_bill(update, context):
    query = update.callback_query
    chat_id = query.message.chat.id
    username = query.message.chat.username
    user = get_user(username)

    if query.data:
        tariff = get_tariff(query.data)
        user.company.tariff = tariff
        user.company.save()

        context.bot.send_message(
            chat_id=chat_id,
            text="Оплатите СЧЕТ. Сообщите после оплаты"
        )
    return 'CHECK_PAYMENT'


def check_payment(update, context):
    query = update.callback_query
    chat_id = query.message.chat.id
    username = query.message.chat.username
    user = get_user(username)

    context.bot.send_message(
            chat_id=chat_id,
            text="Счет еще не оплачен"
        )
    
    return 'CHECK_PAYMENT'


def start_manager(update, context):
    pass


def start_owner(update, context):
    chat_id = update.message.chat_id

    context.bot.send_message(
        chat_id=chat_id,
        text='Добро пожаловать в тех.поддержку! Что вы хотите сделать?',
        reply_markup=owner_menu_keyboard()
    )

    return 'PROFILE_OWNER'

def profile_owner(update, context):
    pass
