import Bio
import os
from Bio import SeqIO
import sys

#Stupid way, but ignore warnings when not multiple of 3
import warnings
warnings.filterwarnings("ignore")


os.chdir('files')
file_list = sys.argv[1:]

#Handles multiple files
for file_name in file_list:
    for seq in SeqIO.parse(file_name, "fasta"):
        print('>' + seq.id)
        if len(seq.seq) < 3:
            print('')
        else:
            print(seq.seq.translate()) #Can add to_stop=True if you don't want stop
