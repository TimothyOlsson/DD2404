import Bio
import os
from Bio import SeqIO
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
import re
import time
import argparse
from colorama import init, Fore, Back, Style #Colors! :)
init(autoreset=True)

def remove_none_files(file_list):
    new_file_list = []
    for file_name in file_list:
        if os.path.isfile(file_name):
            new_file_list.append(file_name)
        else:
            print(Fore.RED + 'No file found called {}'.format(file_name))
    if new_file_list != []:
        return new_file_list
    else:
        print(Back.RED + 'No files listed exist! Terminating...')
        quit()

# CLI
parser = argparse.ArgumentParser(description='Reads Blast outputs and plots them to a histogram.')
parser.add_argument('-i', '--input', nargs = '*', dest='FILES', required=True,
                    help='Input files with extension. Files should be put in the "files" folder')
parser.add_argument('-o', '--output', action='store', dest='OUTFILE', required=False, default='Blast_histo.pdf',
                    help='Output file.')
parser.add_argument('-s', dest='SEARCH', required=False, default='',
                    help='Search hits')
args = parser.parse_args()




# ERROR HANDLING
os.chdir('files')
args.FILES = remove_none_files(args.FILES) # Remove everything that's not a real file
start_time = time.time()

# FINDING VALUES (https://www.biostars.org/p/193393/)
e_values = []
scores = []
print(Back.GREEN + Style.BRIGHT + '\nStart of run\n')
for file_name in args.FILES:
    found_hit = False
    file = open(file_name)
    blast_records = NCBIXML.parse(file)
    for blast_record in blast_records:
        for alignment in blast_record.alignments:
            for hsp in alignment.hsps:
                if bool(re.search(args.SEARCH, str(alignment.title))):
                    if not found_hit:
                        print('\nQuery name\tHit name\tScore\tE-value')
                    found_hit = True                    
                    index_word= re.search(args.SEARCH,
                                          alignment.title)
                    print(blast_record.query + '\t' +
                          alignment.title[index_word.start():index_word.start()+20] + '\t' +
                          str(hsp.score) + '\t' +
                          str(hsp.expect) + '\t')

                    e_values.append(hsp.expect)
                    scores.append(hsp.score)
                    
    file.close()

if not found_hit:
    print(Back.RED + 'No hits found. Terminating...')
    quit()

stop_time = time.time()
print('\nIt took {} seconds'.format(stop_time-start_time))

# PLOTTING HISTOGRAM
"""I have imports here, since they take some time to import"""
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import matplotlib.axes as axes
import matplotlib.ticker as mtick

fig = plt.figure()
subplot = fig.add_subplot(1,2,1)
x, y, patches = plt.hist(scores, 50, normed=0, facecolor='green', alpha=0.75)
plt.xlabel('Score')
plt.ylabel('Counts')
plt.title('Blast histogram: Scores')
plt.axis([min(scores),
          max(scores),
          0,
          max(x)+1])
plt.grid(True)

ax = fig.add_subplot(1,2,2)
x, y, patches = plt.hist(e_values, 50, normed=0, facecolor='green', alpha=0.75)
plt.xlabel('E-values')
plt.ylabel('Counts')
plt.title('Blast histogram: E-values')
plt.axis([min(e_values),
          max(e_values),
          0,
          max(x)+1])
plt.grid(True)
ax.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.2e'))


# SAVING HISTOGRAM
plt.savefig(args.OUTFILE, dpi=400)
print(Back.GREEN + Style.BRIGHT + '\nDONE, saved figure as {}'.format(args.OUTFILE))

# Shows the figure
plt.show()

