from telebot import TeleBot
from telebot.types import Message
from database import new_word


def start_handler(message: Message, bot: TeleBot):
    bot.send_message(message.chat.id, 'start_text')
    answer = new_word(message.chat.id, ['cat', 'кошка', message.date])
    bot.send_message(message.from_user.id, answer)



def help_handler(message: Message, bot: TeleBot):
    pass


def register_handlers(bot: TeleBot):
    bot.register_message_handler(start_handler, commands=['start'], pass_bot=True)
    bot.register_message_handler(help_handler, commands=['help'], pass_bot=True)
