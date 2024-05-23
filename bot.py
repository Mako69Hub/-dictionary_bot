from telebot import TeleBot
from telebot.types import Message
from database import create_database, insert_new_word
from process import str_in_list_dict, remove_double_word, list_in_str_dict
from config import TOKEN
from time import sleep
import datetime
# from scheduler import scheduler
#
# from handlers import commands, speechkit

bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_handler(message: Message):

    bot.send_message(message.chat.id, 'Привет! Я бот для запоминания слов.\nНапиши /new чтобы добавить слово и перевод. \nНапиши /list чтобы посмотреть все слова.\n'
    'Напиши /update чтобы обновить значение слова.')



@bot.message_handler(commands=['help'])
def help_handler(message: Message):
    bot.send_message(message.chat.id, '/new - добавить слово и перевод. \n/list - посмотреть все слова.\n'
    '/update - обновить значение слова.')

@bot.message_handler(commands=['new'])
def new_word_info_handler(message: Message):
    bot.send_message(message.chat.id,'Напиши слово и перевод в формате: слово=перевод и каждое новое слово пиши новым сообщением')

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
        for element in dict_user: #list
            report += insert_new_word(message.chat.id, [element[0], element[1], date_dict])
            
        if not report:
            report = 'Сохранено'
        else:
            report = 'Ошибка во время добавления в БД'
        bot.send_message(message.chat.id, report)
    return


if __name__ == '__main__':
    create_database()
    bot.polling()
