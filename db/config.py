import os

import pymongo
from dotenv import load_dotenv

load_dotenv('../.env')

client = pymongo.MongoClient(
    f"mongodb+srv://"
    f"{os.environ.get('MONGODB_USERNAME')}:"
    f"{os.environ.get('MONGODB_PASSWORD')}@"
    f"{os.environ.get('MONGODB_HOST')}/"
    f"?retryWrites=true"
    f"&w=majority"
)
db = client['telegramgpt']
messages_col = db['messages']
images_col = db['images']
voices_col = db['voices']
music_col = db['music']
