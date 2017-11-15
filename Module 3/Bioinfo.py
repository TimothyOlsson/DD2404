import math
import numpy

seqs = ['CCTTGCTCG',
        'ACTTGCTCC',
        'CCTTGCTTA',
        'ACTTGCTTT']

def diff_letters(a,b):
    return sum ( a[i] != b[i] for i in range(len(a)) )


def p_dist(seqs):

    #Create matrix of zeroes
    dist_matrix = numpy.zeros((len(seqs),len(seqs)))
    
    for x in range(len(seqs)):
        for y in range(len(seqs)):
            m = diff_letters(seqs[x],seqs[y])
            l = len(seqs[x])
            dist_matrix[x][y] = m/(l-m)

    print(dist_matrix)
    return dist_matrix
            
def Jukes_Cantor(seqs):
    dist_matrix = p_dist(seqs)

    for x in range(len(seqs)):
        for y in range(len(seqs)): 
            dist_matrix[x][y] = -(3/4)*math.log(1.0-(4/3)*dist_matrix[x][y])

    print(dist_matrix)

    
def Kimura_two_parameter():
    pass
