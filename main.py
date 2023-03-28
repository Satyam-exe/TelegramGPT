import os.path

import openai.error
import telebot

from bot.constant_messages import start_message_reply, context_cleared_message
from bot.constants import bot
from bot.handlers import on_api_telegram_exception_429
from open_ai.chatgpt.reply import get_chatgpt_reply
from db.db import insert_message, revoke_messages, insert_image
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
                        bot.reply_to(message, 'Please enter a valid size. [256x256, 512x512, 1024x1024]')
                        return
                else:
                    bot.reply_to(message, 'Please enter a valid size. [256x256, 512x512, 1024x1024]')
                    return
        if not prompt:
            bot.reply_to(message, 'Please enter a prompt after the /img command.')
            return
        image_url = get_image_url(prompt=prompt, size=size)
        insert_image(message=message, image_url=image_url)
        bot.send_photo(message.chat.id, photo=image_url, reply_to_message_id=message.message_id)
    except telebot.apihelper.ApiTelegramException as e:
        if e.error_code == 429:
            on_api_telegram_exception_429(reply_with_dalle_img, message)
    except openai.error.InvalidRequestError as e:
        bot.reply_to(message, 'Please enter a valid size. [256x256, 512x512, 1024x1024]')


@bot.message_handler(content_types=['voice'])
def reply_to_voice_prompt(message: telebot.types.Message):
    transcribed_voice = transcribe_voice(message)
    print(transcribed_voice)
    try:
        reply = get_chatgpt_reply(content=transcribed_voice, user_id=message.from_user.id)
        insert_message(message=message, reply=reply, transcribed_voice=transcribed_voice)
        bot.reply_to(message=message, text=reply)
    except telebot.apihelper.ApiTelegramException:
        on_api_telegram_exception_429(reply_to_voice_prompt, message)


@bot.message_handler(func=lambda message: message.text.isprintable())
def reply_to_text_prompt(message: telebot.types.Message):
    try:
        reply = get_chatgpt_reply(content=message.text, user_id=message.from_user.id)
        insert_message(message, reply)
        bot.reply_to(message=message, text=reply)
    except telebot.apihelper.ApiTelegramException:
        on_api_telegram_exception_429(reply_to_text_prompt, message)


bot.polling()
