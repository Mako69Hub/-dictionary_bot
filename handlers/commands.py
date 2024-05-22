from telebot import TeleBot
from telebot.types import Message
from scheduler import create_job, scheduler


def start_handler(message: Message, bot: TeleBot):
    print(message)
    bot.send_message(message.chat.id, 'start_text')
    create_job(bot, message.from_user.id, 1)


def jobs_handler(message: Message, bot: TeleBot):
    scheduler.print_jobs()


def register_command_handlers(bot: TeleBot):
    bot.register_message_handler(start_handler, commands=['start'], pass_bot=True)
    bot.register_message_handler(jobs_handler, commands=['jobs'], pass_bot=True)
