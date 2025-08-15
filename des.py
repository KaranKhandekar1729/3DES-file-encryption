# option 2: key of 16 bytes (2 keys of 8 bytes)
from Crypto.Cipher import DES3 # pip install pycryptodome
from hashlib import md5 # to ensure key of size 16 bytes
import sys

if len(sys.argv) != 4:
    print("Usage: python des.py <operation:1|2> <file_path> <key>")
    sys.exit(1)

# sys.argv[0] for python file
operation = sys.argv[1] # '1' for encrypt, '2' for decrypt
file_path = sys.argv[2]
key = sys.argv[3]

print("OPERATION:", operation)
print("FILE:", file_path)
print("KEY:", key)
sys.stdout.flush()

key_hash = md5(key.encode('ascii')).digest() # get the hash of the key => 16-byte key using ascii encoding
tdes_key = DES3.adjust_key_parity(key_hash) # get tdes key

# ---------------------------------------
# OPERATIONS (ENCRYPT/DECRYPT)
# ---------------------------------------

if operation == '1': # encrypt
    cipher = DES3.new(tdes_key, DES3.MODE_EAX, nonce=b'0') # DES3.MODE_EAX => mode of operation
    with open(file_path, 'rb') as input_file:
        file_bytes = input_file.read()
    new_file_bytes = cipher.encrypt(file_bytes) # encrypt
    with open(file_path, 'wb') as output_file:
        output_file.write(new_file_bytes) # write encrypted bytes in file
    
if operation == '2': # decrypt
    with open(file_path, 'rb') as f:
        file_bytes = f.read()
    cipher = DES3.new(tdes_key, DES3.MODE_EAX, nonce=b'0') # DES3.MODE_EAX => mode of operation
    new_file_bytes = cipher.decrypt(file_bytes)
    with open(file_path, 'wb') as output_file:
        output_file.write(new_file_bytes)