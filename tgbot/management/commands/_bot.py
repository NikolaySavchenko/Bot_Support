from environs import Env

from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    Filters
)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.models import User


env = Env()
env.read_env()


def choose_role_keyboard():
    inline_keyboard = [
        [InlineKeyboardButton('Заказчик', callback_data='client')],
        [InlineKeyboardButton('Разработчик', callback_data='developer')],
        [InlineKeyboardButton('Менеджер', callback_data='manager')],
        [InlineKeyboardButton('Админ', callback_data='admin')]
    ]
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)
    return inline_kb_markup


def start(update, context):
    try:
        query = update.callback_query
        chat_id = query.message.chat.id
        message_id = query.message.message_id
    except:
        chat_id = update.message.chat_id
        message_id = update.message.message_id

    # TODO: Попробовать создать юзера с telegram_id
    # Если пользователь найден, то вывести меню для него
    # Далее код для нового пользователя

    message_text = '''Привет! Введите ваше имя:'''

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message_text
    )

    return 'INPUT_PHONE_NUMBER'


def input_phone_number(update, context):
    chat_id = update.message.chat_id

    # TODO: Добавить имя пользователя в модель юзера

    context.bot.send_message(
        chat_id=chat_id,
        text='Введите номер телефона (пример: +79001234567):',
    )

    return 'CHOOSE_ROLE'


def choose_role(update, context):
    chat_id = update.message.chat_id
    
    # TODO: Добавить номер телефона в модель юзера

    context.bot.send_message(
        chat_id=chat_id,
        text='Выберите роль:',
        reply_markup=choose_role_keyboard()
    )
    
    return 'PROFILE'


def profile_handler(update, context):
    query = update.callback_query
    chat_id = query.message.chat.id

    if query.data == 'client':
        message_text = 'Напишите название компании:'

        context.bot.send_message(
            chat_id=chat_id,
            text=message_text,
        )
        

    if query.data == 'developer':
        message_text = '"Объяснение, как работает платформа"'

        context.bot.send_message(
            chat_id=chat_id,
            text=message_text,
        )
        
        


def handle_users_reply(update, context):
    if update.message:
        user_reply = update.message.text
        chat_id = update.message.chat_id
    elif update.callback_query:
        user_reply = update.callback_query.data
        chat_id = update.callback_query.message.chat_id
    else:
        return

    user, created = User.objects.get_or_create(
        telegram_id=chat_id,
    )
    if user_reply == '/start':
        user_state = 'START'
    else:
        user_state = user.state

    states_functions = {
        'START': start,
        'INPUT_PHONE_NUMBER': input_phone_number,
        'CHOOSE_ROLE': choose_role,
        'PROFILE': profile_handler,
        # 'SAVE_COMPANY': save_company,
    }

    print(user_state)
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
    dispatcher.add_handler(CommandHandler('start', start))
    

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
