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
            labels.append((n.offset, n.lyric, str(label.main_key), str(label.secondary_key)))
    pprint.pprint(labels)