from environs import Env

from telegram.ext import (
    Updater,
    CallbackQueryHandler,
    MessageHandler,
    Filters
)

from _bot_functions import (
    start_new_client,
    input_phone_number,
    start_owner,
    profile_owner,
)

from _func_for_user import get_or_create_user

env = Env()
env.read_env()

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
            'START': start_owner,
            'PROFILE_OWNER': profile_owner,
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
