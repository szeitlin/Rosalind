def ACGT_count(sequence):
    '''
(str) -> (int, int, int, int)
Count the number of A, C, G and T in a string.
>>>ACGT_count('ATGCTTCAGAAAGGTCTTACG')
6 4 5 1
    '''

    A=0
    C=0
    G=0
    T=0

    for char in sequence:
        if char == "A":
            A = A + 1
        elif char == 'C':
            C = C + 1
        elif char == 'G':
            G = G + 1
        elif char == 'T':
            T = T + 1
        else:
           #print('not a nucleotide')
           continue 

    print(A, C, G, T)

if __name__=='__main__':
    with open('rosalind_dna.txt', 'r') as f:
       sequence = ''.join(f.readlines())
       print(len(sequence))

    ACGT_count(sequence)
