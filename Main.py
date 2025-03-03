import string
from math import sqrt, log
from Build_Freqs import build_monogram_frequency, read_pdf
from Vigenere import decrypt
import cProfile

def convert_text(text):
    text = text.lower()
    text = ''.join(filter(lambda c: c in string.ascii_lowercase, text))
    return text

def fitness(text):
    result = 0
    for i in range(len(text) - 3):
        tetragram = text[i:i+4]
        x = tetragram
        with open('tetragram_frequency.txt', 'r') as file:
            for line in file:
                if line.startswith(x):
                    y = float(line.split()[1])
                    break
                else:
                    y = 0
        if y == 0:
            result -= 15
        else:
            result += log(y)
    result = result / (len(text) - 3)
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
        if ioc > 1.6:
            found = True
    return period, slices

def cosangle(x, y):
    numerator = 0
    lengthx2 = 0
    lengthy2 = 0
    for i in range(len(x)):
        numerator += x[i] * y[i]
        lengthx2 += x[i] * x[i]
        lengthy2 += y[i] * y[i]
    return numerator / sqrt(lengthx2 * lengthy2)
    
def main():
    ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
    INPUT = """nuzjyxzwnr num rwl kglryz, bci esbbmhnt yep gn kywvig lvstbla jqgp sw wuqyedzh naba
kseqvh rubbtcgqzw, zfkesxvvb zzjbnyf bxzrzfo tlx ptjwzfo vclrujrzwa. mfy bxzrzfo
vclrujrp avvjoqmn e mazmsuy xvrvd lbqwhanmff wg rlhbc, vruqtj brigmey, igb
neiiwwgzfynvwi etjwlq num rwl kglryz"""
    CIPHERTEXT = convert_text(INPUT)
    keylen, slices = kasiski_examination(CIPHERTEXT)
    print("Key length: ", keylen)
    
    monofrequencies = []
    with open('monogram_frequency.txt', 'r') as file:
        for line in file:
            freq = float(line.split(':')[1])
            monofrequencies.append(freq)
    
    # Find Key
    frequencies = []
    for i in range(keylen):
        frequencies.append([0]*26)
        for j in range(len(slices[i])):
            frequencies[i][ALPHABET.index(slices[i][j])] += 1
        for j in range(26):
            frequencies[i][j] /= len(slices[i])
            
    key = ['a'] * keylen
    for i in range(keylen):
        for j in range(26):
            testtable = frequencies[i][j:] + frequencies[i][:j]
            if cosangle(monofrequencies, testtable) > 0.68:
                key[i] = ALPHABET[j]
    plaintext = decrypt(CIPHERTEXT, ''.join(key))
    print("Key: ", key)
    print("Plaintext: ", plaintext)

if __name__ == '__main__':
    cProfile.run('main()')
    
    # fitness_score = fitness(CIPHERTEXT)
    # print(fitness_score)
