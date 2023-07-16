'''
Credits:
- akintos: https://gist.github.com/akintos/04e2494c62184d2d4384078b0511673b
'''

import os
import zlib

m_iCryptoKey = 0x25F ## old crypto key

def Decrypt(file_name):
    with open(f'{file_name}', "rb") as f:
        data = bytearray(f.read())

    for i in range(len(data)):
        v = i + m_iCryptoKey + 0x23D
        v *= m_iCryptoKey
        v ^= i % 7
        data[i] ^= v & 0xFF

    with open(f'{file_name}' + ".dec", "wb") as f:
        f.write(zlib.decompress(data))

while True:

	try:

		Decrypt('CARD_Indx')
		if os.stat('CARD_Indx.dec').st_size > 0:
			with open('!CryptoKey.txt', 'w') as f:
				f.write(hex(m_iCryptoKey))
			print("Crypto key found and written to ""!CryptoKey.txt"" ")
			
		break

	except zlib.error:

		print("zlib error, CryptoKey =", hex(m_iCryptoKey))
		m_iCryptoKey = m_iCryptoKey + 1		

print("Press <ENTER> to continue")
input()
