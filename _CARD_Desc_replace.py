# python3
import fileinput
import re
import sys

def FileCheck(fn):
    try:
      open(fn, 'r')
      return 1
    except IOError:
      # print 'Error: File does not appear to exist.'
      return 0

#Check which Replace Guide text file to use:
if FileCheck('Replace Guide.txt') == 1:
	RG_filename='Replace Guide.txt'
elif FileCheck('Replace_Guide.txt') == 1:
	RG_filename='Replace_Guide.txt'
else:
	print('Replace guide text file not found. The file name must be \"Replace Guide.txt\" or \"Replace_Guide.txt\".\nPress <ENTER> to exit.')
	input()
	sys.exit()

#Check if file "CARD_Desc.dec.json" exists:
if FileCheck('CARD_Desc.dec.json') == 0:
	print('The required file "CARD_Desc.dec.json" was not found.\nPress <ENTER> to exit.')
	input()
	sys.exit()

#Create list for string replacement instructions:
RG_list=[]

#Read Replace Guide text file into the list:
with open(RG_filename, 'rt', encoding="utf8") as f_RG:
	line_counter = 0	
	for line in f_RG:
		line_counter += 1
		line = line.strip('\n') #remove line break
		#if not line == '' and not line == ' ': #skip empty lines (replaced by line below)
		if line_counter % 3 != 0: # check if line no. is not dividable by 3, because these are the blank lines
			RG_list.append(line) #append line to list
	f_RG.close()

#Read CARD_Desc JSON file into string variable:
with open('CARD_Desc.dec.json', 'rt', encoding="utf8") as f_CARD_Desc:
	CARD_Desc_content = f_CARD_Desc.read()
f_CARD_Desc.close()

#Apply string replacement instructions:
for i in range(0,len(RG_list)-1,2):
	if not any([x in RG_list[i] for x in ['*','^']]): #check if replacement instruction contains RegEx
		CARD_Desc_content_new = CARD_Desc_content_new.replace(RG_list[i], RG_list[i+1])	#Simple string replacement
	else:
		CARD_Desc_content_new = re.sub(RG_list[0], RG_list[1], CARD_Desc_content, count=0, flags=0)	#RegEx replacement

#Write changes to CARD_Desc JSON file:
with open('CARD_Desc.dec.json', 'wt', encoding="utf8") as f_CARD_Desc:
	f_CARD_Desc.write(CARD_Desc_content_new)
	f_CARD_Desc.close()

'''
print("Press <ENTER> to continue")
input()
'''
