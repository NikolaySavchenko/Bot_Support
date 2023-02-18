from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from ._func_for_company import (
    get_tariff_list,
)


def choose_group_keyboard():
    inline_keyboard = [
        [InlineKeyboardButton('Клиент', callback_data='add_client')],
        [InlineKeyboardButton('Разработчик', callback_data='developer')]
    ]
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)
    return inline_kb_markup


def owner_menu_keyboard():
    inline_keyboard = [
        [InlineKeyboardButton('Открыть доступ клиенту', callback_data='open_access_to_user')],
        [InlineKeyboardButton('Закрыть доступ клиенту', callback_data='close_access_to_user')],
        [InlineKeyboardButton('Добавить нового разработчика', callback_data='add_new_developer')],
        [InlineKeyboardButton('Закрыть доступ разработчику', callback_data='close_access_to_developer')],
        [InlineKeyboardButton('Получить статистику по заказам', callback_data='get_statistics_on_orders')],
        [InlineKeyboardButton('Получить статистику по выплатам', callback_data='get_payout_statistics')]
    ]
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)
    return inline_kb_markup

def user_menu_keyboard():
    inline_keyboard = [
        [InlineKeyboardButton('Отправить новую заявку', callback_data='new_order')],
        [InlineKeyboardButton('Посмотреть статус подписки', callback_data='check_tariff')]
    ]
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)
    return inline_kb_markup


def choose_tariff_keyboard():
    inline_keyboard = []
    for tariff in get_tariff_list():
        inline_keyboard.append([InlineKeyboardButton(tariff.title, callback_data=f'{tariff.id}')])
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)
    return inline_kb_markup
