from ._keyboards import (
    choose_group_keyboard,
    owner_menu_keyboard,
    user_menu_keyboard,
    choose_tariff_keyboard,
    agreement_keyboard,
)

from ._func_for_user import (
    get_user_group,
    get_user,
    add_user_phone,
    create_user,
    create_developer,
    get_developer,
)

from ._func_for_company import (
    get_company,
    create_company,
    get_tariff_list,
    get_tariff,
    get_tariff_message,
    create_order,
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
            return 'INPUT_PHONE_NUMBER'
        else:
            return '/start'


def input_phone_number(update, context):
    chat_id = update.message.chat_id
    name = update.message.text
    username = update.message.chat.username
    user, group = get_user_group(username)
    user.name = name
    user.save()

    context.bot.send_message(
        chat_id=chat_id,
        text='Введите номер телефона (пример: +79001234567):',
    )
    if group == 'CLIENT':
        return 'INPUT_COMPANY_UNP'
    if group == 'DEVELOPER':
        return 'AGREEMENT'


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
        return 'CHECK_ACTIVE_TARIFF'
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

        message = get_tariff_message()
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
    chat_id = update.message.chat_id
    username = update.message.chat.username
    user = get_user(username)
    if user.company.is_active():
        context.bot.send_message(
            chat_id=chat_id,
            text="Счет успешно оплачен! Выберите действие:",
            reply_markup=user_menu_keyboard()
        )
        return 'USER_PROFILE'
    else:
        context.bot.send_message(
            chat_id=chat_id,
            text="Счет еще не оплачен. Сообщите как оплатите"
        )

        return 'CHECK_PAYMENT'


def check_active_tariff(update, context):
    chat_id = update.message.chat_id
    username = update.message.chat.username
    user = get_user(username)

    # TODO: добавить проверку
    message = "У вас нет активного тарифа\n"
    message += get_tariff_message()
    context.bot.send_message(
            chat_id=chat_id,
            text=message,
            reply_markup=choose_tariff_keyboard()
        )

    return 'SEND_BILL'


def user_menu(update, context):
    try:
        query = update.callback_query
        chat_id = query.message.chat.id
    except:
        chat_id = update.message.chat_id

    context.bot.send_message(
        chat_id=chat_id,
        text='Выберите действие:',
        reply_markup=user_menu_keyboard()
    )

    return 'USER_PROFILE'


def user_profile(update, context):
    query = update.callback_query
    chat_id = query.message.chat.id
    
    if query.data == 'new_order':
        context.bot.send_message(
            chat_id=chat_id,
            text='Пришлите задание:',
        )
        return 'NEW_ORDER'
    
    elif query.data == 'check_tariff':
        # TODO: добавить проверку
        message = "У вас нет активного тарифа\n"
        message += get_tariff_message()
        context.bot.send_message(
                chat_id=chat_id,
                text=message,
                reply_markup=choose_tariff_keyboard()
            )

        return 'SEND_BILL'


def new_order(update, context):
    chat_id = update.message.chat_id
    order_description = update.message.text
    username = update.message.chat.username
    user = get_user(username)

    order = create_order(user, order_description)

    context.bot.send_message(
        chat_id=chat_id,
        text='Ваш заказ принят. Ожидайте ответа.'
    )



def agreement(update, context):
    chat_id = update.message.chat_id
    
    message = "Наши условия - ... \n Вы согласны продолжить работу?"
    context.bot.send_message(
        chat_id=chat_id,
        text=message,
        reply_markup=agreement_keyboard()
    )

    return 'CHECK_AGREE'

def check_agree(update, context):
    query = update.callback_query
    chat_id = query.message.chat.id

    if query.data == 'agree':
        context.bot.send_message(
            chat_id=chat_id,
            text='Отлично! Теперь чтобы продолжить, ожидайте подтверждения админа.'
        )
        return 'CHECK_ACCESS'
    else:
        context.bot.send_message(
            chat_id=chat_id,
            text='Пока вы не согласитесь, вы не сможете работать. Соглашаетесь?',
            reply_markup=agreement_keyboard()
        )
        return 'CHECK_AGREE'

def check_access(update, context):
    chat_id = update.message.chat_id
    username = update.message.chat.username

    developer = get_developer(username)
    if developer.access_to_orders:
        context.bot.send_message(
            chat_id=chat_id,
            text='Поздравляю! Доступ открыт! Хотите посмотреть активные заказы?'
        )
        # return 'FIND_ORDER_DEV'
    else:
        context.bot.send_message(
            chat_id=chat_id,
            text='Доступ еще не открыт. Ожидайте'
        )
        return 'CHECK_ACCESS'


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
    query = update.callback_query
    chat_id = query.message.chat.id

    if query.data == 'open_access_to_user':
        context.bot.send_message(
            chat_id=chat_id,
            text='Введите ник клиента без @',
        )
        return 'OPEN_ACCESS_TO_USER'

    elif query.data == 'close_access_to_user':
        context.bot.send_message(
            chat_id=chat_id,
            text='Введите ник клиента без @',
        )
        return 'CLOSE_ACCESS_TO_USER'

    elif query.data == 'add_new_developer':
        context.bot.send_message(
            chat_id=chat_id,
            text='Введите ник разработчика без @',
        )
        return 'ADD_NEW_DEVELOPER'

    elif query.data == 'close_access_to_developer':
        context.bot.send_message(
            chat_id=chat_id,
            text='Введите ник разработчика без @',
        )
        return 'CLOSE_ACCESS_TO_DEVELOPER'
    

def open_access_to_user(update, context):
    chat_id = update.message.chat_id
    user_username = update.message.text
    owner_username = update.message.chat.username
    
    if get_user(user_username):
        user = get_user(user_username)
        user.company.activate_per_month()
        context.bot.send_message(
            chat_id=chat_id,
            text='Клиент активирован. Что-то еще?',
            reply_markup=owner_menu_keyboard()
        )
    else:
        context.bot.send_message(
            chat_id=chat_id,
            text='Клиент не найден. Выберите другое действие',
            reply_markup=owner_menu_keyboard()
        )
    return 'PROFILE_OWNER'


def close_access_to_user(update, context):
    chat_id = update.message.chat_id
    user_username = update.message.text
    owner_username = update.message.chat.username
    
    if get_user(user_username):
        user = get_user(user_username)
        user.company.paid_to = None
        user.company.save()
        context.bot.send_message(
            chat_id=chat_id,
            text='Клиент деактивирован. Что-то еще?',
            reply_markup=owner_menu_keyboard()
        )
    else:
        context.bot.send_message(
            chat_id=chat_id,
            text='Клиент не найден. Выберите другое действие',
            reply_markup=owner_menu_keyboard()
        )
    return 'PROFILE_OWNER'


def add_new_developer(update, context):
    chat_id = update.message.chat_id
    developer_username = update.message.text
    owner_username = update.message.chat.username

    if get_developer(developer_username):
        developer = get_developer(developer_username)
        developer.access_to_orders = True
        developer.save()    
        context.bot.send_message(
            chat_id=chat_id,
            text='Разработчик активирован. Что-то еще?',
            reply_markup=owner_menu_keyboard()
        )
    else:
        context.bot.send_message(
            chat_id=chat_id,
            text='Разработчик не найден. Выберите другое действие',
            reply_markup=owner_menu_keyboard()
        )
    return 'PROFILE_OWNER'

def close_access_to_developer(update, context):
    chat_id = update.message.chat_id
    developer_username = update.message.text
    owner_username = update.message.chat.username
    
    if get_developer(developer_username):
        developer = get_developer(developer_username)
        developer.access_to_orders = False
        developer.save()    
        context.bot.send_message(
            chat_id=chat_id,
            text='Разработчик активирован. Что-то еще?',
            reply_markup=owner_menu_keyboard()
        )
    else:
        context.bot.send_message(
            chat_id=chat_id,
            text='Разработчик не найден. Выберите другое действие',
            reply_markup=owner_menu_keyboard()
        )
    return 'PROFILE_OWNER'
