import os
import openai
from dotenv import load_dotenv

load_dotenv('../.env')


def set_openai_api_key():
    openai.api_key = os.environ.get('OPENAI_API_KEY')
