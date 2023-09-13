import pickle
import numpy as np
import os
import random 

cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory
print("Files in %r: %s" % (cwd, files)) 

from jazz_rnn.utils.music.vectorXmlConverter import *

#python jazz_rnn/A_data_prep/durationpitch.py

'''
old non-pitch12: 
'''

maxPitch = 97 + 7 #104
minPitch = 36 - 5 #31 ; so lowest note 0==31==G 
REST_SYMBOL = maxPitch+1-minPitch #74
EOS_SYMBOL = REST_SYMBOL+1 #75
EOS_VECTOR = [EOS_SYMBOL] + [0] * 30


maxPitch12 = 71 
minPitch12 = 60 #so lowest note 0==60==C
REST_SYMBOL12 = maxPitch12+1-minPitch12 #12
EOS_SYMBOL12 = REST_SYMBOL12+1 #13
EOS_VECTOR12 = [EOS_SYMBOL12] + [0] * 30

#MUST FIX TRANSPOSITION SO THAT IT DOESNT OVERFLOW maxPitch and minPitch 

def main(): 

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

    for i in range(len(songData)):
        for j in range(len(songData[i])):
            songData[i][j][0]-=minPitch
            if songData[i][j][0]==68.0: #rests are 68 in the pickle, but the code in dataprocessing now produces 69. 
                songData[i][j][0]=REST_SYMBOL
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

def main2pitch12(): 

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

    for i in range(len(songData)):
        for j in range(len(songData[i])):
            if songData[i][j][0]==99.0:
                songData[i][j][0]=REST_SYMBOL12
            else:
                songData[i][j][0]=songData[i][j][0]%12
            
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
            
        songData[i].append(EOS_VECTOR12)
        if i==0:
            print(songData[i])
        
    sorted_durfreq = sorted(durfreq.items(), key=lambda x:x[0])
    sorted_pitchfreq = sorted(pitchfreq.items(), key=lambda x:x[0])
    sorted_offsetfreq = sorted(offsetfreq.items(), key=lambda x:x[0])

    uniquedurs = [a for a,b in sorted_durfreq]

    converter = VectorXmlConverter(uniquedurs)

    train_data = []
    test_data = []
    for i in range(len(songData)):
        for j in range(len(songData[i])):
            if songData[i][j][0] != EOS_SYMBOL12:
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
    
    with open(os.path.join(outdir, 'converter_and_duration12.pkl'), 'wb') as fp:
        pickle.dump(converter, fp)
        pickle.dump(uniquedurs, fp)
    with open(os.path.join(outdir, 'train12.pkl'), 'wb') as fp:
        pickle.dump(train_data, fp)
    with open(os.path.join(outdir, 'val12.pkl'), 'wb') as fp:
        pickle.dump(test_data, fp)
    
    #plug all the holes in train.py 
    

if __name__ == "__main__":
    main()

'''
[(1, 1320), (2, 6901), (3, 18973), (4, 18075), (5, 20787), (6, 22583), (7, 14923), (8, 7367), (9, 3442), (10, 1935), (11, 1629), (12, 1754), (13, 1135), (14, 888), (15, 837), (16, 747), (17, 743), (18, 725), (19, 634), (20, 520), (21, 420), (22, 402), (23, 404), (24, 398), (25, 330), (26, 265), (27, 222), (28, 190), (29, 193), (30, 196), (31, 200), (32, 167), (33, 142), (34, 144), (35, 147), (36, 146), (37, 120), (38, 114), (39, 132), (40, 87), (41, 86), (42, 100), (43, 84), (44, 85), (45, 77), (46, 78), (47, 52), (48, 69), (49, 65), (50, 56), (51, 53), (52, 38), (53, 40), (54, 27), (55, 31), (56, 26), (57, 24), (58, 23), (59, 27), (60, 36), (61, 18), (62, 25), (63, 10), (64, 18), (65, 13), (66, 11), (67, 10), (68, 17), (69, 10), (70, 12), (71, 9), (72, 4), (73, 16), (74, 7), (75, 3), (76, 6), (77, 3), (78, 3), (79, 4), (80, 2), (81, 3), (83, 1), (84, 3), (87, 1), (88, 2), (90, 2), (91, 2), (92, 1)]
pitchfreq:
[(5, 1), (6, 1), (7, 3), (8, 2), (9, 1), (10, 8), (11, 3), (12, 32), (13, 71), (14, 103), (15, 199), (16, 117), (17, 364), (18, 254), (19, 616), (20, 762), (21, 778), (22, 1924), (23, 1002), (24, 2681), (25, 2073), (26, 2554), (27, 4360), (28, 2192), (29, 5532), (30, 3556), (31, 5690), (32, 5963), (33, 4899), (34, 8649), (35, 3684), (36, 7953), (37, 5573), (38, 5486), (39, 6687), (40, 3100), (41, 5575), (42, 2821), (43, 3497), (44, 2745), (45, 1721), (46, 2377), (47, 816), (48, 1517), (49, 889), (50, 566), (51, 593), (52, 223), (53, 400), (54, 151), (55, 172), (56, 112), (57, 44), (58, 42), (59, 21), (60, 8), (61, 6), (62, 1), (63, 2), (64, 1), (65, 1), (66, 1), (74, 20455)]
offsetfreq:
[(0, 5610), (1, 3539), (2, 2718), (3, 2106), (4, 1837), (5, 1847), (6, 2348), (7, 2952), (8, 3091), (9, 2880), (10, 2276), (11, 957), (12, 5224), (13, 3358), (14, 2633), (15, 2064), (16, 1961), (17, 2045), (18, 2746), (19, 3182), (20, 3365), (21, 3104), (22, 2427), (23, 944), (24, 5575), (25, 3641), (26, 2826), (27, 2223), (28, 1839), (29, 1996), (30, 2468), (31, 2998), (32, 3190), (33, 2964), (34, 2292), (35, 1065), (36, 5398), (37, 3464), (38, 2648), (39, 2143), (40, 1942), (41, 2185), (42, 2728), (43, 3137), (44, 3431), (45, 3112), (46, 2224), (47, 927)]
'''