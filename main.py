#!/usr/bin/python
# -*- coding: utf-8 -*-

import lab_1

swaper = lab_1.language_swap()
spacer = lab_1.space_method()
symbol = lab_1.spec_symbol_method()

# swaper.get_secret_text('./lab_1/test_file_inserted_ultr', 'en')
#
# spacer.insert_text('./lab_1/test_file', 'megalul')
# spacer.read_secret_file('./lab_1/test_file_space_inserted_mega', 'en')

symbol.insert_text('./lab_1/test_file_2', 'observer')
symbol.get_secret_text('./lab_1/test_file_2_spec_inserted_obse', 'en')
