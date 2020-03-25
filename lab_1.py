# -*- coding: utf-8 -*-

import argparse
import steganography
import shutil
import datetime
import time

class language_swap:
    steg_core = 'empty class'
    en_symbol = 'o'
    ru_symbol = 'о'
    inserting_symbol = False

    def __init__(self):
        self.steg_core = steganography.core()
        self.steg_core.log('SUCCESS', ' === Lab1 language swap method initialized === ')

    def __detect_lenguage(self, contents):
        i = 0
        while( (contents[i] != self.en_symbol) and (contents[i] != self.ru_symbol) ):
            i += 1
        if ( contents[i] == self.en_symbol ):
            self.inserting_symbol = self.ru_symbol
            return 1

        elif ( contents[i] == self.ru_symbol ):
            self.inserting_symbol = self.en_symbol
            return 1
        else:
            self.steg_core.log('ERROR', 'Can not find ' + self.en_symbol + 'in the text.')
            return 0


    def insert_text(self, file_path, insert_text):

        # Initialize inserting and copy original file

        self.steg_core.log('SUCCESS', 'Inserting \'' + str(insert_text) + '\' into ' + str(file_path))
        inserted_file_name = file_path + '_inserted_' + insert_text[0:4] + '_' + str(datetime.datetime.fromtimestamp(time.time()))
        shutil.copyfile(file_path, inserted_file_name)

        # Get contents to insert

        inserting_file = open(inserted_file_name, 'r')
        inserting_contents = inserting_file.read()
        inserting_file.close()

        # Detect file lenguage

        detected = self.__detect_lenguage(inserting_contents)

        if ( not detected or not self.inserting_symbol ):
            self.steg_core.log('ERROR', 'Inserting stopped')
            return 0

        # Insert secret test to contents variable

        for i in insert_text :
            print(' '.join(format(ord(i), 'b')))
