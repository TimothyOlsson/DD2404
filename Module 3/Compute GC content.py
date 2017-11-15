from __future__ import division
"""In python 2.7, using ex 25/100 will yield 0, but not in 3.6. This fixes it"""


"""
GC content is important, since genes and important regions usually
have high GC content. GC pairs are also more stable than AT,
due to more hydrogen bonds (3 vs 2)
"""


import sys
import os
import time

file_list = sys.argv[1:] #First in list is the name of the script

os.chdir('files')

start_time = time.time()

for file_name in file_list:
    GC = 0 #Amount of GC
    NTs = 0 #Amount of basepairs
    with open(file_name,'r') as f:
        for line in f: #Read lines
            line = line.upper().rstrip() #Makes everything upper case and removes \n
            if line.startswith('>'):
                pass
            else:
                NTs += len(line)
                GC += sum(1 for c in line if c in ['G', 'C'])

        print('%.4f' % (GC/NTs)) #Limit to 4 decimals


stop_time = time.time()

print('\nIt took {} seconds'.format(stop_time-start_time))
