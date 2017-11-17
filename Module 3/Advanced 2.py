from __future__ import division
"""In python 2.7, using ex 25/100 will yield 0, but not in 3.6. This fixes it"""
import sys
import os
import time
#import numpy #Can be used  to improve the matrix creation
import math
import subprocess
import tempfile

# Function, reading fasta files
def read_fasta(self, file_contents):
    """Input: list from fasta file, Output: 2 lists with names and sequences"""
    names = []
    sequences = []
    _seq = []
    for line in file_contents:
        line = str(line) #Bug with empty comments
        if line.startswith('>'):
            names.append(line.rstrip('\n'))
            if _seq != []:
                sequences.append(''.join(_seq))
            _seq = []
        else:
            _seq.append(line.rstrip('\n').upper())
    sequences.append(''.join(_seq).upper()) #upper case
    return names, sequences

arg_list = sys.argv[1:] #First in list is the name of the script
os.chdir('files')

##Error handling
if len(arg_list) != 2:
    print('No bootstrap value added!')
    print("""Usage:\n
           bootstrap <filename> <number of boostraps>""")
    quit()
if os.path.splitext(arg_list[0])[1] not in ['.fa','.FA','.fasta','.FASTA']:
    print('Wrong file type used. Only use fasta files!')
    quit()
elif not os.path.isfile(arg_list[0]):
    print('File not found: %s' % arg_list[0])
    quit()

try:
    int(arg_list[1])
except:
    print('Bootstrap value is not a number')
    print("""Usage:\n
           bootstrap <filename> <number of boostraps>""")
    quit()

tmp_file = tempfile.NamedTemporaryFile(mode='w+') #Opens in read and write mode
print(arg_list)
with open(arg_list[0], 'r') as f:
    for i in f:
        tmp_file.write(i)

tmp_file.seek(0) #Go to start of file
path_to_tmp = os.path.split(tmp_file.name)

os.chdir(path_to_tmp[0])

process = subprocess.Popen(['phylip','neighbor'],
                           stdin=subprocess.PIPE,
                           stdout=subprocessPIPE,
                           stderr=subprocess.PIPE)

process.communicate(path_to_tmp[1])

#process = subprocess.call(['phylip','neighbor', [arg for sublist in lists for item in sublist]



