import os

import pymongo
from dotenv import load_dotenv

load_dotenv('../.env')

client = pymongo.MongoClient(f"mongodb+srv://satyam2007v:{os.environ.get('MONGODB_PASSWORD')}@telegramgpt.tbshaua.mongodb.net/?retryWrites=true&w=majority")
db = client['telegramgpt']
messages_col = db['messages']
images_col = db['images']