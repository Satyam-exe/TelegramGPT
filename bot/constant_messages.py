import telebot.types


def start_message_reply(message: telebot.types.Message):
    return f"""
Welcome to TelegramGPT, {message.from_user.full_name}!
Please continue by typing anything, and you shall receive an artificially generated reply. 

If you leave, you can continue the same conversation once back. 
If you wish to start a new conversation, type \'/clearcontext\', or you could also type \'/start\' again. 

To generate images, use the **\'/images\'** command in this way:
    /img <prompt> size=<size>
    Here, prompt is the description of the image that you want, and size is an optional parameter with available sizes \
    256x256, 512x512, and 1024x1024.

This is still quite underdeveloped, so there might be some issues. Wishing you a great experience!
Maybe try \'Good Morning, TelegramGPT\'?
"""


too_many_requests_message = 'Too many requests recieved. The reply may be delayed.'

context_cleared_message = 'The context of the previous conversation has been successfully cleared.'
