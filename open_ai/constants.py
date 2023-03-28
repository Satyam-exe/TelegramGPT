import os
import openai
from dotenv import load_dotenv

from bot.constants import bot

load_dotenv('../.env')


def set_openai_api_key():
    openai.api_key = os.environ.get('OPENAI_API_KEY')


GET_FILE_URL = lambda path: f"https://api.telegram.org/file/bot{bot.token}/{path}"
