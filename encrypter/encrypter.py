import hashlib, binascii
import nacl.secret
import nacl.utils
import argparse
import numpy as np
import os
import re
import sys

def generate_key():
    '''
    Generates a secret key to be used in the SecretBox
    containing that particular file. The secret key is based on a
    user inputted password that must contain numerical and non-numerical
    values.

    Inputs: None
    Output: Secured hash key
    '''

    pw = input("Please enter a password that contains letters and numbers: ")
    w = ''.join(re.findall('[^0-9]', pw))

    # password rule checks
    if len(w) == 0:
        print("Please retry this with a password that includes " +
              "both letters and numbers.")
        sys.exit()
        
    try:
        n = int(re.findall('\d+', pw)[0])
    except:
        print("Please retry this with a password that includes " +
              "both letters and numbers.")
        sys.exit()
    
    h = hashlib.sha256()
    h.update(str.encode(w))
    h = h.digest()
    
    np.random.seed(n)
    salt = np.random.bytes(16)
    dk = hashlib.pbkdf2_hmac('sha256', h, salt, 100000, dklen=16)
    out = binascii.hexlify(dk)
    
    return out
 
def encrypt_message(file):
    '''
    Encrypts a string using a Secret Box
    Input:
        m (str): string to be encoded
    Output:
        encrypted (bytes): encrypted message
    '''
    
    secret_key = generate_key()
    box = nacl.secret.SecretBox(secret_key)

    newfile = file.split(".")[0] + "_encrypted.bin"
    bin_f = open(newfile, "wb")

    with open(file,'rb') as c: 
        for chunk in iter(lambda: c.read(10000), b''):
            e = box.encrypt(chunk)
            bin_f.write(e)

    bin_f.close()
    print("The encrypted file is saved in: ", newfile)

def decrypt_message(file):
    '''
    Decrypts a string using a Secret Box. Asks for the secret key as input
    to prevent storing keys in command line history. 
    Input:
        em (str): string to be decoded
    Output:
        plaintext (str): decrypted message encoded using 'utf-8'
    '''
    secret_key = generate_key()
    box = nacl.secret.SecretBox(secret_key)

    newfile = file.split("_")[0] + "_decrypted.txt"
    text_file = open(newfile, "w")

    with open(file,'rb') as c: 
        for chunk in iter(lambda: c.read(10040), b''):
            d = box.decrypt(chunk)
            dw = d.decode("utf-8")
            text_file.write(dw)

    text_file.close()
    print("The decrypted file is saved in: ", newfile)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--file')
    parser.add_argument('instruction')
    args = parser.parse_args()

    # to simply see a key being generated
    if args.instruction == 'generatekey':
        print(generate_key())
    
    # to encrypt a new file
    # must provide the instruction "encrypt" and a file containing the
    # message to be encrypted
    if args.instruction == 'encrypt':

        # check that file is entered and exists
        if args.file == None or not os.path.exists(args.file):
            print("Please enter a valid file to be encrypted.",
                file=sys.stderr)
            sys.exit()

        # check if file is blank
        if os.path.getsize(args.file) == 0:
            print("This file is blank.", file=sys.stderr)
            sys.exit()

        # read file to a string and run the encryption function
        encrypted = encrypt_message(args.file)
        
    # to decrypt a file encrypted by this utilty
    # must provide the instruction "decrypt" and a file encrypted by this
    # program containing the message to be decrypted
    if args.instruction == 'decrypt':

        # check that file is entered and exists
        if args.file == None or not os.path.exists(args.file):
            print("Please enter a valid file to be decrypted.",
                file=sys.stderr)
            sys.exit()

        # check if file is blank
        if os.path.getsize(args.file) == 0:
            print("This file is blank.", file=sys.stderr)
            sys.exit()

        #  run the decryption function
        try:
            decrypted = decrypt_message(args.file)
        except:
            print("Decryption failed!")
            print("Please check that you entered the correct password" +
                  " and that the file you are trying to decrypt was encrypted " +
                  "by this utility")
