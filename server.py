import socket
import cv2
import pickle
import struct

from time import sleep

HOST = socket.gethostbyname(socket.gethostname())
PORT = int(input("PORT: "))
RECV_SIZE = 8192

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created ✅')

s.bind((HOST, PORT))
print('Socket bind complete ✅\n')

print(f"PORT - {PORT}\nHOST - {HOST}\nRECV_SIZE - {RECV_SIZE}\n")

s.listen(20)
print('Socket now listening 🎲')


conn, addr = s.accept()

data = b''
payload_size = struct.calcsize("L")

while True:
    while len(data) < payload_size:
        data += conn.recv(RECV_SIZE)
    packed_msg_size = data[:payload_size]

    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0]

    while len(data) < msg_size:
        data += conn.recv(RECV_SIZE)
    frame_data = data[:msg_size]
    data = data[msg_size:]

    frame = pickle.loads(frame_data)

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2.imshow('Window', frame)
    cv2.waitKey(10)