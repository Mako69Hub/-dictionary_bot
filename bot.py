from telebot import TeleBot
from telebot.types import Message

from database import create_database, insert_new_word, update_word, select_word, bd_update_lvl
from process import str_in_list_dict, remove_double_word, list_in_str_dict
from config import TOKEN, CUR_USER_DICT, STEP_USER
from time import sleep
from random import sample
import datetime

# from scheduler import scheduler
# from handlers import commands, speechkit

bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_handler(message: Message):
    bot.send_message(message.chat.id,
                     'Привет! Я бот для запоминания слов.\nНапиши /new чтобы добавить слово и перевод. \nНапиши /list чтобы посмотреть все слова.\n'
                     'Напиши /update чтобы обновить значение слова.')


@bot.message_handler(commands=['help'])
def help_handler(message: Message):
    bot.send_message(message.chat.id, '/new - добавить слово и перевод. \n/list - посмотреть все слова.\n'
                                      '/update - обновить значение слова.')


@bot.message_handler(commands=['new'])
def new_word_info_handler(message: Message):
    bot.send_message(message.chat.id,
                     'Напиши слово и перевод в формате: слово=перевод, можно в одно сообщение. Не используй цифры в слове')


@bot.message_handler(func=lambda message: '=' in message.text)
def new_word_handler(message: Message):
    cur_list_dict, report_int = str_in_list_dict(message.text)
    list_dict, report_check = remove_double_word(message.chat.id, cur_list_dict)
    report = report_int + report_check  # Репорт наличие цифр и наличия слов в БД

    if report and list_dict == []:  # добавить проверку на цифры
        bot.send_message(message.chat.id, 'Слова уже есть в словаре')
        return

    if report:
        bot.send_message(message.chat.id, report)
        sleep(1)
        str_dict1 = list_in_str_dict(list_dict)
        bot.send_message(message.chat.id, str_dict1)

    bot.send_message(message.chat.id, 'Если всё верно, то нажмите /da')
    bot.register_next_step_handler(message, double_check, list_dict)


def double_check(message, dict_user):
    if message.text.lower() == '/da':
        date_dict = datetime.date.fromtimestamp(message.json['date'])

        report = ''
        for element in dict_user:  # list
            report += insert_new_word(message.chat.id, [element[0], element[1], date_dict])

        if not report:
            report = 'Сохранено'
        else:
            report = 'Ошибка во время добавления в БД'
        bot.send_message(message.chat.id, report)
    return


@bot.message_handler(commands=['update'])
def handle_update_command(message):
    bot.reply_to(message, "Напиши слово и новый перевод в формате: слово=новый_перевод. Не используй цифры и знаки")
    user_id = message.from_user.id

    def get_update_word(msg):
        try:
            text = msg.text
            word, translation = map(str.strip, text.split('=', 1))

            if not word.isalnum():
                bot.send_message(message.chat.id, 'Слово не должно содержать букв, а вот регистр не имеет значения')
                bot.register_next_step_handler(message, get_update_word)
                return

            update_word(user_id, word, translation)  # вызов функции обновления в БД
            bot.reply_to(msg, f"Перевод для слова '{word}' успешно обновлен на '{translation}'.")
        except ValueError:
            bot.reply_to(msg, "Ошибка в формате. Пожалуйста, используй формат: /update слово=перевод.")

    bot.register_next_step_handler(message, get_update_word)


@bot.message_handler(commands=['list'])
def list_handler(message: Message):
    dict_user_all = select_word(message.chat.id)
    list_user = list_in_str_dict(dict_user_all)
    bot.send_message(message.chat.id, list_user)


@bot.message_handler(commands=['play'])
def play_handler(message: Message):
    dict_user = select_word(message.chat.id)

    if type(dict_user) == 'str':
        bot.send_message(message.chat.id, dict_user)
        return

    count_word = min(10, len(dict_user))
    CUR_USER_DICT[message.chat.id] = sample(dict_user, count_word)
    bot.send_message(message.chat.id,
                     'Вывести список слов для повторения: /list_words.\nИли начать повторение /repeat.\n'
                     '/exit - выход')
    bot.register_next_step_handler(message, repeat_list)


def repeat_list(message: Message):
    if message.text == '/repeat':
        STEP_USER[message.chat.id] = len(CUR_USER_DICT[message.chat.id])
        repeat(message)
        return

    elif message.text == '/list_words':
        list_words = CUR_USER_DICT[message.chat.id]
        text_words = list_in_str_dict(list_words)
        bot.send_message(message.chat.id, text_words)
        bot.register_next_step_handler(message, repeat_list)
        return

    elif message.text == '/exit':
        bot.send_message(message.chat.id, 'Выход из режима повторения...')
        return

    else:
        bot.send_message(message.chat.id,
                         '/list_words - список повторяемых слов.\n/repeat - начать повторение\nВыход - /exit.')
        bot.register_next_step_handler(message, repeat_list)


def repeat(message: Message):
    list_words = CUR_USER_DICT[message.chat.id]
    len_words = len(list_words)

    if len_words == 0:
        bot.send_message(message.chat.id, 'Молодец, повторил все слова')
        return

    cur_word, cur_trans = list_words[0]

    bot.send_message(message.chat.id, f'Напишите перевод слова {cur_trans}')
    bot.register_next_step_handler(message, replay, cur_word)


def replay(message: Message, word_user):
    answer_us = message.text
    if answer_us == '/exit':
        bot.send_message(message.chat.id, 'Жду нашей встречи вновь.')
        return

    if not answer_us.isalnum():
        bot.send_message(message.chat.id, 'Введите ответ без цифр')
        bot.register_next_step_handler(message, replay, word_user)
        return

    if answer_us.lower() == word_user:
        bot.send_message(message.chat.id,
                         'Верно')  # Увеличить уровень, дописать. Ещё нужно спрашивать чела, праввильно или нет
        bd_update_lvl()

    else:
        bot.send_message(message.chat.id, f'Правильное написание: {word_user} ')

    list_words = CUR_USER_DICT[message.chat.id]

    list_words.pop(0)
    CUR_USER_DICT[message.chat.id] = list_words

    repeat(message)
    return

if __name__ == '__main__':
    create_database()
    bot.polling()
