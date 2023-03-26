import telebot.types


def start_message_reply(message: telebot.types.Message):
    return f"""
Welcome to TelegramGPT, {message.from_user.full_name}!
Please continue by typing anything, and you shall receive an artificially generated reply. 
If you leave, you can continue the same conversation once back. If you wish to start a new conversation, type \
\'/start\' again. This is still quite underdeveloped, so there might be some issues. Wishing you a great experience!
Maybe try \'Good Morning, TelegramGPT\'?
"""

