from datetime import datetime

import pytz
import telebot.types
from .config import messages_col, images_col, voices_col, music_col, users_col, group_col, api_keys_col


def insert_message(message: telebot.types.Message, reply, transcribed_voice=None):
    content = message.text
    if transcribed_voice:
        content = transcribed_voice
    if '/chat' in content:
        content = content.replace('/chat', '')
    message_info = {
        'user_id': message.from_user.id,
        'username': message.from_user.username,
        'message': content,
        'reply': reply,
        'time': datetime.now(pytz.timezone('Asia/Kolkata')),
        'is_revoked': False
    }
    if message.chat.type == 'group' or message.chat.type == 'supergroup':
        message_info['group'] = {
            'name': message.chat.title,
            'id': message.chat.id,
        }
    messages_col.insert_one(message_info)


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


def insert_music(message: telebot.types.Message, query, search_results):
    if search_results[0]['resultType'] == 'song':
        music_col.insert_one({
            "user_id": message.from_user.id,
            "username": message.from_user.username,
            "query": query,
            "result_type": "song",
            "video_id": search_results[0]['videoId'],
            "title": search_results[0]['title'],
            "artists": [
                {
                    "name": search_results[0]['artists'][0]['name'],
                    "id": search_results[0]['artists'][0]['id']
                }
            ],
            "album": {
                "name": search_results[0]['album']['name'],
                "id": search_results[0]['album']['id']
            },
            'time': datetime.now(pytz.timezone('Asia/Kolkata')),
        })


def insert_user_if_not_exists(message: telebot.types.Message):
    if not users_col.count_documents({'user_id': message.from_user.id}):
        users_col.insert_one({
            "user_id": message.from_user.id,
            "username": message.from_user.username,
            'fullname': message.from_user.full_name,
            'time': datetime.now(pytz.timezone('Asia/Kolkata')),
        })


def insert_group_if_not_exists(message: telebot.types.Message):
    if not group_col.count_documents({'group_id': message.chat.id}):
        group_col.insert_one({
            "group_id": message.chat.id,
            "group_name": message.chat.title,
            'time': datetime.now(pytz.timezone('Asia/Kolkata')),
        })


def insert_api_key(message: telebot.types.Message, api_key, key_type):
    api_keys_col.insert_one({
        'user_id': message.from_user.id,
        'username': message.from_user.username,
        'key': api_key,
        'type': key_type,
        'is_expired': False,
        'time': datetime.now(pytz.timezone('Asia/Kolkata')),
    })


def get_api_key(user_id, key_type):
    for doc in api_keys_col.find({'user_id': user_id}):
        if doc['type'] == key_type and not doc['is_expired']:
            return doc['key']


def remove_api_keys(user_id, key_type):
    if api_keys_col.count_documents({'user_id': user_id, 'type': key_type}):
        api_keys_col.delete_many({'user_id': user_id, 'type': key_type})
