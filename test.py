# import required modules
import subprocess
import os
import librosa
from matplotlib import pyplot as plt
# convert mp3 to wav file
filename ="ranking.mp3"

# if os.path.exists(filename):
#     print("file exists")
# else:
#     print("file did not exist")

# input_file = "purcel.mp3"
# print(input_file)
# subprocess.call(['C:/ffmpeg/bin/ffmpeg.exe', '-i',input_file,
#                  'pos.wav'])



import pyaudio
import numpy as np
import pylab
import time
import wave

from threading import Thread
RATE = 44100
CHUNK = int(RATE/20) # RATE / number of updates per second


def soundplot(stream):
    t1=time.time()
    data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
    pylab.plot(data)
    pylab.title(i)
    pylab.grid()
    pylab.axis([0,len(data),-2**16/2,2**16/2])
    pylab.savefig("03.png",dpi=50)
    pylab.close('all')
    print("took %.02f ms"%((time.time()-t1)*1000))

def run():
    global i
    p=pyaudio.PyAudio()
    stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
                  frames_per_buffer=CHUNK)
    for i in range(int(20*RATE/CHUNK)): #do this for 10 seconds
        soundplot(stream)
    stream.stop_stream()
    stream.close()
    p.terminate()

def player(filename):
	# chunk = 1024
    # Open the soaudio/sound file
    # filename = 'fire.wav'
    af = wave.open(filename, 'rb')
    pa = pyaudio.PyAudio()
    chunk = 1024
    stream = pa.open(format = pa.get_format_from_width(af.getsampwidth()),
                    channels = af.getnchannels(),
                    rate = af.getframerate(),
                    output = True)
    # Read data in chunks
    rd_data = af.readframes(chunk)
    start_time = time.perf_counter ()

    while rd_data != '':
        stream.write(rd_data)
        rd_data = af.readframes(chunk)
        end_time = time.perf_counter ()
        print(int(end_time-start_time))
        if int(end_time-start_time)==30:
            break
    # return rd_data
    stream.stop_stream()
    stream.close()
    pa.terminate()
