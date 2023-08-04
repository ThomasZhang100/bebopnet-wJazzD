import pickle
import numpy as np
import os
import random 

cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory
print("Files in %r: %s" % (cwd, files))

from jazz_rnn.utils.music.vectorXmlConverter import *

#python jazz_rnn/A_data_prep/durationpitch.py

durfreq={}
pitchfreq={}
offsetfreq={}
zerosongs=[]
largedursongs=[]

curdir = 'jazz_rnn/A_data_prep'
outdir = 'results/dataset_pkls'

file = open(os.path.join(curdir, 'datatest.pkl'), 'rb') #if not absolute path detected, open uses relative path from cwd, which is your cwd in the terminal 
songData = pickle.load(file)
file.close()

file = open(os.path.join(curdir, 'validSongs.pkl'), 'rb')
validSongs = pickle.load(file)
file.close()

#test_songs = random.sample(validSongs,40)
train_songs = []
test_songs = [392, 275, 332, 283, 360, 70, 202, 375, 437, 288, 374, 271, 312, 72, 272, 89, 190, 134, 3, 12, 356, 131, 150, 252, 263, 266, 328, 127, 42, 16, 449, 128, 101, 315, 292, 244, 265, 345, 293, 427]
for i in validSongs:
   if i not in test_songs:
       train_songs.append(i)

print(train_songs)
print(test_songs)

maxPitch = 97
minPitch = 36
restPitch = maxPitch+1-minPitch #62
EOS_SYMBOL = restPitch+1 #63 
EOS_VECTOR = [EOS_SYMBOL] + [0] * 30

for i in range(len(songData)):
    for j in range(len(songData[i])):
        songData[i][j][0]-=minPitch
        if songData[i][j][0]==63.0:
            songData[i][j][0]=62
        if songData[i][j][0] in pitchfreq.keys():
            pitchfreq[songData[i][j][0]]+=1
        else:
            pitchfreq[songData[i][j][0]]=1
        if songData[i][j][1] in durfreq.keys():
            durfreq[songData[i][j][1]]+=1
        else:
            durfreq[songData[i][j][1]]=1
        if songData[i][j][2] in offsetfreq.keys():
            offsetfreq[songData[i][j][2]]+=1
        else:
            offsetfreq[songData[i][j][2]]=1
        if songData[i][j][1]>96:
            if validSongs[i] not in largedursongs:
                largedursongs.append(validSongs[i])
            print("duration:",songData[i][j][1])
            print("note num:", j)
            print("song:",validSongs[i])
        fournotes = songData[i][j][3:7]
        chordvec = [0]*13
        for idx in fournotes:
            chordvec[idx]=1
        songData[i][j]=songData[i][j][:3]+[0]*14+chordvec+[songData[i][j][7]]
        
    songData[i].append(EOS_VECTOR)
    if i==0:
        print(songData[i])

sorted_durfreq = sorted(durfreq.items(), key=lambda x:x[0])
sorted_pitchfreq = sorted(pitchfreq.items(), key=lambda x:x[0])
sorted_offsetfreq = sorted(offsetfreq.items(), key=lambda x:x[0])

uniquedurs = [a for a,b in sorted_durfreq]

converter = VectorXmlConverter(uniquedurs)

'''
dur2idx = {0:0}
idx2dur = {0:0}
for i in range(len(uniquedurs)):
    dur2idx[uniquedurs[i]]=i+1
    idx2dur[i+1]=uniquedurs[i]
'''

train_data = []
test_data = []
for i in range(len(songData)):
    for j in range(len(songData[i])):
        if songData[i][j][0] != EOS_SYMBOL:
            songData[i][j][1]=converter.dur_2_ind(songData[i][j][1])
    if validSongs[i] in train_songs:
        train_data.append(songData[i])
    else:
        test_data.append(songData[i])


print("durfreq: len=",len(sorted_durfreq))
print(sorted_durfreq)
print("pitchfreq:")
print(sorted_pitchfreq)
print("offsetfreq:")
print(sorted_offsetfreq)
print(largedursongs)

'''
file = open(os.path.join(outdir, 'data.pkl'), 'wb')
pickle.dump(songData, file)
file.close()
'''

with open(os.path.join(outdir, 'converter_and_duration.pkl'), 'wb') as fp:
    pickle.dump(converter, fp)
    pickle.dump(uniquedurs, fp)
with open(os.path.join(outdir, 'train.pkl'), 'wb') as fp:
    pickle.dump(train_data, fp)
with open(os.path.join(outdir, 'val.pkl'), 'wb') as fp:
    pickle.dump(test_data, fp)
#plug all the holes in train.py 
