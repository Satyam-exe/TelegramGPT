import datetime

import pytz
import telebot.types
from .config import col


def insert_message(message: telebot.types.Message, reply):
    col.insert_one({
        'username': message.from_user.username,
        'message': message.text,
        'reply': reply,
        'time': datetime.datetime.now(pytz.timezone('Asia/Kolkata')),
        'is_revoked': False
    })


def revoke_messages(username):
    col.update_many({"username": username}, {"$set": {"is_revoked": True}})