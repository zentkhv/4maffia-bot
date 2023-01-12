from aiogram import Bot, Dispatcher, executor, types

import word  # скрипт с текстовиками
import config  # скрипт с конфигурацией бота, константами и командами


# Основная клавиатура
def get_main_keyboard(role):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard_list = [
        word.label_admin,  # Админка
        word.label_acting,  # Расписание игр
        word.label_dictionary,  # Справочник
        word.label_settings  # Настройки
    ]

    # Инициализация и компановка кнопок Главного меню
    for i in keyboard_list:
        if i == word.label_admin:
            if role == "1":
                markup.add(types.KeyboardButton(i))
        else:
            markup.add(types.KeyboardButton(i))

    return markup


# Клавиатура админа
def get_admin_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard_list = [
        word.label_invitation,  # Рассылка
        word.label_create_event,  # Создать мероприятие
        word.label_visitors,  # Записавшиеся
        word.label_main_menu,  # Главное меню
    ]

    for i in keyboard_list:
        markup.add(types.KeyboardButton(i))

    return markup


# Клавиатура настроек
def get_settings_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard_list = [
        word.label_subscribe,  # Управление подпиской
        word.label_send_contact,  # Получение номера подписчика
        word.label_nickname,  # Записать ник
        word.label_main_menu  # Главное меню
    ]

    for i in keyboard_list:
        if i == word.label_send_contact:
            markup.add(types.KeyboardButton(i, request_contact=True))
        else:
            markup.add(types.KeyboardButton(i))

    return markup


# Клавиатура справочника
def get_manual_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    # Инициализация и компановка кнопок Справочника
    # YouTube и VK
    markup.add(types.KeyboardButton(word.label_youtube), types.KeyboardButton(word.label_vkontakte))
    # Стоимость и Ведущий
    markup.add(types.KeyboardButton(word.label_price), types.KeyboardButton(word.label_master))
    # Главное меню
    markup.add(types.KeyboardButton(word.label_main_menu))

    return markup


# Inline клавиатура управления подпиской
def get_manager_subscribe_keyboard():
    inline_button_subscribe = types.InlineKeyboardButton(word.label_button_subscribe,
                                                         callback_data=config.command_button_subscribe)
    inline_button_unsubscribe = types.InlineKeyboardButton(word.label_button_unsubscribe,
                                                           callback_data=config.command_button_unsubscribe)
    return types.InlineKeyboardMarkup().add(inline_button_subscribe, inline_button_unsubscribe)


# Inline клавиатура подтверждения рассылки после создания мероприятия
def get_instant_access_keyboard():
    inline_button_access_invitation = types.InlineKeyboardButton(word.text_access_instant_invitation,
                                                                 callback_data=config.command_button_access_invitation)
    inline_button_reject_invitation = types.InlineKeyboardButton(word.text_reject_instant_invitation,
                                                                 callback_data=config.command_button_reject_invitation)
    return types.InlineKeyboardMarkup().add(inline_button_access_invitation, inline_button_reject_invitation)


# Inline клавиатура динамического построения
def get_dynamic_list_keyboard(list_sql):
    result = types.InlineKeyboardMarkup()
    for i in list_sql:
        result.add(types.InlineKeyboardButton(str(i), callback_data=str(i)))
    return result
