import os

import telebot
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

bot_token = os.environ.get('BOT_API_KEY')
bot = telebot.TeleBot(bot_token)
bot.set_webhook(os.environ.get('WEBHOOK_URL'))
