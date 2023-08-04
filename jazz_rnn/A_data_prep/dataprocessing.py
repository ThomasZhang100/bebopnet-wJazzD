'''
Preproccessing: 
Reading the wjazzd db into 3d datastructure:
array of vectors including pitch, duration, chord data for each note in each song
3d array/numpy array (songs, notes, notedata)

data structure saved to pickle file for use in training 
'''

import sqlite3
import numpy as np
from chordprocessing import chordString_2_vector
import pickle

DUR_PER_BEAT = 12

con = sqlite3.connect("wjazzd.db")
cur = con.cursor() # cursor used object used to query 

num_songs = len(cur.execute('SELECT * FROM solo_info').fetchall())
#print(num_songs)


songdata = []
uniquedurations = []
zerosongs = []
'''
cur.execute('SELECT pitch FROM melody')
pitches = cur.fetchall()
'''

maxPitch = 97.0
minPitch = 36.0 
pitchTop = maxPitch-minPitch
restPitch = maxPitch+1
    
'''
print(allchords)

{'6': 682, '7': 12222, '-7': 6762, '': 1376, '7alt': 164, 'j7': 3052, 'm7b5': 1117, '79b': 612,
'-': 810, '79#': 152, 'o7': 201, 'NC': 401, '-6': 394, 'o': 334, '79': 218, 'sus7': 371, '+7': 219,
    '7913': 105, '7911#': 131, 'sus79': 30, '69': 67, 'sus': 311, '-69': 49, '-79b': 1, '-j7': 34, 
    'j79': 34, 'j7911#': 174, '79b13b': 19, '+7911#': 2, '7913b': 8, '-79': 116, '79#13': 2, 
    '+79b': 1, '-7911': 105, '79b13': 7, 'j79#11#': 1, 'sus7913': 143, '6911#': 5, '+79': 5, 
    '+j7': 7, '+': 47, '+79#': 22, '79#11#': 8, 'j79#': 2, '-j7913': 8, '-j7911#': 8, 
    '-7913': 8, '7911': 1}
'''

#esclude non 4/4 indeces 

'''
cur.execute('SELECT signature, melid FROM solo_info')
signatures = cur.fetchall()
NCsongs=[]
for signature, melid in signatures:
    if signature!="4/4" and melid not in NCsongs:
        NCsongs.append(melid)
print(NCsongs)
'''


badsongs = [5, 6, 7, 10, 13, 20, 25, 32, 33, 34, 35, 36, 38, 39, 41, 53, 54, 56, 57, 62, 78, 79, 80, 81, 82, 83, 85, 86, 96, 100, 104, 108, 112, 113, 114, 116, 117, 118, 120, 122, 124, 135, 137, 140, 141, 145, 146, 152, 153, 154, 155, 157, 158, 165, 168, 174, 181, 195, 199, 200, 201, 205, 206, 207, 208, 210, 217, 218, 219, 224, 226, 230, 232, 233, 247, 254, 256, 257, 274, 279, 291, 303, 304, 305, 307, 316, 318, 319, 327, 333, 342, 354, 355, 361, 376, 377, 381, 382, 383, 387, 391, 393, 396, 398, 400, 414, 419, 430, 432, 435, 436, 438, 441, 443]

excludedSongs = [50, 66, 84, 147, 184, 185, 187, 188, 214, 215, 227, 228, 229, 246, 308, 322, 336, 337, 338, 339, 340, 403, 404, 405, 407, 411, 412, 431, 433, 434, 439] # duration quantizing not narrowed
excludedSongs2 = [5, 6, 7, 10, 13, 20, 25, 32, 33, 34, 35, 36, 38, 39, 41, 50, 53, 54, 56, 57, 62, 66, 78, 79, 80, 81, 82, 83, 84, 85, 86, 96, 100, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 116, 117, 118, 120, 122, 124, 135, 137, 140, 141, 145, 146, 147, 152, 153, 154, 155, 157, 158, 165, 168, 174, 181, 184, 185, 187, 188, 195, 199, 200, 201, 205, 206, 207, 208, 210, 214, 215, 217, 218, 219, 224, 226, 227, 228, 229, 230, 232, 233, 246, 247, 254, 256, 257, 274, 279, 291, 303, 304, 305, 307, 308, 316, 318, 319, 322, 327, 333, 336, 337, 338, 339, 340, 342, 354, 355, 361, 376, 377, 381, 382, 383, 387, 391, 393, 396, 398, 400, 403, 404, 405, 407, 411, 412, 414, 419, 430, 431, 432, 433, 434, 435, 436, 438, 439, 441, 443]

x = [183, 225, 258, 276, 309]

'''
for i in x:
    if i not in excludedSongs2:
        excludedSongs2.append(i)
        
print(excludedSongs2)
'''


goodSongs = []
for i in range(1,num_songs+1):
    if i not in excludedSongs2:
        goodSongs.append(i)

file = open('validSongs.pkl', 'wb')
pickle.dump(goodSongs, file)
file.close()

print("num songs excluded:", len(excludedSongs2))


