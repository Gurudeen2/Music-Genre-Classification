import json,os,random,sys,math,librosa,subprocess
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow.keras as keras
import matplotlib.pyplot as plt
from os import path



def convert_input(audio,track_duration):
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

model = keras.models.load_model('genre_of_music_cnn.h5')
# genre_of_music = {0:'hiphop',1:'country',2:'jazz',3:'classical',4:'metal',5:'pop',6:'rock',7:'blues',8:'raggae',9:'disco'}
genre_of_music = {0:'others',1:'country',2:'others',3:'classical',4:'others',5:'others',6:'others',7:'blues',8:'others',9:'others'}



new_input_mfcc = convert_input('pos.wav',30)
print(type(new_input_mfcc))
X_to_predict  = new_input_mfcc[np.newaxis,...,np.newaxis]
print(X_to_predict.shape)
prediction = model.predict(X_to_predict)
predicted_index = np.argmax(prediction,axis=1)
result = genre_of_music[int(predicted_index)]
print('Predicted Genres:',result)