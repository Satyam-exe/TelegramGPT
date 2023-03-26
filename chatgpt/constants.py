import os
import openai
from dotenv import load_dotenv

load_dotenv('../.env')

openai.api_key = os.environ.get('OPENAI_API_KEY')