def getSongNotes(melid, uniquedurs):
    cur.execute('SELECT eventid, bar, beat, onset, duration, beatdur, pitch FROM melody WHERE melid=? AND bar>0', (melid,))
    rows = cur.fetchall()
    first_two_beats = cur.execute('SELECT onset FROM beats WHERE melid=? AND bar>0 LIMIT 2', (melid,)).fetchall()
    approx_beat_dur = first_two_beats[1][0]-first_two_beats[0][0]
    songnotes = []
    end_measure_offset=0
    end_bar=1
    end_beat=1
    for row in rows:
        note = list(row)
        bar, note_beat, onset, duration, beatdur, pitch = note[1], note[2], note[3], note[4], note[5], note[6]
        cur.execute('SELECT onset, chord FROM beats WHERE melid=? AND bar=? AND beat=?', (melid, bar, note_beat))

        beat_onset, chord = cur.fetchone()
        note_end = onset + duration

        #calculating the offset of the beginning of the note with respect to its beat and measure
        onset = beat_onset if beat_onset>onset else onset
        note_beg_offset = round((onset-beat_onset)/beatdur*DUR_PER_BEAT)

        #just in case we round up to the next beat 
        if note_beg_offset>(onset-beat_onset)/beatdur*DUR_PER_BEAT and note_beg_offset%DUR_PER_BEAT==0:
            #print("rounded beginning up to next beat")
            note_beg_offset=0
            note_beat+=1
            if note_beat>4:
                note_beat=1
                bar+=1
            chord = cur.execute('SELECT chord FROM beats WHERE melid=? AND bar=? AND beat=?', (melid, bar, note_beat)).fetchone()[0]

        measure_offset = (note_beat-1)*DUR_PER_BEAT+note_beg_offset

        #if there is a gap between this note and the previous one, add a rest note to array
        #if rest_duration smaller than certain number, add rest duration to previous note
        if not (measure_offset==end_measure_offset and bar == end_bar):
            #if bar<6:
                #print("bar:",bar,"end_bar:",end_bar,"measure_offset:",measure_offset,"end_measure_offset:", end_measure_offset)
            if (bar-end_bar>0):
                rest_duration = DUR_PER_BEAT * 4 - end_measure_offset + measure_offset
            else:
                rest_duration = measure_offset - end_measure_offset
            if rest_duration<3 and len(songnotes)!=0:
                songnotes[-1][1]+=rest_duration
            else:
                try:
                    rest_chord = cur.execute('SELECT chord FROM beats WHERE melid=? AND bar=? AND beat=?', (melid, end_bar, end_beat)).fetchone()[0]
                except:
                    print("end_bar:", end_bar, "end_beat:", end_beat)
                rest_fournotes, rest_chordtype = chordString_2_vector(rest_chord)
                songnotes.append([restPitch,rest_duration,end_measure_offset]+rest_fournotes+[rest_chordtype])
                if rest_duration not in uniquedurs:
                    uniquedurs.append(rest_duration)
                #print("rest duration:", rest_duration, "chord:", rest_chord, "measure_offset:", end_measure_offset)
            

        fournotes, chordtype = chordString_2_vector(chord)


        #check for notes extending past one beat
        num_beats_apart=0
        end_beat_onset=beat_onset
        end_beat = note_beat
        end_bar = bar
        while True:
            end_beat+=1
            if end_beat > 4:
                end_beat=1
                end_bar+=1
            cur.execute('SELECT onset FROM beats WHERE melid=? AND bar=? AND beat=?', (melid, end_bar, end_beat))
            try:
                next_beat_onset = cur.fetchone()[0]
            except:
                next_beat_onset = end_beat_onset + approx_beat_dur
            if note_end<next_beat_onset:
                break
            else:
                num_beats_apart+=1
                end_beat_onset=next_beat_onset
        
        #calculating the offset of the note end with respect to its beat
        note_end_offset_raw = (note_end-end_beat_onset)/(next_beat_onset-end_beat_onset)
        note_end_offset = round(note_end_offset_raw*DUR_PER_BEAT)
        #just in case we round up to the next beat 
        if note_end_offset>note_end_offset_raw*DUR_PER_BEAT and note_end_offset%DUR_PER_BEAT==0:
            #print("rounded end up to next beat")
            note_end_offset=0
            num_beats_apart+=1
        else:
            #correcting the position of the end of the note to calculate the measure offset of the end of the note
            end_beat-=1
            if end_beat < 1:
                end_beat=4
                end_bar-=1

        end_measure_offset = (end_beat-1)*DUR_PER_BEAT+note_end_offset

        #calculating the rounded duration of the note (quantized by DUR_PER_BEAT)
        if end_bar-bar>0:
            rounded_duration = DUR_PER_BEAT * 4 - measure_offset + end_measure_offset
        else: 
            rounded_duration = end_measure_offset - measure_offset
        #rounded_duration = DUR_PER_BEAT * num_beats_apart - note_beg_offset + note_end_offset

        if rounded_duration not in uniquedurs:
            uniquedurs.append(rounded_duration)

      
        #print('melid:',i,'bar:',bar,'beat:',note_beat)
        #print("duration:",rounded_duration,"pitch:",int(pitch-minPitch),"chord:",chord,"measure_offset:", measure_offset)
        songnotes.append([int(pitch),rounded_duration,measure_offset]+fournotes+[chordtype])
        #add note to array 

    return songnotes

for i in range(1, num_songs+1):
    if i in excludedSongs2:
        continue

    print("song:",i)
    songNotes = getSongNotes(i, uniquedurations)
    songdata.append(songNotes)

durationslist = sorted(uniquedurations)
print("unique durations:", durationslist)

fp = open('datatest.pkl', 'wb')
pickle.dump(songdata, fp)
fp.close()

con.close()

'''
unique durations: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35,
   36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 
   54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71,
     72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88,
       89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103,
         104, 105, 108, 109, 112, 113, 114, 116, 117, 121, 124, 126, 127,
           128, 129, 130, 131, 132, 134, 136, 137, 139, 140, 142, 144, 145,
             153, 157, 160, 163, 171, 173, 178, 185, 186, 193, 195, 202, 203, 
             213, 219, 225, 227, 261, 323, 327, 329, 331, 355, 365, 394, 552]

'''

