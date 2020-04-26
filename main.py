#!/usr/bin/python
# -*- coding: utf-8 -*-

import lab_1
import steganography

swaper = lab_1.language_swap()
spacer = lab_1.space_method()
symbol = lab_1.spec_symbol_method()

# swaper.insert_text('./lab_1/test_file', 'ultrakek', 'en')
# swaper.get_secret_text('./lab_1/test_file_inserted_ultr', 'en')
#
spacer.insert_text('./lab_1/test_file', 'Evgeny')
spacer.read_secret_file('./lab_1/test_file_space_inserted_Evge', 'en')
#
# symbol.insert_text('./lab_1/test_file_2', 'Evgeny')
# symbol.get_secret_text('./lab_1/test_file_2_spec_inserted_obse', 'en')

cor = steganography.core()
print(cor.str_to_bit('ы'))
print(ord('s'.decode('utf-8')))
print(ord('ы'.decode('utf-8')))
