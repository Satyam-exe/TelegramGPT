import time

import telebot.types

from bot.constant_messages import too_many_requests_message
from bot.constants import bot


def on_api_telegram_exception_429(function, message: telebot.types.Message):
    bot.send_message(message.id, too_many_requests_message)
    time.sleep(5)
    function(message)
