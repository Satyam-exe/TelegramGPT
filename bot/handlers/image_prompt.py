import openai
import telebot

from bot.constant_messages import invalid_size_message, empty_img_prompt_message
from bot.constants import bot
from bot.error_handlers import on_api_telegram_exception_429
from db.db import insert_image
from open_ai.dalle.reply import get_image_url


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


def register_image():
    bot.register_message_handler(
        reply_with_dalle_img,
        commands=['img']
    )