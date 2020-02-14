import music21
import harmalysis

import sys
import pprint

if __name__ == '__main__':
    filename = sys.argv[1]
    score = music21.converter.parse(filename)
    labels = []
    for n in score.flat.notes:
        if n.lyric:
            label = harmalysis.parse(n.lyric)
            try:
                chordlabel = harmalysis.parse(str(label.chord), syntax='chordlabel')
            except:
                chordlabel = 'Unknown chord'
                pass
            labels.append((
                n.offset, 
                n.lyric, 
                chordlabel, 
                str(label.main_key), 
                str(label.secondary_key),))
    pprint.pprint(labels)