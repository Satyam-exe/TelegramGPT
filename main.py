import telebot

from bot.constants import bot
from bot.handlers.chat_text_prompt import register_chat_text
from bot.handlers.chat_voice_prompt import register_chat_voice
from bot.handlers.clear_context import register_clear_context
from bot.handlers.image_prompt import register_image
from bot.handlers.intro import register_intro
from bot.handlers.music_prompt import register_music
from bot.handlers.manage_api_keys import register_api_key_command


def register_message_handlers():
    register_intro()
    register_clear_context()
    register_api_key_command()
    register_music()
    register_image()
    register_chat_voice()
    register_chat_text()


register_message_handlers()

telebot.apihelper.RETRY_ON_ERROR = True


def run_bot():
    while True:
        try:
            bot.polling(non_stop=True)
        except:
            run_bot()


if __name__ == '__main__':
    run_bot()
