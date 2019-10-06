
import os
import sys

'''
Hinrik Hafsteinsson 2019
contact: hih43@hi.is

Script for extracting .wav files from video files using ffmpeg unix command.

  - Variable 'vid_folder' indicates input directory and must be edited as needed.
  - Variable 'extension' indicates input video format extension and must be edited
    as needed.

Part of the research project:
'Patrilineal Descent: Transcribing Spoken Language of Three Generations'
funded by The University of Iceland Research Fund.
'''

vid_folder = 'Vika04'
extension = '.mp4'
src_vid_folder = os.path.join('myndbond', vid_folder)

out_folder = os.path.join('converted', vid_folder)

cwd = os.getcwd()

if not os.path.isdir(out_folder):
    os.mkdir(out_folder)

for filename in os.listdir(os.path.join(cwd, src_vid_folder)):
    if not filename.endswith(extension): continue
    filename = filename.strip(extension)
    # spec_out_folder = os.path.join(out_folder, filename)
    out_path = os.path.join(cwd, out_folder)
    # if not os.path.isdir(out_path):
    # os.mkdir(spec_out_path)
    inFilePath = os.path.join(src_vid_folder, filename)
    outFilePath = os.path.join(out_path, filename)
    # os.system('ffmpeg -i {0}.MOD {1}.mov'.format(inFilePath, outFilePath))
    os.system('ffmpeg -i {0}{2} -f wav -ab 192000 -vn {1}.wav'.format(inFilePath, outFilePath, extension))
