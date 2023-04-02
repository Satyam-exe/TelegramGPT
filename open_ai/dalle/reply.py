import openai

from db.db import get_api_key


def get_response(user_id, prompt, size):
    api_key = get_api_key(user_id=user_id, key_type='openai')
    response = openai.Image.create(
        prompt=prompt,
        size=size,
        n=1,
        api_key=api_key
    )
    return response


def get_image_url(user_id, prompt, size):
    response = get_response(user_id, prompt, size)
    img_url = response.get('data')[0].get('url')
    return img_url
