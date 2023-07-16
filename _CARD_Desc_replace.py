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

#Create list for RegEx patterns:
RG_list=[]

#Read Replace Guide text file into the list:
with open(RG_filename, 'rt', encoding="utf8") as f_RG:
	for line in f_RG:
		line = line.strip('\n') #remove line break
		if not line == '' and not line == ' ': #skip empty lines
			RG_list.append(line) #append line to list

#Apply RegEx patterns to CARD_Desc JSON file:
with open('CARD_Desc.dec.json', 'rt', encoding="utf8") as f_CARD_Desc:
	CARD_Desc_content = f_CARD_Desc.read()
	CARD_Desc_content_new = re.sub(RG_list[0], RG_list[1], CARD_Desc_content, count=0, flags=0)	#use 1st and 2nd list entries for RegEx replacement
	for i in range(2,len(RG_list)-1,2): #use list entries from 3 and above for simple string replacement
		CARD_Desc_content_new = CARD_Desc_content_new.replace(RG_list[i], RG_list[i+1])
	f_CARD_Desc.close()

#Write changes to CARD_Desc JSON file:
with open('CARD_Desc.dec.json', 'wt', encoding="utf8") as f_CARD_Desc:	
	f_CARD_Desc.write(CARD_Desc_content_new)
	f_CARD_Desc.close()