'''
Credits:
akintos: https://gist.github.com/akintos/04e2494c62184d2d4384078b0511673b
timelic from NexusMods: https://forums.nexusmods.com/index.php?/user/145588218-timelic
'''

from typing import List
import json
import os
import zlib

def FileCheck(filename):
    try:
      open(filename, 'r')
      return 1
    except IOError:
      # print 'Error: File does not appear to exist.'
      return 0

def Decrypt(filename):
    with open(f'{filename}', "rb") as f:
        data = bytearray(f.read())

    for i in range(len(data)):
        v = i + m_iCryptoKey + 0x23D
        v *= m_iCryptoKey
        v ^= i % 7
        data[i] ^= v & 0xFF

    with open(f'{filename}' + ".dec", "wb") as f:
        f.write(zlib.decompress(data))

def CheckCryptoKey():	
	try:
		Decrypt('CARD_Indx')
		return 1
	except zlib.error:	
		return 0

# 1. Find crypto key

if FileCheck('!CryptoKey.txt') == 1:
	print('Trying to read crypto key from file...')
	with open('!CryptoKey.txt', 'rt') as f_CryptoKey:		
			m_iCryptoKey = int(f_CryptoKey.read(),16)			
	f_CryptoKey.close()	
	print('Read crypto key "' + hex(m_iCryptoKey) + '" from file, checking if it is correct...')
else:
	m_iCryptoKey = 0x0

if CheckCryptoKey() == 1:
	print('The crypto key "' + hex(m_iCryptoKey) + '" is correct.')
else:
	print('No correct crypto key found. Searching for crypto key...')
	m_iCryptoKey = 0x0	
	while True:
		try:
			Decrypt('CARD_Indx')
			if os.stat('CARD_Indx.dec').st_size > 0:						
				with open('!CryptoKey.txt', 'w') as f_CryptoKey:
					f_CryptoKey.write(hex(m_iCryptoKey))
				f_CryptoKey.close()
				print('Found correct crypto key "' + hex(m_iCryptoKey) + '" and wrote it to file "!CryptoKey.txt".')
			break
		except zlib.error:
			#print('Wrong crypto key:', hex(m_iCryptoKey), ' (zlib error)')
			m_iCryptoKey = m_iCryptoKey + 1
		#except Exception:
			#print('Unexpected {err=}, {type(err)=}')
		#else:


# 2. Decrypt CARD_Desc, Card_Indx + CARD_Name

filenames = ['CARD_Desc', 'CARD_Indx', 'CARD_Name']

print('Decrypting files...')

for name in filenames:
	if FileCheck(name) == 1:
		Decrypt(name)
		print('Decrypted file "' + name + '".')	
	else:
		print("Could not decrypt file " + name + " because it does not appear to exist.")

# 3. Split CARD_Desc + CARD_Name

def WriteJSON(l: list, json_file_path: str):
    with open(json_file_path, 'w', encoding='utf8') as f:
        json.dump(l, f, ensure_ascii=False, indent=4)

filenames = ['CARD_Name', 'CARD_Desc']

# The start of Name and Desc is 0 and 4 respectively
def ProgressiveProcessing(filename, start):

    # Read binary index
    with open(f'CARD_Indx.dec', "rb") as f:
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

    def fourToOne(x: List[int]) -> int:
        res = 0
        for i in range(3, -1, -1):
            res *= 16 * 16
            res += x[i]
        return res

    indx = [fourToOne(i) for i in indx]
    indx = indx[1:]
    	
    # Convert Decrypted CARD files to JSON files    
    def solve(data: bytes, desc_indx: List[int]):
        res = []
        for i in range(len(desc_indx) - 1):
            s = data[desc_indx[i]:desc_indx[i + 1]]
            s = s.decode('UTF-8')
            while len(s) > 0 and s[-1] == '\u0000':
                s = s[:-1]
            res.append(s)
        return res

    # Read Desc file
    with open(f"{filename}.dec", 'rb') as f:
        data = f.read()

    desc = solve(data, indx)
	
    WriteJSON(desc, f"{filename}.dec.json")

print('Splitting files...')

if __name__ == '__main__':    
    ProgressiveProcessing(filenames[0], 0)    
    ProgressiveProcessing(filenames[1], 4)

print('Finished splitting files.')
