import socket
import cv2
import pickle
import struct
from colorama import Fore
from os import system, path

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

class Server:
    def __init__(self):
        self.HOST = socket.gethostbyname(socket.gethostname())
        self.PORT = int(input("PORT: "))
        system("cls")
    
    def build(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind(("", self.PORT))
            self.sock.listen(20)

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
    
    def getscreen(self):
        RECV_SIZE = 33554432
        SCREEN_SIZE = (1440, 900)
        filename_video = "video1.avi"
        data = b''
        payload_size = struct.calcsize("L")

        while path.exists(filename_video):
            index = filename_video[5:-4]
            filename_video = filename_video[:-5] + str(int(index) + 1) + ".avi"

        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        out = cv2.VideoWriter(filename=filename_video, fourcc=fourcc, fps=15.0, frameSize=(SCREEN_SIZE))

        while True:
            while len(data) < payload_size:
                data += self.conn.recv(RECV_SIZE)
            packed_msg_size = data[:payload_size]

            data = data[payload_size:]
            msg_size = struct.unpack("L", packed_msg_size)[0]

            while len(data) < msg_size:
                data += self.conn.recv(RECV_SIZE)
            frame_data = data[:msg_size]
            data = data[msg_size:]

            frame = pickle.loads(frame_data)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            out.write(frame)
            cv2.imshow('Window', frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

        cv2.destroyAllWindows()
        self.conn.close()

server = Server()
server.build()
server.getscreen()