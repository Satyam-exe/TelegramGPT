import openai


def get_response(prompt, size):
    response = openai.Image.create(
        prompt=prompt,
        size=size,
        n=1
    )
    return response


def get_image_url(prompt, size):
    response = get_response(prompt, size)
    img_url = response.get('data')[0].get('url')
    return img_url
