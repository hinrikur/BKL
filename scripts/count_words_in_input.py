import sys
import string

'''
Hinrik Hafsteinsson 2019
contact: hih43@hi.is

Counts words in POS-tagged file, excluding punctuation.

Part of the research project:
'Patrilineal Descent: Transcribing Spoken Language of Three Generations'
funded by The University of Iceland Research Fund.
'''

with open(sys.argv[1], 'r') as file:
    count = 0
    for line in file.readlines():
        if line.strip() and line[0] not in string.punctuation:
            count += 1
    print(count)
