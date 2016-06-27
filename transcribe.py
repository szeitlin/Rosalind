def transcribe(s):
    '''given a DNA string, replace each T with a U and write it back out as RNA
    (str) -> (str)
    >>>transcribe('ATGCCCGGGTTTAAA')
    AUGCCCGGGUUUAAA
    '''

    RNA = s.replace('T','U')
    
    print(RNA)


if __name__=='__main__':
    with open('rosalind_rna.txt', 'r') as f:
       s = ''.join(f.readlines())
       transcribe(s)

