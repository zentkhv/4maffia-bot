import config       # скрипт с конфигурацией бота, константами и командами
import logging      # библиотека для вывода логов в консоль
import keyboards    # скрипт со всеми клавиатурами
import word         # скрипт с текстовиками
import credentials  # токен для бота

from aiogram import Bot, Dispatcher, executor, types  # элементы библиотеки для работы с ботом
from sqlighter import SQLighter  # класс для работы с бд sql
from event import Event

from aiogram_calendar import simple_cal_callback, SimpleCalendar, dialog_cal_callback, \
    DialogCalendar  # pip install aiogram_calendar
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, ReplyKeyboardMarkup

# from aiogram.dispatcher.filters import Text


# Глобальные переменные
temp_event = Event()
temp_event_type = []
temp_locations = []
temp_main_orgs = []

# Определяем логирование
if config.logging_in_file:
    logging.basicConfig(filename=config.log_file_name, filemode='a', format='%(asctime)s: |%(name)s %(levelname)s| %('
                                                                            'message)s',
                        datefmt=config.format_datetime, level=logging.INFO)
    logging.info("Log started")
else:
    logging.basicConfig(level=logging.INFO)

# Инициализируем бота
bot = Bot(token=credentials.TOKEN)
dp = Dispatcher(bot)

# инициализируем соединение с БД
db = SQLighter(config.db_name)


# Команда старт
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    # добавляем пользователя в таблицу user, если его там еще нет
    if not db.subscriber_exists(message.from_user.id):
        db.add_subscriber(message.from_user.id, message.from_user.username, True)

    await message.answer(word.text_start, reply_markup=keyboards.get_main_keyboard(db.get_role(message.from_user.id)))

    db.add_history_log(message.from_user.id, message.from_user.username, message.text)


# Собитие нажатие кнопки подписки
@dp.callback_query_handler(lambda c: c.data == config.command_button_subscribe)
async def process_callback_button_subscribe(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    if not db.subscriber_exists(callback_query.from_user.id):
        # если юзера нет в базе, добавляем его
        db.add_subscriber(callback_query.from_user.id, callback_query.from_user.username, True)
    else:
        # если он уже есть, то просто обновляем ему статус подписки
        db.update_subscription(callback_query.from_user.id, True)

    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)

    # Логирование
    db.add_history_log(callback_query.from_user.id, callback_query.from_user.username, word.text_subscribe_log)
    await bot.send_message(callback_query.from_user.id, word.text_success_subscribe)


# Собитие нажатие кнопки отписки
@dp.callback_query_handler(lambda c: c.data == config.command_button_unsubscribe)
async def process_callback_button_unsubscribe(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    if not db.subscriber_exists(callback_query.from_user.id):
        # если юзера нет в базе, добавляем его с неактивной подпиской (запоминаем)
        db.add_subscriber(callback_query.from_user.id, False)
        await bot.send_message(callback_query.from_user.id, word.text_unsubscribe_decline)
    else:
        # если он уже есть, то просто обновляем ему статус подписки
        db.update_subscription(callback_query.from_user.id, False)
        await bot.send_message(callback_query.from_user.id, word.text_unsubscribe_success)

    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)

    # Логирование
    db.add_history_log(callback_query.from_user.id, callback_query.from_user.username, word.text_unsubscribe_log)


# Обработка полученного контакта и запись его в базу
@dp.message_handler(content_types=['contact'])
async def get_contact(message: types.Message):
    db.update_phone_number(message.contact["user_id"], message.contact["phone_number"])

    # Логирование
    db.add_history_log(message.from_user.id, message.from_user.username, message.contact["phone_number"])

    await bot.send_message(message.from_user.id, word.text_save_contact)


# Обработка событий календаря
@dp.callback_query_handler(simple_cal_callback.filter())
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: dict):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        # Формирование выбраной даты и запись в temp
        result = date.strftime(config.format_date)
        temp_event.date = result
        # Вывод текста о типе мероприятия, вывод инлайн клавиатуры со списком
        await callback_query.message.answer(word.text_select_event_type,
                                            reply_markup=keyboards.get_dynamic_list_keyboard(
                                                config.get_simple_list_from_sql_list(db.get_no_legacy_event_type(), 1)))
        # Логирование
        db.add_history_log(callback_query.from_user.id, callback_query.from_user.username, result)


