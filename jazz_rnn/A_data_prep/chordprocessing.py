
chord_2_type = {'7': 0, '7911': 0, '79': 0, 'sus7': 0, 'sus79': 0, '7913': 0, 'sus': 0, 'sus7913': 0,
                '79b': 1, '79b13b': 1, '79b13': 1, '7alt': 1, '79#': 1, '79#13': 1, '7911#': 1,  '79#11#': 1, '7913b': 1, 
                '-7': 2,'-': 2, '-6': 2, '-79b': 2, '-69': 2, '-7913': 2, '-79': 2, '-7911': 2, 
                '6': 3, '': 3, 'j7': 3, '69': 3, 'j79': 3, 'j79#': 3, '6911#': 3, 'j7911#': 3,  'j79#11#': 3,
                'm7b5': 4, 
                 'o7': 5,   'o': 5, 
                 '+7': 6,  '+7911#': 6, '+79b': 6, '+79': 6, '+j7': 6, '+': 6, '+79#': 6,
                 '-j7': 7, '-j7913': 7, '-j7911#': 7
               }

root_char_2_ind = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'E#':5, 'Fb': 4,
                   'F': 5, 'F#': 6, 'Gb': 6,'G': 7, 'G#': 8, 'Ab': 8,
                   'A': 9, 'A#': 10,'Bb': 10, 'B': 11, 'B#':0, 'Cb': 11} #This is accurate to the model's multihot formatting 

type_2_fournotes = [[0,4,7,10],[0,4,7,10],[0,3,7,10],[0,4,7,11],[0,3,6,10],[0,3,6,9],[0,4,8,10],[0,3,7,11]]

def chordString_2_vector(chordString):
    chord, root = removeRoot(chordString)
    chordtype = chord_2_type[chord]
    fournotes = type_2_fournotes[chordtype]
    root_num = root_char_2_ind[root]
    fournotes = [(n+root_num)%12 for n in fournotes]
    try:
        return fournotes, chordtype
    except:
        return None



def removeRoot(chord):
    if len(chord)==0:
        raise Exception("empty chord")
    elif len(chord)==1:
        root=chord[0]
        chord=""
    else:
        if chord[1]=="b" or chord[1]=="#":
            root = chord[:2]
            chord = chord[2:]
        else:
            root = chord[0]
            chord = chord[1:]
        if "/" in chord:
            chord = chord[:chord.index("/")]
    return chord, root

if __name__ == "__main__":
    print(chordString_2_vector("C"))