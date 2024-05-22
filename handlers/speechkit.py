from telebot import TeleBot
from telebot.types import Message


def text_handlers(message: Message, bot: TeleBot):
    bot.send_message(message.chat.id, 'hi')
    pass


def register_handlers(bot: TeleBot):
    bot.register_message_handler(text_handlers, content_types=['text'], pass_bot=True)