# Собитие нажатия инлайн кнопки типа игрового вечера
@dp.callback_query_handler(lambda c: c.data in config.get_simple_list_from_sql_list(db.get_no_legacy_event_type(), 1))
async def process_callback_event_type_chose(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    # Вывод текста выбора и запись в temp
    temp_event.event_type_text = callback_query.data
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    # Вывод текста о месте проведения, вывод инлайн клавиатуры со списком
    await callback_query.message.answer(word.text_select_location, reply_markup=keyboards.get_dynamic_list_keyboard(
        config.get_simple_list_from_sql_list(db.get_no_legacy_locations(), 1)))

    # Логирование
    db.add_history_log(callback_query.from_user.id, callback_query.from_user.username, callback_query.data)


# Собитие нажатия инлайн кнопки списка локаций
@dp.callback_query_handler(lambda c: c.data in config.get_simple_list_from_sql_list(db.get_no_legacy_locations(), 1))
async def process_callback_location_chose(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    # Вывод текста выбора и запись в temp
    temp_event.location_text = callback_query.data

    for i in db.get_no_legacy_locations():
        if i[1] == callback_query.data:
            temp_event.address = i[2]
            temp_event.full_name = i[3]

    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)

    # Сохраняем в теми ID локации и типа вечера
    temp_event.location_id = str(db.get_location_id(temp_event.location_text))[2:-3:]
    temp_event.event_type_id = str(db.get_event_type_id(temp_event.event_type_text))[2:-3:]

    # Добавляем новое событие, получаем его номер, сохраняем переменную и temp_event
    db.add_new_event(temp_event)
    temp_event_id = str(db.get_last_event_id()[0][0])
    temp_event.event_id = temp_event_id

    # Формируем текст рассылки
    event_invitation_text = word.get_normal_evening_text(temp_event)

    # Добавляем новую рассылку в базу, получаем ее номер
    db.add_new_invitation(db.get_master_user_id(callback_query.from_user.id)[0][0], event_invitation_text)
    value = str(db.get_last_user_invite(db.get_master_user_id(callback_query.from_user.id)[0][0])[0][0])
    temp_event.invitation_id = value

    await bot.send_message(callback_query.from_user.id,
                           f"{temp_event.event_type_text}\n"
                           f"Дата: {temp_event.date}\n"
                           f"Место: {temp_event.location_text}\n"
                           f"Номер мероприятия: {temp_event_id}\n"
                           f"Номер рассылки: {value}")
    # Запрос разрешения на отправку рассылки
    await bot.send_message(callback_query.from_user.id, word.text_send_event_now,
                           reply_markup=keyboards.get_instant_access_keyboard())

    # Логирование
    db.add_history_log(callback_query.from_user.id, callback_query.from_user.username, callback_query.data)


# Собитие нажатие кнопки согласия провести рассылку после создания мероприятия
@dp.callback_query_handler(lambda c: c.data == config.command_button_access_invitation)
async def process_callback_button_access_invitation(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)

    # Проведение процесса рассылки
    if db.get_role(callback_query.from_user.id) == "1":
        invite_id = temp_event.invitation_id
        text = db.get_invitation_text(invite_id)
        if db.invitation_exists(invite_id):
            db.update_invitation(invite_id)
            for i in db.get_subscriptions():
                await bot.send_message(i[0], text[0][0])
        else:
            # Если введеный id не был найден в базе
            await bot.send_message(callback_query.from_user.id, word.text_invitation_search_error)

    # Логирование
    db.add_history_log(callback_query.from_user.id, callback_query.from_user.username, callback_query.message.text)


# Собитие нажатие кнопки отклонения провести рассылку после создания мероприятия
@dp.callback_query_handler(lambda c: c.data == config.command_button_reject_invitation)
async def process_callback_button_reject_invitation(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)

    await bot.send_message(callback_query.from_user.id, word.text_invitation_reject)

    # Логирование
    db.add_history_log(callback_query.from_user.id, callback_query.from_user.username, callback_query.message.text)


# Собитие нажатия инлайн кнопки записи на конкретный вечер
@dp.callback_query_handler(lambda c: c.data in config.form_events_text(db.get_actual_events()))
async def process_callback_register_on_event(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    a = callback_query.data.split(": ")

    if len(db.get_status_registation_event(a[0], a[1], callback_query.from_user.id)) > 0:
        await callback_query.message.answer(word.text_registration_reject)
    else:
        # Кладем запись в базу
        db.add_new_registration(a[0], a[1], callback_query.from_user.id)
        # Выводим информацию о записи
        await callback_query.message.answer(word.get_registration_text(a[1], a[0]))

    # Логирование
    db.add_history_log(callback_query.from_user.id, callback_query.from_user.username, callback_query.data)


# Обработка сообщений от пользователей
@dp.message_handler()
async def echo_message(message: types.Message):
    # Обработка переключения меню Настроек
    if message.text == word.label_settings:
        await message.answer(word.text_settings, reply_markup=keyboards.get_settings_keyboard())

    # Обработка переключения меню Справочник
    elif message.text == word.label_dictionary:
        await message.answer(word.text_dictionary, reply_markup=keyboards.get_manual_keyboard())

    # Обработка переключения Главного меню
    elif message.text == word.label_main_menu:
        await message.answer(word.text_main_menu,
                             reply_markup=keyboards.get_main_keyboard(db.get_role(message.from_user.id)))

    # Обработка переключения Админского меню
    elif message.text == word.label_admin:
        if db.get_role(message.from_user.id) == '1':
            await message.answer(word.text_admin_menu, reply_markup=keyboards.get_admin_keyboard())

    # Обработка нажатия кнопки Управления рассылкой (подпиской)
    elif message.text == word.label_subscribe:
        await bot.send_message(message.from_user.id, word.text_subscribe_answer,
                               reply_markup=keyboards.get_manager_subscribe_keyboard())

    # Обработка нажатия кнопки Записать ник
    elif message.text == word.label_nickname:
        await message.answer(word.text_nickname)

    # Обработка вариантов реакции на символ * (добавление ника)
    elif message.text[0] == '*':
        if len(message.text) == 1:
            await bot.send_message(message.from_user.id, word.text_nickname_error)
        else:
            try:
                db.update_nickname(message.from_user.id, message.text[1:len(message.text)])
                await bot.send_message(message.from_user.id, word.text_nickname_success)
            except Exception:
                await bot.send_message(message.from_user.id, word.error_nick_valid)

    # Обработка нажатия кнопки Расписание игр
    elif message.text == word.label_acting:
        await message.answer(word.text_acting)
        if len(db.get_actual_events()) != 0:
            await bot.send_message(message.from_user.id, "Ты можешь записаться на игры",
                                   reply_markup=keyboards.get_dynamic_list_keyboard(
                                       config.form_events_text(db.get_actual_events())))
        else:
            await bot.send_message(message.from_user.id, "К сожалению не могу записать тебя на игры.")

    # Обработка нажатия кнопки Сделать рассылку
    elif message.text == word.label_invitation:
        await message.answer(word.text_invitation)

    # Обработка события получения сообщения с символом % (добавление новой рассылки)
    elif message.text[0] == '%' and db.get_role(message.from_user.id) == "1":
        # Добавляем новую запись в базу, у сообщения убираем первый символ
        db.add_new_invitation(db.get_master_user_id(message.from_user.id)[0][0], message.text[1::])
        # Получаем значение ID последней рассылки
        value = str(db.get_last_user_invite(db.get_master_user_id(message.from_user.id)[0][0])[0][0])
        await message.answer(word.text_invitation_create + value)

    # Обработка события получения сообщения с символом & (отправка рассылки)
    elif message.text[0] == '&' and db.get_role(message.from_user.id) == "1":
        invite_id = message.text[1::]
        text = db.get_invitation_text(invite_id)
        if db.invitation_exists(invite_id):
            db.update_invitation(invite_id)
            for i in db.get_subscriptions():
                await bot.send_message(i[0], text[0][0])
        else:
            # Если введеный id не был найден в базе
            await message.answer(word.text_invitation_search_error)

    # Обработка нажатия кнопки YouTube
    elif message.text == word.label_youtube:
        await message.answer(word.text_youtube)

    # Обработка нажатия кнопки ВК
    elif message.text == word.label_vkontakte:
        await message.answer(word.text_vkontakte)

    # Обработка нажатия кнопки Стоимость
    elif message.text == word.label_price:
        await message.answer(word.text_price)

    # Обработка нажатия кнопки Ведущий
    elif message.text == word.label_master:
        await message.answer(word.text_master)
        await bot.send_contact(message.from_user.id, word.contact_master, word.contact_master_firstname)

    # Обработка нажатия кнопки Создание ивента
    elif message.text == word.label_create_event:
        await message.answer("Новое мероприятие ", reply_markup=await SimpleCalendar().start_calendar())

    # Обработка нажатия кнопки Записавшиеся
    elif message.text == word.label_visitors:
        await message.answer(word.text_in_progress)

        # Обработка события, на которое бот не знает ответа
    else:
        await bot.send_message(message.from_user.id, word.text_unknown_command)

    # Логирование
    db.add_history_log(message.from_user.id, message.from_user.username, message.text)


# Запускаем лонг поллинг
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
