from telebot import TeleBot

from config import TOKEN
from handlers.commands import register_command_handlers

bot = TeleBot(TOKEN)


def set_up_handlers():
    register_command_handlers(bot)


if __name__ == '__main__':
    set_up_handlers()
    bot.polling()
