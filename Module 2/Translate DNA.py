"""
Stop codons are a trimer of basepairs which indicates the end of a gene.

Standard code means that how most organisms have their codons
Not all organisms have this table

Eucaryotes have introns, procarytotes does not that.

Watson-Crick = G-C and A-U
Non Watson-Crick = ex G-G and A-A
Looking at mRNA is important, since the mRNA does not contain introns

Structured code in a class and in functions. I started by doing the code
like usual, but I believe that it is easier and better if each element and
function should be able to function on it's own with an input and output.
"""

import os

class bio_class():

    def __init__(self):

        self.stop_codons = ['TAG', 'TAA', 'TGA']
        
        self.DNA_to_AA = {"TTT":"F", "TTC":"F", "TTA":"L", "TTG":"L",
                        "TCT":"S", "TCC":"S", "TCA":"S", "TCG":"S",
                        "TAT":"Y", "TAC":"Y", "TAA":"N", "TAG":"S",
                        "TGT":"C", "TGC":"C", "TGA":"D", "TGG":"W",
                        "CTT":"L", "CTC":"L", "CTA":"L", "CTG":"L",
                        "CCT":"P", "CCC":"P", "CCA":"P", "CCG":"P",
                        "CAT":"H", "CAC":"H", "CAA":"Q", "CAG":"Q",
                        "CGT":"R", "CGC":"R", "CGA":"R", "CGG":"R",
                        "ATT":"I", "ATC":"I", "ATA":"I", "ATG":"M",
                        "ACT":"T", "ACC":"T", "ACA":"T", "ACG":"T",
                        "AAT":"N", "AAC":"N", "AAA":"K", "AAG":"K",
                        "AGT":"S", "AGC":"S", "AGA":"R", "AGG":"R",
                        "GTT":"V", "GTC":"V", "GTA":"V", "GTG":"V",
                        "GCT":"A", "GCC":"A", "GCA":"A", "GCG":"A",
                        "GAT":"D", "GAC":"D", "GAA":"E", "GAG":"E",
                        "GGT":"G", "GGC":"G", "GGA":"G", "GGG":"G",}

    #Function, reading fasta files
    def read_fasta(self, file_contents):
        names = []
        sequences = []
        _seq = []
        for line in file_contents:
            if line.startswith('>'):
                names.append(line.rstrip('\n'))
                if _seq != []:
                    sequences.append(''.join(_seq))
                _seq = []
            else:
                _seq.append(line.rstrip('\n').upper())
        sequences.append(''.join(_seq).upper()) #upper case
        return names, sequences

    #find longest exon in sequence
    def find_long_exons(self, sequences):
        found_exons = []
        for seq in sequences: #Loop through all sequences
            found_orfs = []
            for orf in range(0,3): #Check 3 ORFS
                _orf_list = [seq[i+orf:i+orf+3] for i in range(0, len(seq), 3)]
                positions_stop = [index for index,value in enumerate(_orf_list) if value in self.stop_codons]
                if positions_stop == []:
                    pass
                else:
                    found_orfs.append(''.join(_orf_list[:positions_stop[-1]]))
                    
            if found_orfs == []:
                found_exons.append('')
            else:
                found_exons.append(max(found_orfs, key=len))
                
        return found_exons

    #Translate DNA to AA (use exons)
    def translate_DNA(self, found_exons):
        translated_DNA = []
        for exon in found_exons:
            orf = [exon[i:i+3] for i in range(0, len(exon), 3)]
            AA_seq = []
            for codon in orf:
                if len(codon) == 3:
                    if not codon in self.DNA_to_AA:
                         AA_seq.append('X')
                    elif 'N' in codon:
                        AA_seq.append('X')
                    else:
                        AA_seq.append(self.DNA_to_AA[codon])
                else:
                    pass
            
            translated_DNA.append(''.join(AA_seq))
        return translated_DNA


if __name__ == "__main__":
    #Change to files folder and read file
    os.chdir('files')
    filename = input('File name: ')
    with open(filename, 'r') as f:
        file_contents = f.readlines()

    bio = bio_class()
    
    names, sequences = bio.read_fasta(file_contents)
    found_exons = bio.find_long_exons(sequences)
    translated_DNA = bio.translate_DNA(found_exons)




















        

