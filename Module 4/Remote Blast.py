import Bio
import os
from Bio import SeqIO
from Bio.Blast import NCBIWWW
import sys
import re
import time

#Stupid way, but ignore warnings when not multiple of 3
import warnings
warnings.filterwarnings("ignore")

os.chdir('files')
file_list = sys.argv[1:]

start_time = time.time()

for file_name in file_list:
    for seq in SeqIO.parse(file_name, "fasta"):
        rh = NCBIWWW.qblast("blastp", "p", seq.seq)

        #Reading rh again will delete it, write as file
        with open('blasted_' + os.path.splitext(file_name)[0] + '.xml','w') as f:
            store_blast = rh.read()
            f.write(store_blast)
            rh.close()
        print(store_blast)

stop_time = time.time()

print('\nIt took {} seconds'.format(stop_time-start_time))
