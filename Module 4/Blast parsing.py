import Bio
import os
from Bio import SeqIO
from Bio.Blast import NCBIWWW, NCBIXML
import sys
import re
import time

#Stupid way, but ignore warnings when not multiple of 3
import warnings
warnings.filterwarnings("ignore")

os.chdir('files')
file_list = sys.argv[1:]

start_time = time.time()

print('Start of run\n')
for file_name in file_list:
    with open(file_name,'r') as f:
        xml_read = NCBIXML.read(f)
        for alignment in xml_read.alignments:
            for hsp in alignment.hsps:
                print(alignment.title)
                print(alignment.length)



        
stop_time = time.time()

print('\nIt took {} seconds'.format(stop_time-start_time))
