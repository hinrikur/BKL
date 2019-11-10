# !/usr/bin/python
import argparse
import os
import csv
import pympi
from datetime import date as d
from tokenizer import tokenize
import nefnir

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
    output .tsv file. Uses the pympi.Elan.Eaf() method to parse data out of
    .eaf transcription files.

    Class takes no object argument, directory paths are defined in __init__
    method.
    '''

    def __init__(self):
        self._iteration_number = 1
        self.ADULT_TIERS = ['Sif', 'Gunnar', 'Hamundur', 'Hámundur',
                            'Rannveig', 'Hrafnhildur', 'Sigmundur', 'Þorgeir']
        self.CHILD_TIERS = ['Kalli', 'Gunnar_ungur', 'Systir', 'Tvíburi']
        # self.output_path = os.path.join('..', 'output')
        # self.output_dir = os.path.join(self.output_path, 'elan-out_0')
        self.output_dir = None
        self.file_basename = None
        self.parsed_tiers = [set(), set()]
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
        for line in self.all_transcriptions:
            if line[0] in self.ADULT_TIERS:
                self.parsed_tiers[0].add(line[0])
            if line[0] in self.CHILD_TIERS:
                self.parsed_tiers[1].add(line[0])
        today = d.today()
        date = today.strftime("%d/%m/%Y")
        info = (
            'Elan transcription output',
            'Date: {0}'.format(str(date)),
            'Part of the research project ‘Patrilineal Descent: Transcribing Spoken Language of Three Generations’',
            'Authors: Einar Freyr Sigurðsson, Hinrik Hafsteinsson',
            # 'Output iteration number: {0}'.format(str(self._iteration_number)),
            'Nr. of output lines: {0}'.format(len(self.all_transcriptions)),
            'Adult speakers: {0}'.format(', '.join(self.parsed_tiers[0])),
            'Child speakers: {0}'.format(', '.join(self.parsed_tiers[1]))
            )
        return info

    def _annotation_data(self, annotation, tier):
        '''
        Extracts relevant annotation data from

        :param annotation: pympi.Elan.Eaf.get_annotation_data_for_tier() object
        :param tier: name of relevant Elan tier
        :return: tuple of relevant annotation data (line in output file)
        '''
        start_time = annotation[0]
        end_time = annotation[1]
        utterance = annotation[2]
        # words = utterance.split() # word list defined but not used
        length = end_time - start_time
        line = (tier, utterance, start_time, end_time, length, self.file_basename)
        return line

    def write_info_file(self):
        if "../output/elan-out_0" in self.output_dir:
            info_name = 'elan-out.0{0}.info'.format(self._iteration_number)
        else:
            info_name = self.file_basename + '.info'
        info_output = os.path.join(self.output_dir, info_name)
        with open(info_output, 'w') as file:
            for item in self._iteration_info():
                # print(item)
                file.write(item)
                file.write('\n')

    def create_out_dir(self):
        '''
        Creates ouput directory if, with correct iteration number
        '''
        # checks if default output value
        if self.output_dir == "../output/elan-out_0":
            self._get_iteration_number()
            if os.path.isdir(self.output_dir):
                self._iteration_number += 1
                return self.create_out_dir(self._iteration_number)
            else:
                os.mkdir(self.output_dir)

        else:
            if os.path.isdir(self.output_dir):
                print("Output directory already exists. Fix and run again.")
                raise SystemExit
            else:
                os.mkdir(self.output_dir)


    def write_to_tsv(self):
        '''
        Writes all annotations in all transcriptions to output .tsv file
        '''
        # self._create_out_dir()
        if "../output/elan-out_0" in self.output_dir:
            tsv_name = 'BKL_utts.0{0}.tsv'.format(self._iteration_number)
        elif self.file_basename == 'uppskriftir':
            tsv_name = 'elan-out_total.tsv'
        else:
            tsv_name = self.file_basename + ".tsv"
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
                file.write('\n')

    def parse_eaf(self, file, root=None):
        '''
        Iterates extracts annotation data from .eaf file.
        Saves annotation data in self.all_transcriptions variable

        :param file: name of .eaf file to read
        :param root: optional argument with root path of file to read
        '''
        # wav_name = file.replace('.eaf', '.wav') # not used
        if root:
            file_path = os.path.join(root, file)
        else:
            file_path = file
        eafob = pympi.Elan.Eaf(file_path)
        for tier in self.ADULT_TIERS:
            try:

                tier_data = eafob.get_annotation_data_for_tier(tier)
                for annotation in tier_data:
                    output_data = self._annotation_data(annotation, tier)
                    self.all_transcriptions.append(output_data)
                    # print(annotation_data(tie r, file))
            except KeyError:
                continue
        for tier in self.CHILD_TIERS:
            try:

                tier_data = eafob.get_annotation_data_for_tier(tier)
                for annotation in tier_data:
                    output_data = self._annotation_data(annotation, tier)
                    self.all_transcriptions.append(output_data)
                    # print(output_data)
            except KeyError:
                continue


def main():
    # input parameters read
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                     # formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='''
    ELAN transcription parser

    Hinrik Hafsteinsson 2019
    contact: hih43@hi.is
    Part of the research project:

    Module for processing Elan transcription data and writing to output file
    in .tsv format and preparing for PoS tagging.

    Part of the research project:
    'Patrilineal Descent: Transcribing Spoken Language of Three Generations'
    funded by The University of Iceland Research Fund.
    ''')

    parser.add_argument("-t", "--type",
                        help="designate input as file or directory (default: %(default)s)",
                        choices=['file', 'dir'],
                        default="dir")
    parser.add_argument("-T", "--totag",
                        help="prepare seperate files for PoS-tagging",
                        action="store_true")
    parser.add_argument("-n", "--nodir",
                        help="pass to not create specific directory for output files ",
                        action="store_true")
    parser.add_argument('-i', '--input',
                               nargs='+',
                               required=False,
                               default="../uppskriftir",
                               help="Path to the input to be read (file or directory, default: %(default)s)")
    parser.add_argument("-o", "--output",
                               help="name of output directory (default: %(default)s)",
                               default="../output/elan-out_0")
    args = parser.parse_args()

    # transcription object created and file basename set
    t = ElanTranscription()
    t.file_basename = os.path.splitext(os.path.basename(args.input[0]))[0]

    # checked wether nodir parameter met
    if not args.nodir:
        if args.type == 'file':
            t.output_dir = "../output/" + t.file_basename
            t.create_out_dir()
        elif args.type == 'dir':
            t.output_dir = args.output
            t.create_out_dir()
    else:
        t.output_dir = "../output"

    # checked wether input is directory
    if args.type == "dir":
        if args.input[0].endswith(".eaf"):
            print("'-T dir' flag implies directory and input path implies file")
            print("Please try again")
            raise SystemExit
        else:
            input_dir = args.input[0]
            for root, dirs, files in os.walk(input_dir, topdown=False):
                for file in files:
                    if not file.endswith('.eaf'): continue
                    t.parse_eaf(file, root=root)
                    # print(root, file)

    # checked wether input file exists
    elif args.type == "file":
        for file in args.input:
            t.parse_eaf(file)
            # print(file)

    # input not found
    else:
        print('Cannot find designated input location: "{0}"'.format(args.input[0]))
        raise SystemExit

    # .tsv output written
    t.write_to_tsv()

    # transcription metadata written to file
    if os.path.isdir(t.output_dir) and not t.output_dir == "../output":
        t.write_info_file()

    # .tsv files written, if totag parameter present
    if args.totag:
        t.write_totag_files()

    # t = ElanTranscription(args.)
    # t.parse_eaf()
    # t.write_to_tsv()
    # t.write_totag_files()


if __name__ == '__main__':
    main()
