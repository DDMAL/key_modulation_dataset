import numpy

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