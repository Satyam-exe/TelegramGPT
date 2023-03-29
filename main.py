import time
from tempfile import TemporaryDirectory

import openai.error
import telebot

from bot.constant_messages import start_message_reply, context_cleared_message, invalid_size_message, \
    empty_voice_message, empty_img_prompt_message, empty_music_query_message, invalid_music_type_message
from bot.constants import bot
from bot.handlers import on_api_telegram_exception_429
from google.youtube.config import query_types
from google.youtube.ytmusic import get_music_results, convert_yt_to_ogg
from open_ai.chatgpt.reply import get_chatgpt_reply
from db.db import insert_message, revoke_messages, insert_image, insert_music
from open_ai.constants import set_openai_api_key
from open_ai.dalle.reply import get_image_url
from open_ai.whisper.whisper import transcribe_voice


set_openai_api_key()


@bot.message_handler(commands=['start'])
def send_intro(message: telebot.types.Message):
    try:
        revoke_messages(message.from_user.id)
        bot.reply_to(
            message, start_message_reply(message)
        )
    except telebot.apihelper.ApiTelegramException:
        on_api_telegram_exception_429(send_intro, message)


@bot.message_handler(commands=['clearcontext'])
def clear_context(message: telebot.types.Message):
    try:
        revoke_messages(message.from_user.id)
        bot.reply_to(
            message, context_cleared_message
        )
    except telebot.apihelper.ApiTelegramException:
        on_api_telegram_exception_429(clear_context, message)


@bot.message_handler(commands=['img'])
def reply_with_dalle_img(message: telebot.types.Message):
    try:
        str_list = message.text.split(' ')
        size = '512x512'
        prompt = message.text.replace('/img', '')
        for str in str_list:
            if 'size=' in str:
                untested_size = str.split('=')[1]
                if 'x' in untested_size.lower():
                    dimensions_list = untested_size.split('x')
                    if len(dimensions_list) == 2:
                        size = untested_size
                        prompt = prompt.replace(size, '')
                    else:
                        bot.reply_to(message, invalid_size_message)
                        return
                else:
                    bot.reply_to(message, invalid_size_message)
                    return
        if not prompt:
            bot.reply_to(message, empty_img_prompt_message)
            return
        image_url = get_image_url(prompt=prompt, size=size)
        insert_image(message=message, image_url=image_url)
        bot.send_photo(message.chat.id, photo=image_url, reply_to_message_id=message.message_id)
    except telebot.apihelper.ApiTelegramException as e:
        if e.error_code == 429:
            on_api_telegram_exception_429(reply_with_dalle_img, message)
    except openai.error.InvalidRequestError:
        bot.reply_to(message, invalid_size_message)


@bot.message_handler(commands=['music'])
def reply_with_music(message: telebot.types.Message):
    try:
        str_list = message.text.split(' ')
        type = 'songs'
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


@bot.message_handler(content_types=['voice'])
def reply_to_voice_prompt(message: telebot.types.Message):
    transcribed_voice = transcribe_voice(message)
    if not transcribed_voice:
        bot.reply_to(message=message, text=empty_voice_message)
    else:
        try:
            reply = get_chatgpt_reply(
                content=transcribed_voice,
                user_id=message.from_user.id,
                full_name=message.from_user.full_name,
                username=message.from_user.username
            )
            insert_message(message=message, reply=reply, transcribed_voice=transcribed_voice)
            bot.reply_to(message=message, text=reply)
        except telebot.apihelper.ApiTelegramException:
            on_api_telegram_exception_429(reply_to_voice_prompt, message)


@bot.message_handler(func=lambda message: message.text.isprintable())
def reply_to_text_prompt(message: telebot.types.Message):
    try:
        reply = get_chatgpt_reply(
            content=message.text,
            user_id=message.from_user.id,
            full_name=message.from_user.full_name,
            username=message.from_user.username
        )
        insert_message(message, reply)
        bot.reply_to(message=message, text=reply)
    except telebot.apihelper.ApiTelegramException:
        on_api_telegram_exception_429(reply_to_text_prompt, message)


try:
    bot.polling()
except Exception as e:
    print(e)
    time.sleep(5)
