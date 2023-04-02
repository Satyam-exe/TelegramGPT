import telebot.types

from bot.constant_messages import empty_api_key_message, invalid_api_key_message, api_key_setup_successful_message, \
    api_key_update_successful_message, api_key_remove_successful_message, set_api_key_message
from bot.constants import bot, VALID_API_KEY_TYPES, VALID_API_KEY_MODES
from bot.error_handlers import on_api_telegram_exception_429
from db.db import insert_api_key, remove_api_keys
from open_ai.common import test_openai_api_key, expire_openai_api_key


def set_up_api_key(message: telebot.types.Message):
    try:
        mode, key, key_type = None, None, None
        content = message.text
        if '/apikey@sv_telegram_gpt_bot' in content:
            content = content.replace('/apikey@sv_telegram_gpt_bot', '')
        if '/apikey' in content:
            content = content.replace('/apikey', '')
        if not content:
            bot.reply_to(message, empty_api_key_message)
            return
        param_list = content.split(' ')
        for param in param_list:
            if 'help' in param:
                bot.reply_to(message, set_api_key_message)
                return
            if 'mode=' in param:
                mode = param.split('=')[1]
            if 'key=' in param:
                key = param.split('=')[1]
            if 'type=' in param:
                key_type = param.split('=')[1]
        invalid_params = []
        if not mode or mode not in VALID_API_KEY_MODES:
            invalid_params.append('mode')
        if not key_type or key_type not in VALID_API_KEY_TYPES:
            invalid_params.append('type')
        if not mode == 'remove':
            if not key or not test_openai_api_key(key):
                invalid_params.append('key')
        if len(invalid_params):
            bot.reply_to(message, invalid_api_key_message(', '.join(invalid_params)))
            return
        if mode == 'setup':
            insert_api_key(message, key, 'openai')
            bot.reply_to(message, api_key_setup_successful_message)
        elif mode == 'update':
            expire_openai_api_key(message.from_user.id)
            insert_api_key(message, key, 'openai')
            bot.reply_to(message, api_key_update_successful_message)
        elif mode == 'remove':
            remove_api_keys(message.from_user.id, 'openai')
            bot.reply_to(message, api_key_remove_successful_message)
    except telebot.apihelper.ApiTelegramException:
        on_api_telegram_exception_429(set_up_api_key, message)


def register_api_key_command():
    bot.register_message_handler(
        set_up_api_key,
        commands=['apikey']
    )
