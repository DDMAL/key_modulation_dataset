import music21
import harmalysis
import sys
import pprint
import pandas as pd

if __name__ == '__main__':
    filename = sys.argv[1]
    score = music21.converter.parse(filename)
    labels = {}
    for n in score.flat.notes:
        if n.lyric:
            label = harmalysis.parse(n.lyric)
            try:
                chordlabel = harmalysis.parse(str(label.chord), syntax='chordlabel')
            except:
                chordlabel = 'Unknown chord'
                pass
            labels[n.offset] = {
                'annotation': n.lyric,
                'chord_label': chordlabel,
                'chord_inversion': label.chord.inversion,
                'local_key': str(label.main_key),
                'tonicized_key': str(label.secondary_key),
            }
    df = pd.DataFrame(labels).transpose()
    print(df)