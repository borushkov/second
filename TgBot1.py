import telebot
from telebot import types
import config
from extensions import *
bot = telebot.TeleBot(config.TOKEN)
@bot.message_handler(commands=["start", "help"])
def help(message: telebot.types.Message):
    text = f"Доброго времени суток,{message.chat.username}!\nДля старта работы бота введите комманду:/value"
    bot.reply_to(message, text) 
@bot.message_handler(commands=['value'])
def button_message(message):
    text = "Доступные валюты:"
    bot.send_message(message.chat.id,text)
    for i in config.keys.keys():
        bot.send_message(message.chat.id, i)
    bot.send_message(message.chat.id, "Для перевода одной валюты в другую напишите текст в формате:\n доллар евро 1")
@bot.message_handler(content_types=["text"])
def convert(message: telebot.types.Message):
    try:
        values2 = message.text.split(" ")
        values = [x.lower() for x in values2]
        if len(values) != 3:
            raise APIException("Слишком много параметров")
        base,quote,amount = values
        total_base = CryptoConverter.get_price(quote,base,amount)
    except APIException as e:
        bot.reply_to(message, f"Ошибка пользователя\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду\n{e}")
    else:
        text = f"Цена {amount} {base} в {quote} - {total_base}" 
        bot.send_message(message.chat.id, text)
bot.infinity_polling()
