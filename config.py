from time import strftime
import re  # библиотека регулярных выражений

# Названия корневых файлов
db_name = 'main.db'
log_file_name = 'log.txt'
logging_in_file = False

# Константы для даты и времени
# format_datetime = '%d.%m.%Y %H:%M:%S'
# format_date = '%d.%m.%Y'
# format_time = '%H:%M:%S'

format_datetime = '%Y-%m-%d %H:%M:%S'
format_date = '%Y-%m-%d'
format_time = '%H:%M:%S'

now_date = strftime(format_date)
now_time = strftime(format_time)
now_datetime = strftime(format_datetime)


# Функция для отчистки результата SELECT от спецсимволов
def cleaner_sql_select(str_to_clear):
    return re.sub('\W+', '', str(str_to_clear))


def get_simple_list_from_sql_list(temp: list, id_column):
    result = []
    for i in temp:
        result.append(i[id_column])
    return result


def form_events_text(events: list):
    result = []
    for i in events:
        result.append(f'{i[2]}: {i[1]}')
    return result


# Команда "Подписаться" (в инлайн клавиатуре управления подпиской)
command_button_subscribe = 'button_subscribe'
# Команда "Отписаться" (в инлайн клавиатуре управления подпиской)
command_button_unsubscribe = 'button_unsubscribe'

# Команда "Подтвердить" (в инлайн клавиатуре завершения создания события)
command_button_access_invitation = 'button_access_invitation'
# Команда "Отклонить" (в инлайн клавиатуре завершения создания события)
command_button_reject_invitation = 'button_reject_invitation'
