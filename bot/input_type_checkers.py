import telebot


def is_normal(message: telebot.types.Message):
    return message.text.isprintable()
