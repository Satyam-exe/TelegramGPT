import telebot.types


def start_message_reply(message: telebot.types.Message):
    return f"""
Welcome to TelegramGPT, {message.from_user.full_name}!
Please continue by typing anything, and you shall receive an artificially generated reply. Instead of texting, you \
could also send a voice message, and you shall receive a reply.

If you leave, you can continue the same conversation once back. 
If you wish to start a new conversation, type \'/clearcontext\', or you could also type \'/start\' again. 

To generate images, use the /img command in this way:
    /img <prompt> size=<size>
Here, prompt is the description of the image that you want, and size is an optional parameter with available sizes \
256x256, 512x512, and 1024x1024.

You can also get songs as audio files. To do so, use the /music command in this way:
    /music <song>
Here, 'song' is the name of the song you wish to be sent.

This is still quite underdeveloped, so there might be some issues. Wishing you a great experience!
Maybe try \'Good Morning, TelegramGPT\'?
"""


too_many_requests_message = 'Too many requests recieved. The reply may be delayed.'

context_cleared_message = 'The context of the previous conversation has been successfully cleared.'

invalid_size_message = 'Please enter a valid size. [256x256, 512x512, 1024x1024]'

empty_voice_message = 'The voice message sent is empty, please speak something.'

empty_img_prompt_message = 'Please enter a prompt after the /img command.'

empty_music_query_message = 'Please enter a query after the /music command.'

invalid_music_type_message = \
    'Please enter a valid type. [songs, videos, albums, artists, playlists, community_playlists, featured_playlists]'
