from event import Event

# Эти сообщения можно увидеть

# при вызове команды start
text_start = "Привет! Я бот клуба 4MAFIA.\nИспользуй меню и специальные кнопки, чтобы общаться со мной!"

# для записи лога в базу о факте подписки
text_subscribe_log = "Подписаться"
text_unsubscribe_log = "Отписаться"

text_save_contact = 'Мы сохранили твой номер для связи, спасибо! 😊'

# в случае успешного подписания на рассылку
text_success_subscribe = 'Вы подписались на рассылку 📬'

# в случае отписания при неоформленной подписке
text_unsubscribe_decline = 'Вы итак не подписаны 📪'

# в случае успешного отписания от рассылки
text_unsubscribe_success = 'Вы отписаны от рассылки 📪'

# при выборе пункта меню: Настройки
text_settings = "Здесь ты можешь управлять настройками своего профиля 💼"

# при выборе пункта меню: Справочник
text_dictionary = "Здесь ты можешь узнать больше об игре и клубе 🗂"

# при выборе пункта меню: Главное меню
text_main_menu = "Теперь ты в главном меню 📱"

# при выборе что делать со своей подпиской
text_subscribe_answer = 'Что хочешь сделать?'

# при нажатии кнопки записать свой никнейм
text_nickname = "Для того, чтобы мы знали твой никнем, нужно написать его в чат, поставив перед ним символ *, " \
                "вот так:\n*Raptor "

# при получении символа * без никнейма (ошибка)
text_nickname_error = 'Для того чтобы мы знали твой никнейм, нужно дописать его после знака *!'

# при успешном получении никнейма
text_nickname_success = 'Мы сохранили твой никнейм!'

# при выборе пункта меню: Расписание игр
text_acting = "Выберите мероприятие"


# после записи на игровой вечер
def get_registration_text(event, date): return f"Вы записаны на мероприятие: {event}, которое пройдет {date}"


# при выборе пункта меню: Расписание игр
text_registration_reject = "Вы уже записаны на это мероприятие"


# при выборе пункта меню: Сделать рассылку
text_invitation = "Для того чтобы сделать рассылку, отправь мне сообщение, которое начинается с символа %"

# при успешном формировании рассылки, после записи в базу
text_invitation_create = "Для отправки рассылки напиши мне сообщение в формате: &000\nнужно только заменить " \
                         "номер.\nНомер твоей рассылки: "

# при выборе пункта меню: YouTube
text_youtube = "У нашего клуба есть youtube-канал:\nhttps://www.youtube.com/c/4MAFIAclub\nЗдесь ты можешь найти " \
               "видео-обучения и записи с прошедших турниров.\nДля новичков рекомендую видео с правилами " \
               "игры:\nhttps://www.youtube.com/watch?v=kwIT-RYaYqw&list=PLrDRU9lcDcit1DBV9FDKxTjbh9JRfBLma&index=6" \
               "&ab_channel=%224MAFIA%22club "

# при выборе пункта меню: ВКонтакте
text_vkontakte = "Вот наша группа во ВКонтакте:\nhttps://vk.com/4mafia_club\nТут ты можешь найти всю " \
                 "необходимую информацию, посмотреть фотографии, записаться на игровой вечер и " \
                 "много чего еще!"

# при выборе пункта меню: Стоимость
text_price = "Стоимость игрового вечера при первом посещении составляет 1000 руб при оплате по факту " \
             "или 900 руб по предоплате. Если сделать репост анонса, то можно получить ещё скидку в " \
             "100 руб. Повторные посещения стоят по 800 рублей и к ним также могут быть использованы " \
             "скидки за предоплату и репост. Членам клуба стоимость вечера составит 400 рублей. Или " \
             "150 рублей за одну игру. За вечер можно сыграть 2-4 игры.\nБолее подробную информацию " \
             "можешь найти в нашей группе ВКонтакте:\nhttps://vk.com/wall-54109989_5832"

# при выборе пункта меню: Ведущий
text_master = "Вот тебе контакт. Можно обращаться по вопросам записи на мероприятия, да и вообще по любым вопросам."

# при возникновении события, на которое бот не знает ответа
text_unknown_command = 'Я не знаю что ответить...\nЛучше воспользуйся специальными кнопками'

# при переходе в админское меню
text_admin_menu = "Включено админское меню!"

#
text_create_event = "Переходим к созданию мероприятия"

#
text_whatch_registrations = "Переходим к списку записавшихся"

# при завершении создания мероприиятия
text_send_event_now = "Провести рассылку преглашения прямо сейчас?"
text_access_instant_invitation = "Подтвердить"
text_reject_instant_invitation = "Отклонить"

text_invitation_reject = "Рассылка не будет произведена. Вы сможете сделать это самостоятельно, используя номер " \
                         "рассылки. "

text_select_event_type = 'Выберите тип мероприятия:'
text_select_location = 'Выберите место проведения:'

contact_master = "+79145489106"
contact_master_firstname = "Виталий (4Mafia)"

# Мастер-фразы команд
label_settings = '🛠 Настройки'
label_dictionary = '📖 Справочник'
label_main_menu = '🏠 Главное меню'
label_subscribe = '📫 Управление рассылкой'
label_nickname = '📜️ Записать ник'
label_acting = '🗓 Расписание игр'
label_youtube = '▶ YouTube'
label_vkontakte = '💬 ВКонтакте'
label_price = '💵 Стоимость'
label_master = '🤵‍♂ Ведущий'

label_admin = '🧰 Админское меню'
label_invitation = '📰 Сделать рассылку'
label_create_event = '📅 Создать мероприятие'
label_visitors = '📝 Список записавшихся'

label_button_subscribe = '📬 Включить'
label_button_unsubscribe = '📪 Выключить'

label_send_contact = '☎️Оставить номер'

text_in_progress = 'В разработке...'

# Ошибки

# при ошибке в поиске рассылки перед отправкой
text_invitation_search_error = "Такой рассылки не существует."
error_nick_valid = 'Такой никнейм уже используется.'


# Шаблоны для рассылки

def get_normal_evening_text(temp_event: Event):
    return f"Приглашаю тебя на игры в мафию!\n{temp_event.event_type_text} пройдет {temp_event.date} по адресу: {temp_event.address}.\nМесто проведения: {temp_event.full_name}"
