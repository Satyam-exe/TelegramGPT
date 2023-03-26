import os

import pymongo
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

client = pymongo.MongoClient(f"mongodb+srv://satyam2007v:{os.environ.get('MONGODB_PASSWORD')}@telegramgpt.tbshaua.mongodb.net/?retryWrites=true&w=majority")
db = client['telegramgpt']
col = db['messages']