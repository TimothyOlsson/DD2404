from __future__ import division
"""In python 2.7, using ex 25/100 will yield 0, but not in 3.6. This fixes it"""

import sys
import os
import time
#import numpy #Can be used  to improve the matrix creation
import math


"""
Example of user mistakes:
Not using fasta file
Files not existing, not in files folder

"""

file_list = sys.argv[1:] #First in list is the name of the script
os.chdir('files')

for file_name in file_list:
    if os.path.splitext(file_name)[1] not in ['.fa','.FA','.fasta','.FASTA']:
        print('Wrong file type used. Only use fasta files!')
        quit()
    elif not os.path.isfile(file_name):
        print('File not found: %s' % file_name)
        quit()


data_dict = {} #Empty dict, used for storage

def dist_func(list1, list2):
    #I don't need to check if the lists are uneven lenght
    dist = math.sqrt(0.25*((list1[0]-list2[0])**2 +
                           (list1[1]-list2[1])**2 +
                           (list1[2]-list2[2])**2 +
                           (list1[3]-list2[3])**2))
    return round(dist,4)

start_time = time.time() #Calculate performance

for file_name in file_list:
    A = 0 #Amount of A
    C = 0 #Amount of C
    G = 0 #Amount of G
    T = 0 #Amount of T
    N = 0 #Amount of N (can be used to subtract from total NTs)
    NTs = 0 #Amount of basepairs
    with open(file_name,'r') as f:
        for line in f: #Read lines
            line = line.upper().rstrip() #Makes everything upper case and removes \n, easy to miss
            if line.startswith('>'):
                pass
            else:
                NTs += len(line)
                A += sum(1 for c in line if c == 'A')
                C += sum(1 for c in line if c == 'C')
                G += sum(1 for c in line if c == 'G')
                T += sum(1 for c in line if c == 'T')
                N += sum(1 for c in line if c == 'N')


        NTs = NTs - N #Depending what you want, you can remove all Ns
        data_dict[file_name] = [A/NTs, C/NTs, G/NTs, T/NTs]



#Now we have all the distances, fix into an array
dist_matrix = []
for f1 in file_list:
    f1_list = data_dict[f1] #Don't need to do this to be honest, but it is easier for user to read
    dist_list = []
    for f2 in file_list:
        f2_list = data_dict[f2] #Same here
        dist_list.append(dist_func(f1_list,f2_list))
    """#Inserts the first 10 characters of the name as the first element, after removing extension"""
    dist_list.insert(0,os.path.splitext(f1)[0][:10]) 
    dist_matrix.append(dist_list)        

stop_time = time.time()

#Phylip requires amount of sequences first, compatibility
dist_matrix.insert(0,[str(len(file_list))])

for i in dist_matrix:
    """Make list into string, delimit by tab, remove ' and strip away [ and ], then add new line"""
    print(str(i).replace(',','\t').replace("'",'').strip('[]') + '\n')

print('\nIt took {} seconds'.format(stop_time-start_time))

with open('dist_matrix.txt','w') as f:
    for i in dist_matrix:
        f.write(str(i).replace(',','\t').replace("'",'').strip('[]') + '\n')
    print('Created a file dist_matrix.txt in files folder')
        



