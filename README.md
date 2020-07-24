# Key Modulation Dataset

A dataset of key modulations that have been annotated in different music theory books.

## Licensing

All the code in this repository is under the MIT License, except for the humdrum scores. All the scores are under the [CC BY SA 4.0](https://creativecommons.org/licenses/by/4.0/) License. The scores consist of all the files under the following folders:
- `aldwell`
- `kostka-payne`
- `reger`
- `rimsky-korsakov`
- `tchaikovsky`

## Dataset

The annotations consist of the following:

- Kostka-Payne
  - [x] Example 18-2
  - [x] Example 18-3
  - [x] Example 18-4
  - [x] Example 18-6
  - [x] Example 18-7
  - [x] Example 19-1
  - [x] Example 19-2
  - [x] Example 19-3
  - [x] Example 19-4
  - [x] Example 19-5
  - [x] Example 19-6
  - [x] Example 19-10
  - [x] Example 19-11
  - [x] Example 19-12
- Aldwell, Schachter and Cadwallader
  - [x] Example 27-2-a
  - [x] Example 27-2-b
  - [x] Example 27-2-c
  - [x] Example 27-3
  - [x] Example 27-4-a
  - [x] Example 27-4-b
  - [x] Example 27-7
- Tchaikovsky
  - [x] Example 173
  - [x] Example 183
  - [x] Example 185
  - [x] Example 189
  - [x] Example 191
  - [x] Example 193
  - [x] Example 195
- Max Reger
  - [x] Examples 1-100
- Rimsky-Korsakov
  - [X] Example 3.5
  - [X] Example 3.7
  - [X] Example 3.8
  - [X] Example 3.10
  - [X] Example 3.14
  - [X] Example 3.15
  - [X] Examples 3.17


Humdrum Utilities

- `add_text_spine.py` - Adds an empty `**text` spine at the end of the file (last column). Very helpful for when a file is not annotated yet and it is going to be annotated.
- `restaff.py` - Replaces the `*staff` entries with a systematic numbering. Starting with `*staff4` for the bass and up to `*staff1` in the soprano. Assumes that there is a `**text` spine at the end and it has an empty `*staff` entry.
- `correct_spine_association.py` - This figures out the correct `*staffX` that the `**text` spine should be pointing to at every slice. This is necessary in order to embed every annotation to a note, which many times is impossible if we annotate a single column.  
- `get_keys.py` - This gets the key annotations of a given file.
