import os
import time
import soundfile as sf

'''
Hinrik Hafsteinsson 2019
contact: hih43@hi.is

Script for measuring total length of .wav files in a directory

Part of the research project:
'Patrilineal Descent: Transcribing Spoken Language of Three Generations'
funded by The University of Iceland Research Fund.
'''

total_length = 0

for root, dirs, files in os.walk('converted', topdown=False):
    for file in files:
        if not file.endswith('.wav'): continue
        filepath = os.path.join(root, file)
        f = sf.SoundFile(filepath)
        length = len(f) / f.samplerate
        print(file, 'seconds = {}'.format(length))
        total_length += length

print('total length = {0}'.format(total_length/3600))

total_length = time.strftime("%H hours\n%M minutes\n%S seconds", time.gmtime(total_length))

print(total_length)
