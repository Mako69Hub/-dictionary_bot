from telebot import TeleBot
from database import create_database

from config import TOKEN
from scheduler import scheduler

from handlers import commands, speechkit

bot = TeleBot(TOKEN)


def set_up_handlers():
    commands.register_handlers(bot)
    speechkit.register_handlers(bot)




if __name__ == '__main__':
    create_database()
    set_up_handlers()
    scheduler.start() #Функция для отложенного напоминания
    bot.polling()
