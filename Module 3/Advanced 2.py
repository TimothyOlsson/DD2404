from __future__ import division
"""In python 2.7, using ex 25/100 will yield 0, but not in 3.6. This fixes it"""
import sys
import os
import time
#import numpy #Can be used  to improve the matrix creation
import math
import subprocess
import tempfile

#Function, reading fasta files
def read_fasta(self, file_contents):
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
    print("""Usage:\n
           bootstrap <filename> <number of boostraps>""")
    quit()
if os.path.splitext(arg_list[0])[1] not in ['.fa','.FA','.fasta','.FASTA']:
    print('Wrong file type used. Only use fasta files!')
    quit()
elif not os.path.isfile(arg_list[0]):
    print('File not found: %s' % arg_list[0])
    quit()

temp_file = tempfile.NamedTemporaryFile(mode='w+') #Opens in read and write mode
print(arg_list)
with open(arg_list[0], 'r') as f:
    for i in f:
        temp_file.write(i)

temp_file.seek(0) #Go to start of file
print(temp_file.read())
print(temp_file.name)
os.rename(temp_file.name,'infile')
print(temp_file.name)
temp_file.close()
