from tempfile import TemporaryDirectory

import telebot

from bot.constant_messages import invalid_music_type_message, empty_music_query_message
from bot.constants import bot
from bot.error_handlers import on_api_telegram_exception_429
from db.db import insert_music, insert_user_if_not_exists
from google.youtube.config import query_types
from google.youtube.ytmusic import get_music_results, convert_yt_to_ogg


def reply_with_music(message: telebot.types.Message):
    try:
        insert_user_if_not_exists(message)
        str_list = message.text.split(' ')
        type = 'songs'
        if '/music@sv_telegram_gpt_bot' in message.text:
            query = message.text.replace('/music@sv_telegram_gpt_bot', '')
        else:
            query = message.text.replace('/music', '')
        for string in str_list:
            if 'type=' in string:
                untested_type = string.split('=')[1]
                if untested_type in query_types:
                    type = untested_type
                else:
                    bot.reply_to(message, invalid_music_type_message)
                    return
        if not query:
            bot.reply_to(message, empty_music_query_message)
            return
        search_results = get_music_results(query=query, type=type)
        if not search_results:
            bot.reply_to(message, 'Sorry, I could not find that song.')
            return
        insert_music(message=message, search_results=search_results, query=query)
        if search_results[0]['resultType'] == 'song':
            song_name = search_results[0]['title']
            song_id = search_results[0]['videoId']
            artist = search_results[0]['artists'][0]['name']
            album = search_results[0]['album']['name']
            if album:
                bot.reply_to(
                    message,
                    f"Sending {song_name} ({album}) by {artist}"
                )
            else:
                bot.reply_to(
                    message,
                    f"Sending {song_name} by {artist}"
                )
            temp_dir: TemporaryDirectory[str | bytes]
            ogg_file, temp_dir = convert_yt_to_ogg(song_id=song_id)
            bot.send_voice(chat_id=message.chat.id, voice=open(ogg_file, 'rb'), reply_to_message_id=message.message_id)
            temp_dir.cleanup()
        else:
            bot.reply_to(message, 'Something went wrong!')
    except telebot.apihelper.ApiTelegramException as e:
        if e.error_code == 429:
            on_api_telegram_exception_429(reply_with_music, message)


def register_music():
    bot.register_message_handler(
        reply_with_music,
        commands=['music']
    )