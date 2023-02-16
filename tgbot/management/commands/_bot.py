from environs import Env

from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    Filters
)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.models import User, Developer, Manager, Owner


env = Env()
env.read_env()


def get_or_create_user(telegram: str):
    if Owner.objects.filter(telegram=telegram):
        return Owner.objects.filter(telegram=telegram)[0],'OWNER'
    elif Manager.objects.filter(telegram=telegram):
        return Manager.objects.filter(telegram=telegram)[0], 'MANAGER'
    elif Developer.objects.filter(telegram=telegram):
        return Developer.objects.filter(telegram=telegram)[0], 'DEVELOPER'
    elif User.objects.filter(telegram=telegram):
        return User.objects.filter(telegram=telegram)[0], 'CLIENT'
    else:
        user = User.objects.create(telegram=telegram)
        return user, 'NEW_CLIENT'


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

    user = User.objects.get(telegram=username)
    user.name = name
    user.save()

    context.bot.send_message(
        chat_id=chat_id,
        text='Введите номер телефона (пример: +79001234567):',
    )

    # return 'CREATE COMPANY'


def handle_users_reply(update, context):
    if update.message:
        user_reply = update.message.text
        username = update.message.chat.username
    elif update.callback_query:
        user_reply = update.callback_query.data
        username = update.callback_query.message.chat.username
    else:
        return

    user, group = get_or_create_user(username)

    if user_reply == '/start':
        user_state = 'START'
    else:
        user_state = user.state

    print(f'group: {group}')
    print(f'user_state: {user_state}')

    if group == 'OWNER':
        states_functions = {
        # 'START': start_owner,
    }
    elif group == 'MANAGER':
        states_functions = {
        # 'START': start_manager,
    }
    elif group == 'DEVELOPER':
        states_functions = {
        # 'START': start_developer,
    }
    elif group == 'CLIENT':
        states_functions = {
        # 'START': start_client,
        'INPUT_PHONE_NUMBER': input_phone_number,
    }
    elif group == 'NEW_CLIENT':
        states_functions = {
        'START': start_new_client,
    }
    else:
        return

    state_handler = states_functions[user_state]
    
    next_state = state_handler(update, context)
    user.state = next_state
    user.save()


def main():
    tg_token = env.str('TELEGRAM_TOKEN')

    updater = Updater(tg_token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CallbackQueryHandler(handle_users_reply))
    dispatcher.add_handler(MessageHandler(Filters.text, handle_users_reply))
    

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
