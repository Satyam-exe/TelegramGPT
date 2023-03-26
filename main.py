import telebot

from bot.constant_messages import start_message_reply
from bot.constants import bot
from chatgpt.reply import get_chatgpt_reply
from db.db import insert_message, revoke_messages


@bot.message_handler(commands=['start'])
def send_intro(message: telebot.types.Message):
    revoke_messages(message.from_user.username)
    bot.reply_to(
        message, start_message_reply(message)
    )


def is_normal(message: telebot.types.Message):
    return message.text.isprintable()


@bot.message_handler(func=is_normal)
def reply_to_prompt(message: telebot.types.Message):
    reply = get_chatgpt_reply(message)
    insert_message(message, reply)
    bot.reply_to(message=message, text=reply)


bot.polling()
