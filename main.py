import telebot

from bot.constants import bot
from bot.handlers.chat_text_prompt import register_chat_text
from bot.handlers.chat_voice_prompt import register_chat_voice
from bot.handlers.clear_context import register_clear_context
from bot.handlers.image_prompt import register_image
from bot.handlers.intro import register_intro
from bot.handlers.music_prompt import register_music
from bot.handlers.group_messages import register_group

from open_ai.constants import set_openai_api_key

set_openai_api_key()


def register_message_handlers():
    register_intro()
    register_clear_context()
    register_music()
    register_image()
    register_chat_voice()
    register_chat_text()
    register_group()


register_message_handlers()


telebot.apihelper.RETRY_ON_ERROR = True
while True:
    bot.polling()
