from tkinter import *
from tkinter import ttk,messagebox,filedialog
from distutils.dir_util import copy_tree
from PIL import ImageTk,Image
from ttkthemes import ThemedTk as team
import sys
import sqlite3
import json
import os
import shutil,subprocess
from shutil import copyfile,copy2,copy,move
from test import player
import pyaudio
import numpy as np
import pylab
import time
import wave
import json,os,random,sys,math,librosa,subprocess
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow.keras as keras
import matplotlib.pyplot as plt
from os import path
# from test import run

class Check_music():

    def __init__(self,root):
        self.root = root
        self.root.title("Check writting")
        self.root.geometry("800x500+300+45")
        self.root.configure(background="black")
        self.root.resizable(False,False)
        self.RATE = 44100
        self.CHUNK = int(self.RATE/20)
        
    
        #frame
        dashboard_frame = ttk.Frame(self.root)
        dashboard_frame.place(x=0,y=0,height=660,width=1000)
        
        User_label = Label(dashboard_frame,text="CS/HND/F19/2643",font=("Goudy old style",15,"bold")).place(x=0,y=0,width=800)
        #logout
        self.logout =PhotoImage(file="image/logout.png")

        logout =Button(User_label,image=self.logout,command=self.cancel,bd=0).place(x=730,y=0,height=30,width=60)

        
        
        #frame
        Frame_login = Frame(dashboard_frame,bg="black")
        Frame_login.place(x=0,y=30,height=480,width=800)
        # title = Label(Frame_login,text="Check Genre",font=("Impact",20,"bold"),fg="white",bg="black").place(x=170,y=10)
      
       
        self.photo=PhotoImage(file="image/2.png") 
        self.matric =Button(Frame_login,image=self.photo,font=("times new roman",15),bg="lightgray").place(x=100,y=60,height=300,width=600)
        # self.matric.configure(image=self.photo)

        new_folder = Button(Frame_login,text="Load Music",font=("Goudy old style",15,"bold"),fg="white",bg="black",command=self.load_image).place(x=100,y=400,width=250)

        Check_digit_writting_btn = Button(Frame_login,text="CLASSIFY",font=("Goudy old style",15,"bold"),fg="white",bg="black",command=self.play_music).place(x=450,y=400,width=250)


        # check_alpha_writting_btn = Button(Frame_login,text="Predict",command=self.predict_audio,font=("Goudy old style",15,"bold"),fg="white",bg="black").place(x=540,y=400,width=250)


    def load_image(self):
        # run()
        # pass
        self.Add_folder()

    def Add_folder(self):
        # global photo
        global filename
        filename = filedialog.askopenfilename()
        # photo=PhotoImage(file="image/2.png")
        # self.matric.configure(image=photo)
        if os.path.exists:
            os.remove('predict.wav')
        subprocess.call(['ffmpeg/bin/ffmpeg.exe', '-i',filename,
                 'predict.wav'])
        # self.play_music()
        
    
    

    def soundplot(self,stream):
        t1=time.time()
        data = np.fromstring(stream.read(self.CHUNK),dtype=np.int16)
        pylab.plot(data)
        pylab.title(i)
        pylab.grid()
        pylab.axis([0,len(data),-2**16/2,2**16/2])
        pylab.savefig("image/03.png",dpi=50)
        # pylab.show()
        pylab.close('all')
        # photo=PhotoImage(file="image/03.png")
        # self.matric.configure(image=photo)
        print("took %.02f ms"%((time.time()-t1)*1000))
        

    def run(self):
        global i
        p=pyaudio.PyAudio()
        stream=p.open(format=pyaudio.paInt16,channels=1,rate=self.RATE,input=True,
                    frames_per_buffer=self.CHUNK)
        for i in range(int(20*self.RATE/self.CHUNK)): #do this for 10 seconds
            self.soundplot(stream)
        stream.stop_stream()
        stream.close()
        p.terminate()



    def play_music(self):
        player('predict.wav')
        self.predict_audio()


    def convert_input(self,audio,track_duration):
        SAMPLE_RATE = 22050
        NUM_MFCC = 13
        NUM_FFT = 2048
        HOP_LENGTH = 512
        TRACK_DURATION = track_duration
        SAMPLE_PER_TRACK = SAMPLE_RATE *TRACK_DURATION
        NUM_SEGMENTS=10
        sample_per_segment = int(SAMPLE_PER_TRACK/NUM_SEGMENTS)
        num_mfcc_vector_per_segment = math.ceil(sample_per_segment/HOP_LENGTH) 
        signal, sample_rate = librosa.load(audio,sr=SAMPLE_RATE)

        for i in range(10):
            start = sample_per_segment * i
            end = start + sample_per_segment
            mfcc =librosa.feature.mfcc(signal[start:end], sample_rate,n_mfcc=NUM_MFCC,n_fft=NUM_FFT,hop_length=HOP_LENGTH)
            mfcc = mfcc.T
            return mfcc

    def predict_audio(self):
        model = keras.models.load_model('model/genre_of_music_cnn.h5')
        # genre_of_music = {0:'hiphop',1:'country',2:'jazz',3:'classical',4:'metal',5:'pop',6:'rock',7:'blues',8:'raggae',9:'disco'}
        genre_of_music = {0:'others',1:'country',2:'others',3:'classical',4:'others',5:'others',6:'others',7:'blues',8:'others',9:'others'}
        new_input_mfcc = self.convert_input('predict.wav',30)
        # print(type(new_input_mfcc))
        X_to_predict  = new_input_mfcc[np.newaxis,...,np.newaxis]
        print(X_to_predict.shape)
        prediction = model.predict(X_to_predict)
        predicted_index = np.argmax(prediction,axis=1)
        result = genre_of_music[int(predicted_index)]
        print('Predicted Genres:',result)
        self.show_result("Uploaded Music is ",result)


    def cancel(self):
        Msg=messagebox.askquestion('Exist Application','Are you sure you want to exist',icon="info")
        if Msg == "yes":
            self.root.destroy()

    
        
    def show_result(self,written,result):
        root = team(theme="black")
        root.title("Update")
        root.geometry("800x500+200+60")          
        root.resizable(False,False)
        root_frame = ttk.Frame(root)
        root_frame.place(x=0,y=0,height=640,width=1000)

        update_frame = Frame(root_frame,bg="black")
        update_frame.place(x=150,y=30,height=420,width=460)
        update_title = Label(update_frame,text=written,font=("Impact",25,"bold"),fg="white",bg="black").place(x=70,y=60)
        result_label = Label(update_frame,text=result,font=("Impact",35,"bold"),fg="black",bg="white",height=4,width=12).place(x=75,y=150)




     
       


if __name__ == "__main__":
   root = team(theme="black")
   obj = Check_music(root)
   root.mainloop()
