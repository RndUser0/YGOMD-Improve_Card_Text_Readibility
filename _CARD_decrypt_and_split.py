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
from _defs import *

# 1. Check if CARD_* files exist:

CARD_filenames = Check_CARD_files()
CARD_Indx_filename = CARD_filenames[0]
CARD_Desc_filename = CARD_filenames[1]
CARD_Name_filename = CARD_filenames[2]

# 2. Get crypto key

m_iCryptoKey = GetCryptoKey(CARD_Indx_filename)

# 3. Decrypt CARD_Desc, Card_Indx + CARD_Name

print('Decrypting files...')

for filename in CARD_filenames:
	if FileCheck(filename) == 1:
		data = ReadData(filename)
		data = Decrypt(data, m_iCryptoKey)
		WriteDecData(filename, data)
		print('Decrypted file "' + filename + '".')	
	else:
		print("Could not decrypt file " + filename + " because it does not appear to exist.")

# 4. Split CARD_Name + CARD_Desc

print('Splitting files...')

if __name__ == '__main__':    
    ProgressiveProcessing(CARD_Indx_filename, CARD_Name_filename, 0)    
    ProgressiveProcessing(CARD_Indx_filename, CARD_Desc_filename, 4)

print('Finished splitting files.')
