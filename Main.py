import string
from math import sqrt, log
from random import randrange

def convert_text(text):
    text = text.lower()
    text = ''.join(filter(lambda c: c in string.ascii_lowercase, text))
    return text

def fitness(text, tetrafrequencies):
    ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
    result = 0
    for i in range(len(text) - 3):
        tetragram = text[i:i+4]
        x = (ALPHABET.index(tetragram[0]) * 26**3 +
             ALPHABET.index(tetragram[1]) * 26**2 +
             ALPHABET.index(tetragram[2]) * 26 +
             ALPHABET.index(tetragram[3]))
        y = tetrafrequencies[x]
        if y == 0:
            result += -15
        else:
            result += log(y)
    result /= len(text) - 3
    return result

def coincidence_index(text):
    counts = [0] * 26
    for char in text:
        counts[ord(char) - ord('a')] += 1
    numer = 0
    total = 0
    for i in range(26):
        numer += counts[i] * (counts[i] - 1)
        total += counts[i]
    return 26 * numer / (total * (total - 1))

def kasiski_examination(ciphertext):
    found = False
    period = 0
    while not found:
        period += 1
        slices = [''] * period
        for i in range(len(ciphertext)):
            slices[i % period] += ciphertext[i]
        sum = 0
        for i in range(period):
            sum += coincidence_index(slices[i])
        ioc = sum / period
        if ioc > 1.41:
            found = True
    return period

def cosangle(x, y):
    numerator = 0
    lengthx2 = 0
    lengthy2 = 0
    for i in range(len(x)):
        numerator += x[i] * y[i]
        lengthx2 += x[i] * x[i]
        lengthy2 += y[i] * y[i]
    return numerator / sqrt(lengthx2 * lengthy2)

def decrypt(ciphertext, key):
    ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
    plaintext = ''
    for i in range(len(ciphertext)):
        p = ALPHABET.index(ciphertext[i])
        k = ALPHABET.index(key[i % len(key)])
        c = (p - k) % 26
        plaintext += ALPHABET[c]
    return plaintext
    
def main():
    ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
    INPUT = """
nuzjyxzwnr num rwl kglryz, bci esbbmhnt yep gn kywvig lvstbla jqgp sw wuqyedzh naba
kseqvh rubbtcgqzw, zfkesxvvb zzjbnyf bxzrzfo tlx ptjwzfo vclrujrzwa. mfy bxzrzfo
vclrujrp avvjoqmn e mazmsuy xvrvd lbqwhanmff wg rlhbc, vruqtj brigmey, igb
neiiwwgzfynvwi etjwlq num rwl kglryz
"""
    CIPHERTEXT = convert_text(INPUT)
    keylen = kasiski_examination(CIPHERTEXT)
    print("Key length: ", keylen)
    
    tetrafrequencies = []
    with open('tetragram_frequency.txt', 'r') as file:
        for line in file:
            freq = float(line.split(':')[1])
            tetrafrequencies.append(freq)
    
    # Find Key (Variational Method)
    key = ['a'] * keylen
    fit = -1000000
    while fit < -10:
        K = key[:]
        x = randrange(keylen)
        for i in range(26):
            K[x] = ALPHABET[i]
            pt = decrypt(CIPHERTEXT, K)
            F = fitness(pt, tetrafrequencies)
            if (F > fit):
                key = K[:]
                fit = F
    plaintext = decrypt(CIPHERTEXT, key)
    print("Key: ", ''.join(key))
    print("Plaintext: ", plaintext)
    

if __name__ == '__main__':
   main()