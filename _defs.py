'''
Credits:
akintos: https://gist.github.com/akintos/04e2494c62184d2d4384078b0511673b
timelic: https://github.com/timelic/master-duel-chinese-translation-switch
'''

from typing import List
import json
#import os
import sys
import zlib

#[Decrypt and split]

def FileCheck(filename):
	try:
		open(filename, 'r')
		return 1
	except IOError:
	#print 'Error: File does not appear to exist.'
		return 0

def Decrypt(data, m_iCryptoKey):	
	try:
		for i in range(len(data)):
			v = i + m_iCryptoKey + 0x23D
			v *= m_iCryptoKey
			v ^= i % 7
			data[i] ^= v & 0xFF			
		return zlib.decompress(data)		
	except zlib.error:
		#print('zlib.error because of wrong crypo key:' + hex(m_iCryptoKey))		
		return bytearray()
	#except Exception:
	#else:

def ReadByteData(filename):
	with open(f'{filename}', "rb") as f:
		data = bytearray(f.read())	
	return data

def WriteDecData(filename, data):
	with open(f'{filename}' + ".dec", "wb") as f:
		f.write(data)

def CheckCryptoKey(filename, m_iCryptoKey):	
	data = ReadByteData(filename)	
	if Decrypt(data, m_iCryptoKey) == bytearray():
		return 0
	else:
		return 1
		
def FindCryptoKey(filename):
	print('No correct crypto key found. Searching for crypto key...')	
	m_iCryptoKey = -0x1	
	enc_data = ReadByteData(filename)	
	dec_data = bytearray()	
	while dec_data == bytearray():			
			m_iCryptoKey = m_iCryptoKey + 1			
			data = bytearray(enc_data)
			dec_data = Decrypt(data, m_iCryptoKey)
			#if os.stat('CARD_Indx.dec').st_size > 0:						
	with open('!CryptoKey.txt', 'w') as f_CryptoKey:
		f_CryptoKey.write(hex(m_iCryptoKey))
	f_CryptoKey.close()
	print('Found correct crypto key "' + hex(m_iCryptoKey) + '" and wrote it to file "!CryptoKey.txt".')	
	return m_iCryptoKey

def GetCryptoKey(filename):
	if FileCheck('!CryptoKey.txt') == 1:
		print('Trying to read crypto key from file...')
		with open('!CryptoKey.txt', 'rt') as f_CryptoKey:		
				m_iCryptoKey = int(f_CryptoKey.read(),16)			
		f_CryptoKey.close()	
		print('Read crypto key "' + hex(m_iCryptoKey) + '" from file, checking if it is correct...')
	else:
		m_iCryptoKey = 0x0

	if CheckCryptoKey(filename, m_iCryptoKey) == 1:
		print('The crypto key "' + hex(m_iCryptoKey) + '" is correct.')
	else:
		m_iCryptoKey = FindCryptoKey(filename)	
	return m_iCryptoKey

def Check_CARD_files():
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
	return [CARD_Indx_filename,CARD_Desc_filename,CARD_Name_filename]
	
def WriteJSON(l: list, json_file_path: str):
    with open(json_file_path, 'w', encoding='utf8') as f:
        json.dump(l, f, ensure_ascii=False, indent=4)

# The start of Name and Desc is 0 and 4 respectively
def ProgressiveProcessing(CARD_Indx_filename, filename, start):

    # Read binary index
    with open(CARD_Indx_filename + ".dec", "rb") as f:
        hex_str_list = ("{:02X}".format(int(c))
                        for c in f.read())  # Define variables to accept file contents
    dec_list = [int(s, 16) for s in hex_str_list]  # Convert hexadecimal to decimal

    # Get the index of Desc
    indx = []
    for i in range(start, len(dec_list), 8):
        tmp = []
        for j in range(4):
            tmp.append(dec_list[i + j])
        indx.append(tmp)

    def FourToOne(x: List[int]) -> int:
        res = 0
        for i in range(3, -1, -1):
            res *= 16 * 16
            res += x[i]
        return res

    indx = [FourToOne(i) for i in indx]
    indx = indx[1:]
    	
    # Convert Decrypted CARD files to JSON files    
    def Solve(data: bytes, desc_indx: List[int]):
        res = []
        for i in range(len(desc_indx) - 1):
            s = data[desc_indx[i]:desc_indx[i + 1]]
            s = s.decode('UTF-8')
            while len(s) > 0 and s[-1] == '\u0000':
                s = s[:-1]
            res.append(s)
        return res

    # Read Desc file
    with open(f"{filename}" + ".dec", 'rb') as f:
        data = f.read()

    desc = Solve(data, indx)
	
    WriteJSON(desc, f"{filename}" + ".dec.json")
	
#[Merge and encrypt]

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

def IntTo4Hex(num: int) -> List[int]:
    res = []
    for _ in range(4):
        res.append(num % 256)
        num //= 256
    return res

def Encrypt(output_name, b: bytes, m_iCryptoKey):
    data = bytearray(zlib.compress(b))

    for i in range(len(data)):
        v = i + m_iCryptoKey + 0x23D
        v *= m_iCryptoKey
        v ^= i % 7
        data[i] ^= v & 0xFF

    with open(output_name, "wb") as f:
        f.write((data))
    f.close()
