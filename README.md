# cryptic

The file [`encrypter`](https://github.com/natashamathur/cryptic/blob/master/encrypter.py) contains a utility that can encrypt and decrypt a file and generate the cryptographic keys necessary to do so. It is designed to prevent unauthorized read/write access of the encrytped files either by an inside or outside attacker. 

## Getting Started

The code is written in python3, and utilizes the following packages:

* [`hashlib`](https://docs.python.org/2/library/hashlib.html)
* [`pynacl`](https://pynacl.readthedocs.io/en/stable/secret/)
* [`numpy`](http://www.numpy.org/)


The following built-in modules are also used: `sys`, `re`, `argparse`, `os`

All requisite packages can be installed as such:

```
$ pip install [package name]
```
       
This utility is intended to be run from the command line. The following formats
can be used for commands:

*Suppose the file name of the original file is: sample.txt*

     python3 project2.py generatekey
     python3 project2.py encrypt --file "sample.txt"
     python3 project2.py decrypt --file "sample_encrypted.bin"
     
## How It Works
     
The encrypted file is stored in a separate binary file, and the resulting
decryption is also saved in a separate text file. When you run the command line
command it will print out the name of the file created.

When a file is entered to be encrypted, the first step is to create a specific
key to be used. An attacker would not know the key; however they should not be
able to reconstruct the key solely from anything in the code.

The user supplies a password that must contain numerical and non-numerical 
characters. If the provided password does not fulfill the requirement the system
exits. The function then hashes the textual part of the password using
SHA-256. The hashed message is then further hashed through PBKDF2. The salt
for this part is extracted from the numeric part of the password provided.
If the attacker did not have the entire password, they would not be able to
reconstruct the key from the code. The user must remember the password they
entered, but will never see or know the key. 

This key is then used to make a secret box, which is an example of symmetric key
encryption. The box can only be opened and interpreted by someone who has the
right key. The next step is to go through the message in chunks and repeatedly
use the box to encode. Each chunk is 1000 characters. This uniformity
is necessary to enable decryption. Every time the box is called a new random
nonce is generated. The encoded text, the authentication information,
and the nonce size are all printed to the output file.

When the file it to be decrypted the user is once again prompted to enter
their password. A SecretKey is then regenerated. The SecretBox will build a box
using the SecretKey based on the password provided. However if the reconstructed
SecretKey does not create the same box as was used to encrypt the message,
the decryption will fail. The encrypted message is read in 1040 byte chunks
that contain a part of the message to be decrypted the nonce and other information
it was encrypted with. If any of this information is different the message
will not be decrypted and an error message will be printed. 
