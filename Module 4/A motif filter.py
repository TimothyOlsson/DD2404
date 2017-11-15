import Bio
import os
from Bio import SeqIO
import sys
import re
from colorama import init, Fore, Back, Style #Colors! :)
init()

#Stupid way, but ignore warnings when not multiple of 3
import warnings
warnings.filterwarnings("ignore")

os.chdir('files')
file_list = sys.argv[1:]

re_pattern = r'(KL([EI])\2{1}K)' #Need two capturing groups, due to the coloring

#Handles multiple files, input is fasta files with amino acid seq
for file_name in file_list:
    for seq in SeqIO.parse(file_name, "fasta"):
        if len(seq.seq) < 3:
            pass
        else:
            if bool(re.search(re_pattern, str(seq.seq))): #re.match didnt work...
                print('>' + seq.id)
                """I wanted to colorize the found patterns, which makes the file more complicated"""
                print(re.sub(re_pattern, Fore.RED + r'\1' + Style.RESET_ALL, str(seq.seq)))
