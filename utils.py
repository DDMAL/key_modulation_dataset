import numpy
import pandas as pd
import json
import os
import music21
import harmalysis

key_encodings = {}
keys = [                
    ('C', 0), 
    ('D', 2), 
    ('E', 4),
    ('F', 5),
    ('G', 7),
    ('A', 9),
    ('B', 11),
    ('c', 12), 
    ('d', 14), 
    ('e', 16),
    ('f', 17),
    ('g', 19),
    ('a', 21),
    ('b', 23)  
]

alterations = [
    ('', 0),
    ('#', 1),
    ('x', 2),
    ('##', 2),
    ('b', -1),
    ('bb', -2),
    ('-', -1),
    ('--', -2)
]

for key, label in keys:
    for alt, value in alterations:
        key_encodings[key + alt] = (12 + label + value) % 12
        key_encodings[key + alt] += 12 if label >= 12 else 0


def keyname_to_simplifiedkey(keyname):
    # Assume name is valid
    tonic, mode = keyname.split()
    mode = mode.lower()
    if mode == 'major':
        case = tonic[0].upper()
    elif mode == 'minor':
        case = tonic[0].lower()
    else:
        case = 'X'
    simplified = "{}{}".format(case, tonic[1:])        
    return simplified

def simplifiedkey_to_encodedlabel(simplified):        
    if simplified in key_encodings:
        return key_encodings[simplified]
    else:
        return -1

def score_key_prediction(gt, pred):        
    if pred == gt:
        return 1.0
    if gt < 12:
        dominant = (gt + 7) % 12
        subdominant = (gt + 5) % 12
        relative = ((gt + 9) % 12) + 12
        parallel = gt + 12
    else:
        dominant = ((gt + 7) % 12) + 12
        subdominant = ((gt + 5) % 12) + 12
        relative = (gt - 9) % 12
        parallel = gt - 12
    if pred == dominant or pred == subdominant:
        return 0.5    
    elif pred == relative:
        return 0.3
    elif pred == parallel:
        return 0.2
    else:
        return 0.0

def justkeydding_to_dfdictionary(filename):
    dfdict = {}
    with open(filename) as fd:
        lines = fd.readlines()
        for line in lines[1:]: # first line is the header
            line = line.strip()
            filename, jsondata = line.split('\t')
            df = pd.DataFrame(json.loads(jsondata))
            df.drop(columns=['global_key'], inplace=True)
            df['local_key_label'] = df.local_keys.apply(simplifiedkey_to_encodedlabel)
            dfdict[filename] = df
    return dfdict

def load_dataset(allfiles_folder):
    dfdict = {}
    dfdict_perfectmodulation = {}
    dfdict_perfecttonicization = {}
    for f in os.listdir(allfiles_folder):
        print(f)
        filename = os.path.join(allfiles_folder, f)
        score = music21.converter.parse(filename)
        labels = {}
        for n in score.flat.notes:
            if n.lyric:
                label = harmalysis.parse(n.lyric)                
                offset = eval(str(n.offset)) # Resolving triplets (fractions) into floats                
                local_key = str(label.main_key)
                if label.secondary_key:
                    tonicized_key = str(label.secondary_key)
                else:
                    tonicized_key = local_key
                local_key_simple = keyname_to_simplifiedkey(local_key)
                tonicized_key_simple = keyname_to_simplifiedkey(tonicized_key)
                local_key_label = simplifiedkey_to_encodedlabel(local_key_simple)
                tonicized_key_label = simplifiedkey_to_encodedlabel(tonicized_key_simple)
                labels[offset] = {
                    'local_key': local_key_simple,
                    'tonicized_key': tonicized_key_simple,
                    'local_key_label': local_key_label,
                    'tonicized_key_label': tonicized_key_label
                }
        df = pd.DataFrame(labels).transpose()        
        dfdict[f] = df
        # Getting the "perfect modulation" model
        dfmodulation = df.drop(columns=['local_key', 'tonicized_key', 'tonicized_key_label'])
        dfmodulation.rename(columns={'local_key_label': 'local_key_label'}, inplace=True)
        dfdict_perfectmodulation[f] = dfmodulation        
        # Getting the "perfect tonicization" model
        dftonicization = df.drop(columns=['local_key', 'tonicized_key', 'local_key_label'])
        dftonicization.rename(columns={'tonicized_key_label': 'local_key_label'}, inplace=True)
        dfdict_perfecttonicization[f] = dftonicization
    return dfdict, dfdict_perfectmodulation, dfdict_perfecttonicization

if __name__ == '__main__':
    gt = "C MAJOR"
    pred = "c minor"
    print(f"Ground truth: {gt}")
    print(f"Prediction: {pred}")
    
    gt_simple = keyname_to_simplifiedkey(gt)
    pred_simple = keyname_to_simplifiedkey(pred)
    print(f"Ground truth simple: {gt_simple}")
    print(f"Prediction simple: {pred_simple}")

    gt_label = simplifiedkey_to_encodedlabel(gt_simple)
    pred_label = simplifiedkey_to_encodedlabel(pred_simple)
    print(f"Ground truth label: {gt_label}")
    print(f"Prediction label: {pred_label}")

    score = score_key_prediction(gt_label, pred_label)
    print(f"Score is {score}")