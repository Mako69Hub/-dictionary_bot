from telebot import TeleBot
from telebot.types import Message

from database import create_database, insert_new_word, update_word, select_word
from process import str_in_list_dict, remove_double_word, list_in_str_dict
from config import TOKEN
from time import sleep
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
                     'Напиши слово и перевод в формате: слово=перевод, можно в одно сообщение')


@bot.message_handler(func=lambda message: '=' in message.text)
def new_word_handler(message: Message):
    cur_list_dict = str_in_list_dict(message.text)
    list_dict, report = remove_double_word(message.chat.id, cur_list_dict)

    if report and list_dict == []:
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
    bot.reply_to(message, "Напиши слово и новый перевод в формате: слово=новый_перевод")
    user_id = message.from_user.id

    def get_update_word(msg):
        try:
            text = msg.text
            word, translation = map(str.strip, text.split('=', 1))
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


if __name__ == '__main__':
    create_database()
    bot.polling()
