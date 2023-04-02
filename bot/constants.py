import os

import telebot
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

bot_token = os.environ.get('BOT_API_KEY')
bot = telebot.TeleBot(bot_token)

VALID_API_KEY_TYPES = [
    'openai'
]

VALID_API_KEY_MODES = [
    'setup',
    'update',
    'remove'
]
