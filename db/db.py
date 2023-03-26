import datetime

import pytz
import telebot.types
from .config import col


def insert_message(message: telebot.types.Message, reply):
    col.insert_one({
        'user_id': message.from_user.id,
        'username': message.from_user.username,
        'message': message.text,
        'reply': reply,
        'time': datetime.datetime.now(pytz.timezone('Asia/Kolkata')),
        'is_revoked': False
    })


def revoke_messages(user_id):
    col.update_many({"user_id": user_id}, {"$set": {"is_revoked": True}})