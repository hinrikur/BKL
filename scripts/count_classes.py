import sys
from collections import defaultdict

'''
Hinrik Hafsteinsson 2019
contact: hih43@hi.is

Counts word classes in POS-tagged and lemmatized .tsv file.
Prints output to command line

Counts verb lemmas in POS-tagged and lemmatized .tsv file.
Outputs to command line

Part of the research project:
'Patrilineal Descent: Transcribing Spoken Language of Three Generations'
funded by The University of Iceland Research Fund.
'''

in_file = sys.argv[1]

wordClasses = defaultdict(int)

with open(in_file) as file:
    file = file.readlines()
    for line in file:
        line = line.strip('\n').split('\t')
        if len(line) == 1: continue
        wordClass = line[1][0]
        if wordClass == 'a':
            print(line)
        # wordClasses[wordClass] += 1

# for k,v in wordClasses.items():
#     print(k,v)
