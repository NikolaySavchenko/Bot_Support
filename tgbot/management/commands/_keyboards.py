from telegram import InlineKeyboardButton, InlineKeyboardMarkup


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
