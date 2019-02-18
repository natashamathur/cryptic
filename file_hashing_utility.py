import sys
import os.path
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('filename')

# check arguments entered in command line
try:
    args = parser.parse_args()
except:
    print("Please input a single file, and no other arguments.",
          file=sys.stderr)
    sys.exit()
    
# check if file exists
if not os.path.exists(args.filename):
    print("The file '{}' does not exist!".format(args.filename),
            file=sys.stderr)
    sys.exit()
    
# check if file is blank    
if os.path.getsize(args.filename) == 0:
    print("This file is blank.", file=sys.stderr)
    sys.exit()
    
#try to import cryptographic library
try:
    import hashlib
except:
    print("Cannot load the cryptographic library", file=sys.stderr)
    sys.exit()
    
# I wasn't sure what the most reasonable way to break down a file into
# parts and use hashlib would be. I used the approach suggested in this
# StackOverflow post: https://stackoverflow.com/questions/1131220/get-md5-hash
# -of-big-files-in-python

# hash in chunks
hl = hashlib.sha256()
with open(content,'rb') as c: 
    for chunk in iter(lambda: c.read(hl.block_size*128), b''): 
        hl.update(chunk)
        
hashed = hl.hexdigest()

print("{}  {}".format(hashed, content), file=sys.stdout)
