import telebot

from cfg import *

API_TOKEN = "6466690541:AAFfFWUqEbEzZfIOuybgrqHot_hJYBiI-eI"
ADMIN = 804011643

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.send_message(message.chat.id, "Hello i'm Yretra")
    bot.send_message(message.chat.id, cmd)



bot.infinity_polling()