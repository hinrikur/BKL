# !/usr/bin/python
import os
import csv
import sys
import string
from collections import Counter
from collections import OrderedDict

'''
Hinrik Hafsteinsson 2019
contact: hih43@hi.is
Part of the research project:
'Patrilineal Descent: Transcribing Spoken Language of Three Generations'
funded by The University of Iceland Research Fund.


'''

input_file = sys.argv[1]
output_file = sys.argv[2]

lemma_file = open(input_file, 'r').readlines()

lemmas = []

for line in lemma_file:
    line = line.split()
    if line:
        if line[0] not in string.punctuation and line[1][0] == 's':
            # print(line[2])
            lemmas.append(line[2])

lemmas = Counter(lemmas)
lemmas = OrderedDict(sorted(lemmas.items(), key=lambda x: x[1], reverse=True))

with open(output_file, 'w') as tsvfile:
    writer = csv.writer(tsvfile, delimiter='\t')
    for k,v in lemmas.items():
        writer.writerow((k, v))
