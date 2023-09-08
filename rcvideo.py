import numpy as np
import pyautogui
import cv2
import os
import time

from ctypes  import windll

width = windll.user32.GetSystemMetrics(0)
height = windll.user32.GetSystemMetrics(1)

filename_video = "video1.avi"


SREEN_SIZE = (width, height)
fourcc = cv2.VideoWriter_fourcc(*"XVID")

while True:
    stop_time = round(time.time()) + 60
    
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

