import socket
import cv2
import pickle
import struct

HOST = socket.gethostbyname(socket.gethostname())
PORT = 9111

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bot.send_message(ADMIN, "Socket created.")

s.bind((HOST, PORT))
bot.send_message(ADMIN, "Socket bind complete.")

s.listen(20)
bot.send_message(ADMIN, "Socket now listening.")

conn, addr = s.accept()

data = b''
payload_size = struct.calcsize("L")

while True:
    while len(data) < payload_size:
        data += conn.recv(4096)
        
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0]

    while len(data) < msg_size:
        data += conn.recv(4096)

    frame_data = data[:msg_size]
    data = data[msg_size:]
    frame = pickle.loads(frame_data)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    cv2.imshow('Window', frame)
    cv2.waitKey(10)