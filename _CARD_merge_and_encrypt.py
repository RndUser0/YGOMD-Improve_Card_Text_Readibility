'''
Credit:
timelic: https://github.com/timelic/master-duel-chinese-translation-switch
'''

from typing import List
import json
import sys
import zlib
from _defs import *

#1. Check if CARD_* files exist:

CARD_filenames = Check_CARD_files()
CARD_Indx_filename = CARD_filenames[0]
CARD_Desc_filename = CARD_filenames[1]
CARD_Name_filename = CARD_filenames[2]

#2. Read JSON files

print('Reading files...')

CARD_Name_json: list = ReadJSON(CARD_Name_filename + ".dec.json")
CARD_Desc_json: list = ReadJSON(CARD_Desc_filename + ".dec.json")

print('Finished reading files...')

#3. Merge JSON files

name_merge_string = "\u0000" * 8  # There are eight blanks at the beginning
desc_merge_string = "\u0000" * 8

merge_string = {"name": "\u0000" * 8, "desc": "\u0000" * 8}

name_indx = [0]
desc_indx = [0]

print('Merging files...')

for i in range(len(CARD_Name_json)):  # Here because of a strange bug in English desc is one less than name
    name = CARD_Name_json[i]
    desc = CARD_Desc_json[i]

    def Helper(sentence: str, indx: List[int], name_or_desc: str,
               merge_string: dict):
        #    Cancel here first, but it shouldn't be a problem here.
        # Convert Chinese pendulum monster effects to Japanese format
        # if sentence.startswith('←'):
        #     sentence = Solve_P_desc(sentence)
        length = GetStringLen(sentence)
        if i == 0:
            length += 8
        space_len = 4 - length % 4  # It means getting the remainder
        indx.append(indx[-1] + length + space_len)  # Record indx
        if name_or_desc == "name":
            merge_string["name"] += sentence + '\u0000' * space_len
        else:
            merge_string["desc"] += sentence + '\u0000' * space_len

    Helper(name, name_indx, "name", merge_string)
    Helper(desc, desc_indx, "desc", merge_string)

print('Finished merging files.\nCalculating index...')

#4. Calculate CARD index

# Compression
# Can't compress. Compression is a problem.

name_indx = [4, 8] + name_indx[1:]
desc_indx = [4, 8] + desc_indx[1:]

# print(name_indx)
# print(desc_indx)

card_indx = []
for i in range(len(name_indx)):
    card_indx.append(name_indx[i])
    card_indx.append(desc_indx[i])

#print(card_indx)

card_indx_merge = []
for item in card_indx:
    card_indx_merge.extend(IntTo4Hex(item))

print('Finished calculating index.')

# 5. Get crypto key

m_iCryptoKey = GetCryptoKey(CARD_Indx_filename)

# 6. Direct encryption

print('Encrypting files...')

Encrypt(CARD_Name_filename, bytes(merge_string["name"], encoding='utf-8'), m_iCryptoKey)
Encrypt(CARD_Desc_filename, bytes(merge_string["desc"], encoding='utf-8'), m_iCryptoKey)
Encrypt(CARD_Indx_filename, bytes(card_indx_merge), m_iCryptoKey)

print('Finished encrypting files.')
