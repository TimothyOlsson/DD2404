from __future__ import division
"""In python 2.7, using ex 25/100 will yield 0, but not in 3.6. This fixes it"""
import sys
import os
import time
#import numpy #Can be used  to improve the matrix creation
import math
import subprocess
import tempfile


"""
Example of user mistakes:
Not using fasta file
Files not existing, not in files folder

"""


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


file_list = sys.argv[1:] #First in list is the name of the script
os.chdir('files')

##Error handling
if len(file_list) > 1:
    print('Please input just one file with aligned AA')
    quit()
for file_name in file_list:
    if os.path.splitext(file_name)[1] not in ['.fa','.FA','.fasta','.FASTA']:
        print('Wrong file type used. Only use fasta files!')
        quit()
    elif not os.path.isfile(file_name):
        print('File not found: %s' % file_name)
        quit()


f = tempfile.NamedTemporaryFile(delete=False, mode='w+') #Opens in read and write mode
f.write((str('Test').replace(',','\t').replace("'",'').strip('[]') + '\n'))

f.seek(0) #Go to start of file
print(f.read())
print(f.name)
f.close()
os.rename(f.name,'infile')
print(f.name)
