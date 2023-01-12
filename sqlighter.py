import sqlite3
import config  # скрипт с конфигурацией бота, константами и командами
from event import Event


class SQLighter:

    # Подключаемся к БД и сохраняем курсор соединения
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    # Получаем всех активных подписчиков бота
    def get_subscriptions(self, status=True):
        with self.connection:
            result = self.cursor.execute("SELECT user_id FROM user WHERE status = ?", (status,)).fetchall()
            return result

    # Проверяем, есть ли уже подписчик в базе
    def subscriber_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `user` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(len(result))

    # Добавляем нового подписчика
    def add_subscriber(self, user_id, user_name, status=True, role=False):
        with self.connection:
            result = self.cursor.execute("INSERT INTO `user` (`user_id`, user_name, `status`, `sub_date`,`sub_time`,"
                                         "`last_change_date`, `last_change_time`, 'role') VALUES(?,?,?,?,?,?,?,?)",
                                         (user_id, user_name, status, config.now_date, config.now_time, config.now_date,
                                          config.now_time, role))
            return result

    # Обновляем статус подписки пользователя
    def update_subscription(self, user_id, status):
        with self.connection:
            result = self.cursor.execute("UPDATE `user` SET `status` = ?, `last_change_date` = ?, `last_change_time` = "
                                         "? WHERE `user_id` = ?", (status, config.now_date, config.now_time, user_id))
            return result

    # Обновляем номер телефона
    def update_phone_number(self, user_id, phone_number):
        with self.connection:
            result = self.cursor.execute("UPDATE 'user' SET `phone_number` = ?, `last_change_date` = ?, "
                                         "`last_change_time` = ? WHERE `user_id` = ?",
                                         (phone_number, config.now_date, config.now_time, user_id))
            return result

    # Обновляем никнейм
    def update_nickname(self, user_id, nickname):
        with self.connection:
            result = self.cursor.execute("UPDATE `user` SET `nickname` = ?, `last_change_date` = ?, `last_change_time` "
                                         "= ? WHERE `user_id` = ?",
                                         (nickname, config.now_date, config.now_time, user_id))
            return result

    # Добавляем лог переписки с пользователем
    def add_history_log(self, user_id, user_name, text):
        with self.connection:
            result = self.cursor.execute("INSERT INTO `history` (`user_id`, user_name, `date`, `time`, `message_text`) "
                                         "VALUES(?,?,?,?,?)",
                                         (user_id, user_name, config.now_date, config.now_time, text))
            return result

    # Получаем роль подписчика
    def get_role(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT role FROM `user` WHERE `user_id` = ?", (user_id,)).fetchall()
            return config.cleaner_sql_select(result)

    # Получаем мастер-id подписчика
    def get_master_user_id(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT id FROM `user` WHERE `user_id` = ?", (user_id,)).fetchall()
            return result

    # Добавляем запись о рассылке в таблицу invitation
    def add_new_invitation(self, user_id, text):
        with self.connection:
            result = self.cursor.execute("INSERT INTO `invitation` (`master_user_id`, 'date_create','time_create',"
                                         "`invite_text`) VALUES(?,?,?,?)",
                                         (user_id, config.now_date, config.now_time, text))
            return result

    # Получаем id последней записи рассылки пользователя
    def get_last_user_invite(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT MAX(id) FROM invitation WHERE master_user_id = ?",
                                         (user_id,)).fetchall()
            return result

    # Проверяем, есть ли номер рассылки в базе
    def invitation_exists(self, invite_id):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `invitation` WHERE `id` = ?', (invite_id,)).fetchall()
            return bool(len(result))

    # Получаем текст рассылки из базы
    def get_invitation_text(self, invite_id):
        with self.connection:
            result = self.cursor.execute('SELECT `invite_text` FROM `invitation` WHERE `id` = ?',
                                         (invite_id,)).fetchall()
            return result

    # Обновляем информацию о проведеной рассылке
    def update_invitation(self, invite_id):
        with self.connection:
            result = self.cursor.execute(
                "UPDATE `invitation` SET date_last_send = ?, time_last_send = ? WHERE `id` = ?",
                (config.now_date, config.now_time, invite_id))
            return result

    # Получаем список всех актуальных типов мероприятий
    def get_no_legacy_event_type(self):
        with self.connection:
            result = self.cursor.execute("SELECT id, name FROM event_type WHERE legacy = 0", ()).fetchall()
            return result

    # Получаем id типа мероприятия по name
    def get_event_type_id(self, type_text):
        with self.connection:
            result = self.cursor.execute("SELECT id FROM event_type WHERE name = ?", (type_text,)).fetchall()
            return result

    # Получаем список всех актуальных локаций
    def get_no_legacy_locations(self):
        with self.connection:
            result = self.cursor.execute("SELECT id, short_name, address, full_name FROM location WHERE legacy = 0",
                                         ()).fetchall()
            return result

    # Получаем id локации по short_name
    def get_location_id(self, location_text):
        with self.connection:
            result = self.cursor.execute("SELECT id FROM location WHERE short_name = ?", (location_text,)).fetchall()
            return result

    # Получаем список организаторов
    def get_organisators(self):
        with self.connection:
            result = self.cursor.execute("SELECT id, nickname FROM user WHERE org_status = 1", ()).fetchall()
            return result

    # Получаем id организатора по нику
    def get_master_org(self, org_text):
        with self.connection:
            result = self.cursor.execute("SELECT id FROM user WHERE nickname = ?", (org_text,)).fetchall()
            return result

    # Добавляем запись о новом мероприятии
    def add_new_event(self, temp_event: Event):
        with self.connection:
            result = self.cursor.execute("INSERT INTO `event` (`date`, 'event_type_id','location_id') VALUES(?,?,?)",
                                         (temp_event.date, temp_event.event_type_id, temp_event.location_id))
            return result

    # Получаем id последней записи в мероприятиях
    def get_last_event_id(self):
        with self.connection:
            result = self.cursor.execute("SELECT MAX(id) FROM event", ()).fetchall()
            return result

    # Получаем актуальные мероприятия
    def get_actual_events(self):
        with self.connection:
            result = self.cursor.execute("SELECT e.id, et.name, e.date FROM event e, event_type et WHERE "
                                         "e.event_type_id = et.id and e.date>=strftime('%Y-%m-%d','now') ORDER BY "
                                         "e.date", ()).fetchall()
            return result

    # Добавляем запись о новой записи на вечер (запись игрока на вечер)
    def add_new_registration(self, reg_date, reg_event_name, user_id):
        with self.connection:
            result = self.cursor.execute("INSERT INTO `registration` ('event_id', `user_id`) VALUES((SELECT event.id "
                                         "FROM event WHERE event.event_type_id = (SELECT event_type.id FROM "
                                         "event_type WHERE event_type.name = ?) AND (event.date = ?)),(SELECT user.id "
                                         "FROM user WHERE user.user_id = ?))",
                                         (reg_event_name, reg_date, user_id))
            return result

    # Проверка на существование записи пользователя на конкретный вечер
    def get_status_registation_event(self, reg_date, reg_event_name, user_id):
        with self.connection:
            result = self.cursor.execute(
                "SELECT registration.id from registration WHERE registration.user_id = (SELECT user.id FROM user "
                "WHERE user.user_id = ?) AND registration.event_id = (SELECT event.id FROM event WHERE "
                "event.event_type_id = (SELECT event_type.id FROM event_type WHERE event_type.name = ?) AND "
                "event.date = ?)",
                (user_id, reg_event_name, reg_date)).fetchall()
            return result

    # Закрываем соединение с БД
    def close(self):
        self.connection.close()

    # TEST
    def get_TEST(self):
        with self.connection:
            result = self.cursor.execute("SELECT id, nickname FROM user WHERE org_status = 1", ()).fetchall()
            return result
