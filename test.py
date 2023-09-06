import cv2
import numpy as np
import pyautogui
import moviepy.editor as moviepy
import os


SREEN_SIZE = (1920, 1080)
fourcc = cv2.VideoWriter_fourcc(*"XVID")

out = cv2.VideoWriter(filename=filename_video, fourcc=fourcc, fps=10.0, frameSize=(SREEN_SIZE))

while True:
    img = pyautogui.screenshot()
    frame = np.array(img)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    out.write(frame)
    cv2.imshow("broadcast", frame)
    
    if cv2.waitKey(1) == ord("q"):
        break

cv2.destroyAllWindows()
out.release()

clip = moviepy.VideoFileClip(filename_video)
clip.write_videofile("recorded.mp4", logger=None)

if os.path.isfile(filename_video):
    os.remove(filename_video)
else:
    print('Path is not a file')