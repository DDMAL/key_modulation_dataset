import music21
import harmalysis
import sys
import pprint
import pandas as pd

def get_dataframe_from_file(filename):
    score = music21.converter.parse(filename)
    labels = {}
    for n in score.flat.notesAndRests:
        if n.lyric:
            label = harmalysis.parse(n.lyric)
            try:
                chordlabel = harmalysis.parse(str(label.chord), syntax='chordlabel')
            except:
                chordlabel = 'Unknown chord'
                pass
            offset = eval(str(n.offset)) # Resolving triplets (fractions) into floats
            labels[offset] = {
                'annotation': n.lyric,
                'chord_label': chordlabel,
                'chord_inversion': label.chord.inversion,
                'local_key': str(label.main_key),
                'tonicized_key': str(label.secondary_key),
            }
    df = pd.DataFrame(labels).transpose()
    return df


if __name__ == '__main__':
    filename = sys.argv[1]
    df = get_dataframe_from_file(filename)
    print(df)