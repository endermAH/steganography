# -*- coding: utf-8 -*-

import argparse
import steganography
import shutil
import datetime
import time

class language_swap:
    steg_core = 'empty class'
    en_symbol = 'o'
    ru_symbol = 'о'.decode('utf-8')
    service_symbol_count = 1
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


    def insert_text(self, file_path, insert_text, lang):

        # Initialize inserting

        self.steg_core.log('SUCCESS', 'Inserting \'' + str(insert_text) + '\' into ' + str(file_path))
        inserted_file_name = file_path + '_swap_inserted_' + insert_text[0:4]

        # Get contents to insert

        inserting_file = open(file_path, 'r')
        inserting_contents = inserting_file.read().decode('utf-8')
        inserting_file.close()

        # Detect file lenguage

        detected = self.__detect_lenguage(inserting_contents)

        if ( not detected or not self.inserting_symbol ):
            self.steg_core.log('ERROR', 'Inserting stopped')
            return 0

        self.steg_core.log('TEST', 'detected symbol: ' + str(ord(self.inserting_symbol[0])))

        # Check if inserting text is too long

        bit_string = self.steg_core.str_to_bit(insert_text)
        available_bit_count = 0
        for contents_symbol in inserting_contents:
            if ( (contents_symbol != self.inserting_symbol[0]) and ((contents_symbol == self.en_symbol) or (contents_symbol == self.ru_symbol)) ):
                available_bit_count += 1

        self.steg_core.log('TEST', 'available_bit_count: ' + str(available_bit_count))

        if ( available_bit_count < len(bit_string) + self.service_symbol_count ):
            self.steg_core.log('ERROR', 'Iserting text is too long! It contains ' + str(len(bit_string)) + ' bits, when text can contain only ' + str(available_bit_count) + ' bits.')
            return 0

        # Insert secret test to contents variable

        self.steg_core.log('TEST', 'bit_string: ' + bit_string)
        for i in range(0,len(bit_string)):
            counter = 0
            for j in range(0,len(inserting_contents)):
                if ((inserting_contents[j] == self.ru_symbol) or (inserting_contents[j] == self.en_symbol)):
                    if ( counter == i and bit_string[i] == '1'):
                        inserting_contents = inserting_contents[0:j] + self.inserting_symbol + inserting_contents[j+1:]
                    counter += 1;


        changed_file = open(inserted_file_name, 'w')
        changed_file.write(inserting_contents.encode('utf-8'))
        changed_file.close()

        self.steg_core.log('SUCCESS', 'Text successfully inserted!')

    def get_secret_text(self, file_path, lang):

        self.steg_core.log('SUCCESS', 'Getting secret text from ' + str(file_path))

        # Get contents from file with secret text

        file = open(file_path, 'r')
        contents = file.read().decode('utf-8')
        file.close()

        # Detect 1 letter

        bit_letter = ''

        for i in contents:
            if ( (i != self.en_symbol) and (i != self.ru_symbol) ):
                if ( ord(i) < 128 ):
                    bit_letter = self.en_symbol
                else:
                    bit_letter = self.ru_symbol

        # Getting secret bit string

        bit_string = ''

        for i in range(0,len(contents)):
            if (contents[i] == self.en_symbol or contents[i] == self.ru_symbol):
                if ( contents[i] == bit_letter ):
                    bit_string += '1'
                else:
                    bit_string += '0'

        # Get string

        secret_text = self.steg_core.bit_str_to_text(bit_string, lang)

        self.steg_core.log('SUCCESS', 'Secret text: ' + secret_text)

class space_method:
    steg_core = 'empty class'

    def __init__(self):
        self.steg_core = steganography.core()
        self.steg_core.log('SUCCESS', ' === Lab1 space method initialized === ')

    def insert_text(self, file_path, insert_text):

        # Initialize inserting

        self.steg_core.log('SUCCESS', 'Inserting \'' + str(insert_text) + '\' into ' + str(file_path))
        inserted_file_name = file_path + '_space_inserted_' + insert_text[0:4]

        # Check if inserting text is too long

        bit_string = self.steg_core.str_to_bit(insert_text)
        available_bit_count = sum(1 for line in open(file_path, 'r'))

        self.steg_core.log('TEST', 'available_bit_count: ' + str(available_bit_count))

        if ( available_bit_count < len(bit_string) ):
            self.steg_core.log('ERROR', 'Iserting text is too long! It contains ' + str(len(bit_string)) + ' bits, when text can contain only ' + str(available_bit_count) + ' bits.')
            return 0

        # Insert secret text

        new_file = open(inserted_file_name, 'w')

        i = 0
        for line in open(file_path, 'r'):
            if ( i < len(bit_string) and bit_string[i] == '1' ):
                new_file.write(line[:len(line)-1] + ' \n')
            else:
                new_file.write(line)
            i += 1

    def read_secret_file(self, file_path, lang):
        # Read secret file

        bit_string = ''

        for line in open(file_path, 'r'):
            if ( line[len(line)-2] == ' ' ):
                bit_string += '1'
            else:
                bit_string += '0'

        print(bit_string)

        secret_text = self.steg_core.bit_str_to_text(bit_string, lang)
        self.steg_core.log('SUCCESS', 'Secret text: ' + secret_text)

class spec_symbol_method:

    def __init__(self):
        self.steg_core = steganography.core()
        self.steg_core.log('SUCCESS', ' === Lab1 spec symbol method initialized === ')

    def insert_text(self, file_path, insert_text):

        # Initialize inserting

        self.steg_core.log('SUCCESS', 'Inserting \'' + str(insert_text) + '\' into ' + str(file_path))
        inserted_file_name = file_path + '_spec_inserted_' + insert_text[0:4]

        # Check if inserting text is too long

        file = open(file_path, 'r')
        file_contents = file.read()
        file.close()

        available_bit_count = 0

        bit_string = self.steg_core.str_to_bit(insert_text)
        for i in file_contents:
            if ( i == '-' ):
                available_bit_count += 1

        self.steg_core.log('TEST', 'available_bit_count: ' + str(available_bit_count))

        if ( available_bit_count < len(bit_string) ):
            self.steg_core.log('ERROR', 'Iserting text is too long! It contains ' + str(len(bit_string)) + ' bits, when text can contain only ' + str(available_bit_count) + ' bits.')
            return 0

        # Insert secret text

        new_file = open(inserted_file_name, 'w')

        file_contents = file_contents.decode('utf-8')

        i = 0
        for j in range(0,len(file_contents)):
            if ( file_contents[j] == '-' and file_contents[j+1] == '-' ):
                if ( bit_string[i] == '1' ):
                    file_contents = file_contents[0:j+1] + '–'.decode('utf-8') + file_contents[j+2:]
                i += 1
                if ( i >= len(bit_string) ): break

        changed_file = open(inserted_file_name, 'w')
        changed_file.write(file_contents.encode('utf-8'))
        changed_file.close()

    def get_secret_text(self, file_path, lang):

        self.steg_core.log('SUCCESS', 'Getting secret text from ' + str(file_path))

        file = open(file_path, 'r')
        contents = file.read().decode('utf-8')
        file.close()

        bit_string = ''

        for i in range(0,len(contents)):
            if (contents[i] == '-' and contents[i+1] == '-'):
                bit_string += '0'
            if (contents[i] == '-' and contents[i+1] == '–'.decode('utf-8')):
                bit_string += '1'

        secret_text = self.steg_core.bit_str_to_text(bit_string, lang)

        self.steg_core.log('SUCCESS', 'Secret text: ' + secret_text)
