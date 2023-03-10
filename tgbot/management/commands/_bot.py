from environs import Env

from telegram.ext import (
    Updater,
    CallbackQueryHandler,
    MessageHandler,
    Filters
)

from ._bot_functions import (
    start,
    input_name,
    input_phone_number,
    input_company_unp,
    input_company_name,
    choose_tariff,
    send_bill,
    check_payment,
    check_active_tariff,
    user_menu,
    user_profile,
    new_order,
    start_manager,
    start_owner,
    profile_owner,
    agreement,
    check_agree,
    check_access,
    open_access_to_user,
    close_access_to_user,
    add_new_developer,
    close_access_to_developer,
)

from ._func_for_user import get_user_group

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

    user, group = get_user_group(username)

    if user_reply == '/start' and group == 'OWNER':
        user_state = 'START_OWNER'
    elif user_reply == '/start' and group == 'MANAGER':
        user_state = 'START_MANAGER'
    elif user_reply == 'add_client' or user_reply == 'add_developer':
        user_state = 'INPUT_NAME'
    elif user_reply == '/start' and group == 'NEW_USER':
        user_state = 'START'
    else:
        user_state = user.state
    
    print(f'user_reply: {user_reply}')
    print(f'group: {group}')
    print(f'user_state: {user_state}')


    states_functions = {
        'START': start,
        'INPUT_NAME': input_name,
        'INPUT_PHONE_NUMBER': input_phone_number,

        # client
        'INPUT_COMPANY_UNP': input_company_unp,
        'INPUT_COMPANY_NAME': input_company_name,
        'CHOOSE_TARIFF': choose_tariff,
        'SEND_BILL': send_bill,
        'CHECK_PAYMENT': check_payment,
        'CHECK_ACTIVE_TARIFF': check_active_tariff,
        'USER_MENU': user_menu,
        'USER_PROFILE': user_profile,
        'NEW_ORDER': new_order,

        # developer
        'AGREEMENT': agreement,
        'CHECK_AGREE': check_agree,
        'CHECK_ACCESS': check_access,

        # manager
        'START_MANAGER': start_manager,

        # owner
        'START_OWNER': start_owner,
        'PROFILE_OWNER': profile_owner,
        'OPEN_ACCESS_TO_USER': open_access_to_user,
        'CLOSE_ACCESS_TO_USER': close_access_to_user,
        'ADD_NEW_DEVELOPER': add_new_developer,
        'CLOSE_ACCESS_TO_DEVELOPER': close_access_to_developer,
    }

    state_handler = states_functions[user_state]

    next_state = state_handler(update, context)

    if user:
        user, group = get_user_group(username)
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
