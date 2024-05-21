from telebot import TeleBot
from telebot.types import Message


def start_handler(message: Message, bot: TeleBot):
    bot.send_message(message.chat.id, 'start_text')


def register_command_handlers(bot: TeleBot):
    bot.register_message_handler(start_handler, commands=['start'], pass_bot=True)
