from telebot import TeleBot
from database import create_database

from config import TOKEN
# from handlers.commands import (register_command_handlers
# from handlers.speechkit import register_speechkit_handlers

from handlers import commands, speechkit

TOKEN = '6808267993:AAHAV5ISY2M9EXfp64mTk0k53LwKflvlQ5U'
bot = TeleBot(TOKEN)


def set_up_handlers():
    commands.register_handlers(bot)
    speechkit.register_handlers(bot)


create_database()

if __name__ == '__main__':
    set_up_handlers()
    bot.polling()
