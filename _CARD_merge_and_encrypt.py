'''
Credit:
timelic: https://github.com/timelic/master-duel-chinese-translation-switch
'''

from typing import List
import json
import sys
import zlib
from _CARD_decrypt_and_split import FileCheck, Decrypt, CheckCryptoKey

#1. Check if CARD_* files exist:

filenames_to_check = ['CARD_Indx', 'CARD_Indx.bytes', 'CARD_Indx.txt', 'CARD_Desc', 'CARD_Desc.bytes', 'CARD_Desc.txt', 'CARD_Name', 'CARD_Name.bytes', 'CARD_Name.txt']
check_counter = -1
CARD_Indx_filename = ''
CARD_Desc_filename = ''
CARD_Name_filename = ''

for i in filenames_to_check:
	check_counter += 1		
	if FileCheck(i) == 1 and i.find('CARD_Indx') != -1 and CARD_Indx_filename == '':
		CARD_Indx_filename = i
	if FileCheck(i) == 1 and i.find('CARD_Desc') != -1 and CARD_Desc_filename == '':
		CARD_Desc_filename = i
	if FileCheck(i) == 1 and i.find('CARD_Name') != -1 and CARD_Name_filename == '':
		CARD_Name_filename = i
	if check_counter == len(filenames_to_check)-1 and CARD_Indx_filename == '':
		print('CARD_Indx file not found. The file name must be \"CARD_Indx\", \"CARD_Indx.bytes\" or \"CARD_Indx.txt\".\nPress <ENTER> to exit.')
		input()
		sys.exit()
	if check_counter == len(filenames_to_check)-1 and CARD_Desc_filename == '':
		print('CARD_Desc file not found. The file name must be \"CARD_Desc\", \"CARD_Desc.bytes\" or \"CARD_Desc.txt\".\nPress <ENTER> to exit.')
		input()
		sys.exit()
	if check_counter == len(filenames_to_check)-1 and CARD_Name_filename == '':
		print('CARD_Name file not found. The file name must be \"CARD_Name\", \"CARD_Name.bytes\" or \"CARD_Name.txt\".\nPress <ENTER> to exit.')
		input()
		sys.exit()

#2. Read JSON files

def ReadJSON(json_file_path: str) -> list or dict:
    with open(json_file_path, 'r', encoding='utf8') as f:
        dic: list = json.load(f)
    return dic
	
def GetStringLen(s: str):
    return len(s.encode('utf-8'))
    res = 0
    for c in s:
        res += getCharLen(c)
    return res
	
def Solve_P_desc(desc):
	
    res = ""
    res += monster_effect
    if p_effect != '':
        res += '\n'
        res += separator
        res += '\n'
        res += p_effect

    return res

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

def IntTo4Hex(num: int) -> List[int]:
    res = []
    for _ in range(4):
        res.append(num % 256)
        num //= 256
    return res


card_indx_merge = []
for item in card_indx:
    card_indx_merge.extend(IntTo4Hex(item))

print('Finished calculating index.')

# 5. Find crypto key

if FileCheck('!CryptoKey.txt') == 1:
	print('Trying to read crypto key from file...')
	with open('!CryptoKey.txt', 'rt') as f_CryptoKey:		
			m_iCryptoKey = int(f_CryptoKey.read(),16)			
	f_CryptoKey.close()	
	print('Read crypto key "' + hex(m_iCryptoKey) + '" from file, checking if it is correct...')
else:
	m_iCryptoKey = 0x0

if CheckCryptoKey(m_iCryptoKey) == 1:
	print('The crypto key "' + hex(m_iCryptoKey) + '" is correct.')
else:
	m_iCryptoKey = FindCryptoKey()

# 6. Direct encryption

print('Encrypting files...')

file_names = [CARD_Name_filename, CARD_Desc_filename, CARD_Indx_filename]

def Encrypt(output_name, b: bytes):

    data = bytearray(zlib.compress(b))

    for i in range(len(data)):
        v = i + m_iCryptoKey + 0x23D
        v *= m_iCryptoKey
        v ^= i % 7
        data[i] ^= v & 0xFF

    with open(output_name, "wb") as f:
        f.write((data))
    f.close()

Encrypt(CARD_Name_filename,
        bytes(merge_string["name"], encoding='utf-8'))
Encrypt(CARD_Desc_filename,
        bytes(merge_string["desc"], encoding='utf-8'))
Encrypt(CARD_Indx_filename, bytes(card_indx_merge))

print('Finished encrypting files.')
