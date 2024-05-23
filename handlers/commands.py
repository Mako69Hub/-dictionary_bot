from telebot import TeleBot
from telebot.types import Message
from database import new_word, check_repeat_word, select_word
from scheduler import create_job, scheduler
import datetime

def start_handler(message: Message, bot: TeleBot):
    # print(message.json)
    x = datetime.date.fromtimestamp(message.json['date'])
    print(x)
    bot.send_message(message.chat.id, 'start_text')
    answer = new_word(message.chat.id, ['dog', 'собака', message.date])
    bot.send_message(message.from_user.id, answer)

    create_job(bot, message.from_user.id, 1)


def jobs_handler(message: Message, bot: TeleBot):
    scheduler.print_jobs()


def help_handler(message: Message, bot: TeleBot):
    status, men = check_repeat_word(message.chat.id, 'cat')
    bot.send_message(message.chat.id, men)

def lol_handler(message: Message, bot: TeleBot):
    answer = select_word(message.chat.id)
    bot.send_message(message.chat.id, answer)

def register_handlers(bot: TeleBot):
    bot.register_message_handler(start_handler, commands=['start'], pass_bot=True)
    bot.register_message_handler(help_handler, commands=['help'], pass_bot=True)
    bot.register_message_handler(lol_handler, commands=['lol'], pass_bot=True)
    bot.register_message_handler(jobs_handler, commands=['jobs'], pass_bot=True)
