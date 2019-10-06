
import os
import sys

'''
Hinrik Hafsteinsson 2019
contact: hih43@hi.is

Script for extracting .mov files from .MOD files in a directory, AND .wav files
from output .mov files using ffmpeg unix command.

  - Variable 'vid_folder' indicates input directory and must be edited as needed.

Part of the research project:
'Patrilineal Descent: Transcribing Spoken Language of Three Generations'
funded by The University of Iceland Research Fund.
'''

vid_folder = 'Vika02'
src_vid_folder = os.path.join('myndbond', vid_folder)

out_folder = os.path.join('converted', vid_folder)

cwd = os.getcwd()

for filename in os.listdir(os.path.join(cwd, src_vid_folder)):
    if not filename.endswith('.MOD'): continue
    filename = filename.strip('.MOD')
    spec_out_folder = os.path.join(out_folder, filename)
    spec_out_path = os.path.join(cwd, spec_out_folder)
    if not os.path.isdir(spec_out_path):
        os.mkdir(spec_out_path)
        inFilePath = os.path.join(src_vid_folder, filename)
        outFilePath = os.path.join(spec_out_path, filename)
        os.system('ffmpeg -i {0}.MOD {1}.mov'.format(inFilePath, outFilePath))
        os.system('ffmpeg -i {0}.mov -f wav -ab 192000 -vn {1}.wav'.format(outFilePath, outFilePath))
