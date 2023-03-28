from datetime import datetime

import pytz
import telebot.types
from .config import messages_col, images_col, voices_col


def insert_message(message: telebot.types.Message, reply, transcribed_voice=None):
    if transcribed_voice:
        content = transcribed_voice
    else:
        content = message.text
    messages_col.insert_one({
        'user_id': message.from_user.id,
        'username': message.from_user.username,
        'message': content,
        'reply': reply,
        'time': datetime.now(pytz.timezone('Asia/Kolkata')),
        'is_revoked': False
    })


def revoke_messages(user_id):
    messages_col.update_many({"user_id": user_id}, {"$set": {"is_revoked": True}})


def insert_image(message: telebot.types.Message, image_url):
    images_col.insert_one({
        'user_id': message.from_user.id,
        'username': message.from_user.username,
        'prompt': message.text.replace('/img', ''),
        'image_url': image_url,
        'time': datetime.now(pytz.timezone('Asia/Kolkata')),
    })


def insert_voice(message: telebot.types.Message, path, transcribed_voice=None, translated_voice=None):
    voices_col.insert_one({
        'user_id': message.from_user.id,
        'username': message.from_user.username,
        'path': path,
        'transcription': transcribed_voice,
        'translation': translated_voice,
        'time': datetime.now(pytz.timezone('Asia/Kolkata')),
    })
