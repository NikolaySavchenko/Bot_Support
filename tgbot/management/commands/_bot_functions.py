from ._keyboards import (
    choose_group_keyboard,
    owner_menu_keyboard,
)

from ._func_for_user import (
    get_user,
    create_user,
    create_developer,
    add_user_name,
    add_user_phone,
)


def start(update, context):
    print(update)
    chat_id = update.message.chat.id

    context.bot.send_message(
        chat_id=chat_id,
        text='Добро пожаловать в нашу тех.поддержку! Кто вы?',
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

    add_user_name(user, name)

    context.bot.send_message(
        chat_id=chat_id,
        text='Введите номер телефона (пример: +79001234567):',
    )

    return 'INPUT_COMPANY_NAME'


def input_company_name(update, context):
    chat_id = update.message.chat_id
    phone = update.message.text
    username = update.message.chat.username
    user = get_user(username)

    add_user_phone(user, phone)

    context.bot.send_message(
        chat_id=chat_id,
        text='Название вашей компании?',
    )

    # return 'CHOOSE_TARIF'


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
