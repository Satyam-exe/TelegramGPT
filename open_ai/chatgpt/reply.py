import openai
import pymongo

from open_ai.chatgpt.constant_messages import start_message
from db.config import messages_col


def get_response(content, user_id):
    messages_to_send = [{"role": "system", "content": start_message}]
    cursor = messages_col.find({'user_id': user_id}).sort([("time", pymongo.DESCENDING)]).limit(10)
    for doc in cursor:
        if not doc['is_revoked']:
            messages_to_send.insert(1, {"role": "user", "content": doc['message']})
            messages_to_send.insert(2, {"role": "assistant", "content": doc['reply']})
    messages_to_send.append({"role": "user", "content": content})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages_to_send
    )
    print(messages_to_send)
    return response


def get_chatgpt_reply(content, user_id):
    response = get_response(content, user_id)
    return response.get('choices')[0].get('message').get('content')
