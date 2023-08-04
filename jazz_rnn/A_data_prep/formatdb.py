import sqlite3

con = sqlite3.connect("wjazzd.db")
cur = con.cursor() # cursor used object used to query 

num_songs = 456

num_beats = 132329

excludedSongs = [50, 66, 147, 184, 185, 187, 188, 214, 215, 227, 228, 246, 308, 322, 336, 337, 338, 339, 340, 403, 404, 405, 407, 411, 412, 431, 433, 434, 439]

for i in range(num_songs,num_songs+1):
    if i in excludedSongs:
        continue
    cur.execute('SELECT chord, beatid FROM beats WHERE melid=? AND bar>0', (i,))
    beats = cur.fetchall()
    for chord, beatid in beats:
        if chord!="" and chord!="NC":
            current_chord = chord
        else:
            cur.execute('UPDATE beats SET chord=? WHERE melid=? AND beatid=?', (current_chord,i,beatid,))

con.commit()