import cv2
import numpy as np
import socket
import sys
import pickle
import struct
import pyautogui
import time
from PIL import Image

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('localhost', 7777))

while True:
    image = pyautogui.screenshot()
    image = image.resize((1100, 650))
    image = np.array(image)
    img = Image.frombytes('RGB', (1100, 650), image)
    data = pickle.dumps(np.array(img))
    clientsocket.sendall(struct.pack("L", len(data)) + data)