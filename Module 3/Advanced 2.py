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
def read_fasta(file_contents):
    """Input: list from fasta file, Output: 2 lists with names and sequences"""
    names = []
    sequences = []
    _seq = []
    for line in file_contents:
        line = str(line) #Bug with empty comments
        if line.startswith('>'):
            names.append(line[:9].rstrip('\n').strip('>').rstrip('\r'))
            if _seq != []:
                sequences.append(''.join(_seq).rstrip('\r'))
            _seq = []
        else:
            _seq.append(line.rstrip('\n').rstrip('\r').upper())
    sequences.append(''.join(_seq).upper()) #upper case
    return names, sequences

def check_errors(arg_list):
    ##Error handling
    if len(arg_list) == 1:
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
        int(arg_list[1]) #Check if the value is a number
    except:
        print('Bootstrap value is not a number')
        print("""Usage:\n
               bootstrap <filename> <number of boostraps>""")
        quit()
    try:
	debug = arg_list[2]
        if debug == 'True': # Input is string
	    return True
    except:
        return False


if __name__ == "__main__":
    arg_list = sys.argv[1:] # First in list is the name of the script
    os.chdir('files')
    debug_check = check_errors(arg_list) # Check for errors in arguments
    with open(arg_list[0], 'r') as f:
        names, sequences = read_fasta(f)
    tmp_file = tempfile.NamedTemporaryFile(mode='w+', delete=False) # Opens in read and write mode
    """Detected a problem: The name MUST be length 10, not less!! Fill with spaces"""
    tmp_file.write(str(len(names)) + '\t' + str(len(sequences[0])) + '\n')
    for i in range(len(names)):
        tmp_file.write(names[i] + ' '*(10 - len(names[i])) + sequences[i] + '\n')
    tmp_file.seek(0) #Go to start of file
    path_to_tmp = os.path.split(tmp_file.name)
    os.chdir(path_to_tmp[0])
    try:
	os.remove('outfile') #Clear from previous runs
    except:
	pass
    process = subprocess.Popen(['phylip','protdist'],
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)

    if debug_check:
	print(tmp_file.read())
	time.sleep(3)

    tmp_file.close()
    stderr, stdout = process.communicate(input=(path_to_tmp[1] + '\n'
						'I' + '\n'
						'Y' + '\n'))
    if debug_check:
	print(stderr)
	time.sleep(3)
    

    try:
	os.remove(path_to_tmp[1]) #Clear from previous runs
    except:
	pass
    os.rename('outfile', 'outfile_tmp')
    process = subprocess.Popen(['phylip','neighbor'],
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stderr, stdout = process.communicate(input=('outfile_tmp' + '\n'
						'Y' + '\n'))
    

    if debug_check:
	print(stderr)
	time.sleep(3)

    os.remove('outfile_tmp')
    sys.stderr.write('\x1b[2J\x1b[H') # Clear terminal
    with open('outfile','r') as f1, open('outtree','r') as f2:
	print(f2.read())
	
	start_print = False
	for line in f1:
	    if start_print:
		print(line)
	    if 'Negative' in line:
		start_print = True
	    elif 'remember' in line:
		start_print = False

    os.remove('outfile')
    os.remove('outtree')
	




