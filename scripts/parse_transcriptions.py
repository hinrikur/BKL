# !/usr/bin/python
import os
import re
import csv
import pympi
from datetime import date as d
from tokenizer import tokenize, TOK

'''
Hinrik Hafsteinsson 2019
contact: hih43@hi.is
Part of the research project:

Module for processing Elan transcription data and writing to output file

Part of the research project:
'Patrilineal Descent: Transcribing Spoken Language of Three Generations'
funded by The University of Iceland Research Fund.
'''

class ElanTranscription():
    '''
    Class for processing a directory of Elan transcription data.

    Finds files in the input directory, extracts annotation data and writes to
    output .tsv files. Uses the pympi.Elan.Eaf() method to parse data out of
    .eaf transcription files.

    Class takes no object argument, directory paths are defined in __init__
    method.
    '''
    def __init__(self):
        self._iteration_number = 1
        self.ADULT_TIERS = ['Sif', 'Gunnar', 'Hamundur', 'Hámundur', 'Rannveig', 'Hrafnhildur', 'Sigmundur', 'Þorgeir']
        self.CHILD_TIERS = ['Kalli', 'Gunnar_ungur', 'Systir', 'Tvíburi']
        self.output_dir = os.path.join('output', 'elan-out_0')
        self.input_dir = 'uppskriftir'
        self.all_transcriptions = []

    def _get_iteration_number(self):
        '''
        Checks number of current output iteration
        '''
        dir = self.output_dir + str(self._iteration_number)
        if os.path.isdir(dir):
            self._iteration_number += 1
            return self._get_iteration_number()
        else:
            self.output_dir = dir
            return self

    def _iteration_info(self):
        '''
        Generates metadata on output iteration
        '''
        today = d.today()
        date = today.strftime("%d/%m/%Y")
        info = (
            'Elan transcription output',
            'Date: {0}'.format(str(date)),
            'Part of the research project ‘Patrilineal Descent: Transcribing Spoken Language of Three Generations’',
            'Authors: Einar Freyr Sigurðsson, Hinrik Hafsteinsson',
            'Output iteration number: {0}'.format(str(self._iteration_number)),
            'Nr. of output lines: {0}'.format(len(self.all_transcriptions)),
            'Adult speakers: {0}'.format(', '.join(self.ADULT_TIERS)),
            'Child speakers: {0}'.format(', '.join(self.CHILD_TIERS))
            )
        return info

    def _annotation_data(self, annotation, tier, file):
        '''
        Extracts relevant annotation data from
        input: pympi.Elan.Eaf.get_annotation_data_for_tier() object
        ouput: tuple of relevant annotation data (line in output file)
        '''
        start_time = annotation[0]
        end_time = annotation[1]
        utterance = annotation[2]
        words = utterance.split()
        length = end_time - start_time
        line = (tier, utterance, start_time, end_time, length, file)
        return line

    def _create_out_dir(self):
        '''
        Creates ouput directory if, with correct iteration number
        '''
        self._get_iteration_number()
        if os.path.isdir(self.output_dir):
            self._iteration_number += 1
            return self._create_out_dir(self._iteration_number)
        else:
            os.mkdir(self.output_dir)
            info_name = 'elan-out.0{0}.info'.format(self._iteration_number)
            info_output = os.path.join(self.output_dir, info_name)
            with open(info_output, 'w') as file:
                for item in self._iteration_info():
                    # print(item)
                    file.write(item)
                    file.write('\n')

    def write_to_tsv(self):
        '''
        Writes all annotations in all transcriptions to output .tsv file
        '''
        self._create_out_dir()
        tsv_name = 'BKL_utts.0{0}.tsv'.format(self._iteration_number)
        tsv_output = os.path.join(self.output_dir, tsv_name)
        with open(tsv_output, 'w') as tsvfile:
            writer = csv.writer(tsvfile, delimiter='\t')
            for line in self.all_transcriptions:
                writer.writerow(line)

    def write_totag_files(self):
        '''
        Writes all annotation tokens to files in preperation of POS-tagging
        One speaker per file (based on self.CHILD_TIERS and self.ADULT_TIERS)
        '''
        totag_folder = os.path.join(os.path.join(self.output_dir, 'totag'))
        os.mkdir(totag_folder)
        all_speakers = self.CHILD_TIERS + self.ADULT_TIERS
        for line in self.all_transcriptions:
            speaker = line[0]
            totag_file = speaker + '_test.in'
            totag_path = os.path.join(totag_folder, totag_file)
            with open(totag_path, 'a') as file:
                annotation = line[1]
                # print(list(filter(None.__ne__, [word.txt for word in tokenize(annotation)])))
                annotation = ' '.join(list(filter(None.__ne__, [word.txt for word in tokenize(annotation)])))
                file.write(annotation)
                # for word in tokenize(line[1]):
                #     if word.txt == None: continue
                #     if TOK.descr[word.kind] == 'PUNCTUATION': continue
                #     # file.write(str(speakers[speaker]) + ' ' + word.txt + '\n')
                #     file.write(word.txt + '\n')
                file.write('\n')

    def parse_eaf(self):
        '''
        Iterates through directory and extracts annotation data from .eaf files.
        Saves annotation data in self.all_transcriptions variable
        '''
        if os.path.isdir(self.input_dir):
            for root, dirs, files in os.walk(self.input_dir, topdown=False):
                for file in files:
                    if not file.endswith('.eaf'): continue
                    # wav_name = file.replace('.eaf', '.wav') # not used
                    file_path = os.path.join(root, file)
                    eafob = pympi.Elan.Eaf(file_path)
                    for tier in self.ADULT_TIERS:
                        try:
                            tier_data = eafob.get_annotation_data_for_tier(tier)
                            for annotation in tier_data:
                                output_data = self._annotation_data(annotation,
                                                                    tier, file)
                                self.all_transcriptions.append(output_data)
                                # print(annotation_data(tie r, file))
                        except KeyError:
                            continue
                    for tier in self.CHILD_TIERS:
                        try:
                            tier_data = eafob.get_annotation_data_for_tier(tier)
                            for annotation in tier_data:
                                output_data = self._annotation_data(annotation,
                                                                    tier, file)
                                self.all_transcriptions.append(output_data)
                                # print(output_data)
                        except KeyError:
                            continue
        else:
            print('Cannot find designated input directory: "{0}"'.format(self.input_dir))
            raise SystemExit

if __name__ == '__main__':
    t = ElanTranscription()
    t.parse_eaf()
    t.write_to_tsv()
    t.write_totag_files()
