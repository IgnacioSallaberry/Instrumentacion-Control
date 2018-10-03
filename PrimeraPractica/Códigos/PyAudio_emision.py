import pyaudio
import audioop
import matplotlib.pyplot as plt
import numpy as np
#from itertools import izip
import wave


FORMAT = pyaudio.paInt16                # We use 16bit format per sample
CHANNELS = 1
RATE = 44100
CHUNK = 1024                            # 1024bytes of data red from a buffer
RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = "file.wav"

audio = pyaudio.PyAudio()

# start Recording
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

frames = []
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
    
#le pusimos la b adelante para transformar todos los strings en bytes.
frames = b"".join(frames)

fig = plt.figure()
s = fig.add_subplot(111)
amplitude = np.fromstring(frames, np.int16)
s.plot(amplitude)
fig.savefig('t.png')

stream.stop_stream()
stream.close()
audio.terminate()

