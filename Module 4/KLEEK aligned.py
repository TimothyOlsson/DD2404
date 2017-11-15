import Bio
import os
from Bio import SeqIO
import sys
import re
import subprocess
import time

#Stupid way, but ignore warnings when not multiple of 3
import warnings
warnings.filterwarnings("ignore")

os.chdir('files')
file_list = sys.argv[1:]
re_pattern = r'(KL([EI])\2{1}K)' #Need two capturing groups, due to the coloring
out_file = 'KLEEK_SEQS'

start_time = time.time()

f=open(out_file + '.txt','w') #Looks cleaner than "with" in this case
#Handles multiple files, input is fasta files with amino acid seq
for file_name in file_list:
    for seq in SeqIO.parse(file_name, "fasta"):
        if len(seq.seq) < 3:
            pass
        else:
            if bool(re.search(re_pattern, str(seq.seq))): #re.match didnt work...
                f.write('>' + seq.id)
                f.write(str(seq.seq))

f.close()

#Call automatically waits
process = subprocess.call(['muscle',
                           '-in',
                           out_file + '.txt',
                           "-out",
                           out_file + '_ALIGNED' + '.txt'])

stop_time = time.time()

print('Done, it took {} seconds'.format(stop_time - start_time))


