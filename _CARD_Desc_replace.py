# python3
import fileinput
import os
import re
import sys
from _defs import *

#1. Check which Replace Guide text file to use:
if FileCheck('Replace Guide.txt') == 1:
	RG_filename='Replace Guide.txt'
	print('Using file "Replace Guide.txt".')
elif FileCheck('Replace_Guide.txt') == 1:
	RG_filename='Replace_Guide.txt'
	print('Using file "Replace_Guide.txt".')
else:
	print('Replace guide text file not found. The file name must be \"Replace Guide.txt\" or \"Replace_Guide.txt\".\nPress <ENTER> to exit.')
	input()
	sys.exit()

#2. Check if decompressed CARD_Desc JSON file exists:
filenames_to_check = ['CARD_Desc.dec.json', 'CARD_Desc.bytes.dec.json', 'CARD_Desc.txt.dec.json']
check_counter = -1
CARD_Desc_filename = ''

for i in filenames_to_check:
	check_counter += 1
	if FileCheck(i) == 1 and i.find('CARD_Desc') != -1 and CARD_Desc_filename == '':
		CARD_Desc_filename = i
		print('Using file "' + CARD_Desc_filename + '".')
	if check_counter == len(filenames_to_check)-1 and CARD_Desc_filename == '':
		print('CARD_Desc file not found. The file name must be \"CARD_Desc.dec.json\", \"CARD_Desc.bytes.dec.json\" or \"CARD_Desc.txt.dec.json\".\nPress <ENTER> to exit.')
		input()
		sys.exit()

#3. Create list for string replacement instructions:
RG_list=[]

#4. Read Replace Guide text file into the list:
with open(RG_filename, 'rt', encoding="utf8") as f_RG:
	line_counter = 0
	for line in f_RG:
		line_counter += 1
		line = line.strip('\n') #remove line break
		#if not line == '' and not line == ' ': #skip empty lines (replaced by line below)
		if line_counter % 3 != 0: # check if line no. is not dividable by 3, because these are the blank lines
			RG_list.append(line) #append line to list
	f_RG.close()

'''
for i in range(6):
	print(RG_list[i])
input()
'''

#5. Read CARD_Desc JSON file into string variable:
with open(CARD_Desc_filename, 'rt', encoding="utf8") as f_CARD_Desc:
	CARD_Desc_content = f_CARD_Desc.read()
f_CARD_Desc.close()

#6. Apply string replacement instructions:
for i in range(0,len(RG_list)-1,2):
	if not any([x in RG_list[i] for x in [r'\\n']]): #check if replacement instruction contains RegEx
		CARD_Desc_content = CARD_Desc_content.replace(RG_list[i], RG_list[i+1]) #Simple string replacement
	else:
		CARD_Desc_content = re.sub(RG_list[i], RG_list[i+1], CARD_Desc_content, count=0, flags=0) #RegEx replacement

#7. Write changes to CARD_Desc JSON file:
with open(CARD_Desc_filename, 'wt', encoding="utf8") as f_CARD_Desc:
	f_CARD_Desc.write(CARD_Desc_content)
	f_CARD_Desc.close()
	print('Replacements completed.')

'''
print("Press <ENTER> to continue")
input()
'''
