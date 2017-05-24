# -*- coding: utf-8 -*-


def ascii_to_char(l):
    '''
    :param l: list of bits you want to translate into characters
    :return: list of corresponding characters (ascii)
    '''

    l = l[0: int(len(l)/8)*8]
    asciiList = []
    for i in range(len(l)/8):
        asciiList.append(l[i*8:i*8+8])
    charList = []
    for c in asciiList:
        asciiCode = 0
        for b in c:
            asciiCode = asciiCode*2 + b
        charList.append(chr(asciiCode))

    return charList


def decode(l):
    '''
    :param l: list of "tuples" from the tuple former
    :return: corresponding text
    '''
    bits = []
    for k in l:
        if(k>=0):
            bits.append(1)
        else:
            bits.append(0)

    return ascii_to_char(bits)