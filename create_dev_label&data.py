import os
from scipy import signal
from matplotlib import mlab
import wave
import numpy as np
import soundfile as sf
import struct
filelist = []
# window path
# path = 
# audio_path = 
# savepath = 
# linux path
path = 
audio_path = 
savepath = 

filename1 = os.path.join(path,'fold1_train.txt')
filename2 = os.path.join(path,'fold1_evaluate.txt')
wav_index = []
label_dict = {'bus': 0, 'cafe/restaurant': 1, 'car': 2, 'city_center': 3, 'forest_path': 4, 'grocery_store':5,
    'home': 6, 'beach': 7, 'library': 8, 'metro_station': 9, 'office': 10, 'residential_area': 11,
    'train': 12, 'tram': 13, 'park': 14}

# read the name and label in fold1_train.txt (880 examples)
with open(filename1,'r') as f:
    file_propertys = f.readlines()
    for file_property in file_propertys:
        wavename = file_property.split()
        wav_index.append(wavename)

# read the name and label in fold1_evaluate.txt (290 examples)
with open(filename2,'r') as f:
    file_propertys = f.readlines()
    for file_property in file_propertys:
        wavename = file_property.split()
        wav_index.append(wavename)

# for each wave file, find the only label from the label txt files.
# we don't distinguish the evaluate and training data.
print('the number of files: ',len(wav_index))
i = 0
file_number = 1
start_mark = True
for audio_filename in os.listdir(audio_path):

    data_dir = os.path.join(audio_path,audio_filename)
    data, samplerate = sf.read(data_dir)
    data = data[:,0]
    spect_tmp,f,t = mlab.specgram(data,window=np.hamming(512),NFFT=512,noverlap=256,mode='magnitude')

    exist = False
    window_number = (spect_tmp.shape[1] - 256) // 64 + 1
    j = 0
    for wav_label in wav_index:
        if audio_filename in wav_label[0]:
            print(audio_filename,wav_label)
            print(label_dict[wav_label[1]])
            label_tmp = np.array([label_dict[wav_label[1]]])
            # print(label_tmp.dtype)
            for j in range(window_number):
                spect_window_tmp = spect_tmp[:,j*64:j*64+257]
                # print(j,spect_window_tmp.shape)
                if start_mark:
                    label_index = label_tmp
                    dataset_full = spect_window_tmp
                    start_mark = False
                else:
                    label_index = np.concatenate((label_index,label_tmp),axis=0)
                    dataset_full = np.concatenate((dataset_full,spect_window_tmp),axis=0)

            spect_window_tmp = spect_tmp[:,spect_tmp.shape[1]-258:spect_tmp.shape[1]-1]
            label_index = np.concatenate((label_index,label_tmp),axis=0)
            dataset_full = np.concatenate((dataset_full,spect_window_tmp),axis=0)
            i = i+1
            print(i)
            exist = True
            break
    if not exist:
        print('no')

    if i % 1 == 0:
        label_index.tofile(os.path.join(savepath,'Devlabel_batch_%d.bin' %file_number))
        dataset_full.tofile(os.path.join(savepath,'DevData_batch_%d.bin' %file_number))
        print(dataset_full.shape,label_index.shape)
        file_number = file_number + 1
        start_mark = True
        print(file_number)
    # if i == 5:
    #     break
# print(label_index)
# print(dataset_full.shape)

# savename = os.path.join(savepath,'Devlabel.bin')
# label_index.tofile(savename)
# dataset_full.tofile(os.path.join(savepath,'DevData.bin'))
