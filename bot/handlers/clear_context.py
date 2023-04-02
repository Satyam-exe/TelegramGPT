import telebot

from bot.constant_messages import context_cleared_message
from bot.constants import bot
from bot.error_handlers import on_api_telegram_exception_429
from db.db import revoke_messages, insert_user_if_not_exists


def clear_context(message: telebot.types.Message):
    insert_user_if_not_exists(message)
    try:
        revoke_messages(message.from_user.id)
        bot.reply_to(
            message, context_cleared_message
        )
    except telebot.apihelper.ApiTelegramException:
        on_api_telegram_exception_429(clear_context, message)


def register_clear_context():
    bot.register_message_handler(
        clear_context,
        commands=['clearcontext']
    )