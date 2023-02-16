from ._keyboards import owner_menu_keyboard

from ._func_for_user import (
    get_user,
    add_user_name
)

def start_new_client(update, context):
    chat_id = update.message.chat_id

    context.bot.send_message(
        chat_id=chat_id,
        text='Добро пожаловать в нашу тех.поддержку! Как вас зовут?'
    )

    return 'INPUT_PHONE_NUMBER'


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

    # return 'CREATE COMPANY'


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
