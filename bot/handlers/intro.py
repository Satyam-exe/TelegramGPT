import telebot

from bot.constant_messages import start_message_reply
from bot.constants import bot
from bot.error_handlers import on_api_telegram_exception_429
from db.db import revoke_messages, insert_user_if_not_exists


def send_intro(message: telebot.types.Message):
    try:
        insert_user_if_not_exists(message)
        revoke_messages(message.from_user.id)
        bot.reply_to(
            message, start_message_reply(message)
        )
    except telebot.apihelper.ApiTelegramException:
        on_api_telegram_exception_429(send_intro, message)


def register_intro():
    bot.register_message_handler(
        send_intro,
        commands=['start']
    )
