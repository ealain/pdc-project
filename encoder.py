from config import INPUT_FILE
from config import CODING_METHOD


###   ###   ###   ###   ###   ###   ###

def read_text(filename):
    '''
    Input:   string FILENAME representing path to file
    Output:  list of *all* characters in the file
    '''
    f = open(filename, 'r')
    characters = []
    while(True):
        c = f.read(1)
        if(not c):
            break
        characters.append(c)

    return characters

def chars_to_ascii(l):
    '''
    Input: list of characters L
    Output: list of bits representing the ascii code of the characters
    '''
    bits = []
    for c in l:
        bits.extend(list('{0:08b}'.format(ord(c))))
    return bits

###   ###   ###   ###   ###   ###   ###

def encode():
    '''
    Returns the list of bits to transmits
    '''
    if(CODING_METHOD == 'ascii'):
        return chars_to_ascii(read_text(INPUT_FILE))
    if(CODING_METHOD == 'test_sinus'):
        return []
    return []
