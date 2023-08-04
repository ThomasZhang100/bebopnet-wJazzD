import pickle
from music21 import *

maxPitch = 97.0
minPitch = 36.0 
pitchTop = maxPitch-minPitch
restPitch = maxPitch+1

file = open('datatest.pkl', 'rb')
songData = pickle.load(file)
file.close()

file = open('validSongs.pkl', 'rb')
validSongs = pickle.load(file)
file.close()

stream1 = stream.Stream()

i=0
for j in range(len(songData[0])):
    #print(songData[i][j])
    if songData[i][j][0]==restPitch:
        next = note.Rest()
        next.duration.quarterLength = songData[i][j][1]/12.0
    else:
        next = note.Note(songData[i][j][0])
        next.duration.quarterLength = songData[i][j][1]/12.0
    stream1.append(next)

sp = midi.realtime.StreamPlayer(stream1)
sp.play()
    

        