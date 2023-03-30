import telebot

from bot.constant_messages import empty_voice_message
from bot.constants import bot
from bot.error_handlers import on_api_telegram_exception_429
from db.db import insert_message
from open_ai.chatgpt.reply import get_chatgpt_reply
from open_ai.whisper.whisper import transcribe_voice


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


def register_chat_voice():
    bot.register_message_handler(
        reply_to_voice_prompt,
        content_types=['voice'],
        chat_types=['private']
    )