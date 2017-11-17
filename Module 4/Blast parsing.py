import Bio
import os
from Bio import SeqIO
from Bio import SearchIO
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
import sys
import re
import time

start_time = time.time()
os.chdir('files')
file_list = sys.argv[2:]
regex_search = sys.argv[1]

print('\nStart of run')
for file_name in file_list:
    print(file_name)
    found_hit = False   
    file = open(file_name)
    blast_records = NCBIXML.parse(file)
    for blast_record in blast_records:
        for alignment in blast_record.alignments:
            for hsp in alignment.hsps:
                if bool(re.search(regex_search.upper(), str(alignment.title))):

                    if not found_hit:
                        print('Query name\tHit name\tScore\tE-value')

                    found_hit = True                    
                    index_word= re.search(regex_search.upper(),
                                          alignment.title)
                    print(blast_record.query + '\t' +
                          alignment.title[index_word.start():index_word.start()+20] + '\t' +
                          str(hsp.score) + '\t' +
                          str(hsp.expect) + '\t')

                    
    file.close()


if not found_hit:
    print('No hits found')
    
stop_time = time.time()

print('\nIt took {} seconds'.format(stop_time-start_time))


#https://www.biostars.org/p/193393/
