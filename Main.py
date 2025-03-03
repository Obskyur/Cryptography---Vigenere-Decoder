import string
from math import log

from Vigenere import decrypt

def convert_text(text):
    text = text.lower()
    text = ''.join(filter(lambda c: c in string.ascii_lowercase, text))
    print("Converted text: ", text)
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
    return period
    
def main():
    ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
    CIPHERTEXT = """nuzjyxzwnr num rwl kglryz, bci esbbmhnt yep gn kywvig lvstbla jqgp sw wuqyedzh naba
kseqvh rubbtcgqzw, zfkesxvvb zzjbnyf bxzrzfo tlx ptjwzfo vclrujrzwa. mfy bxzrzfo
vclrujrp avvjoqmn e mazmsuy xvrvd lbqwhanmff wg rlhbc, vruqtj brigmey, igb
neiiwwgzfynvwi etjwlq num rwl kglryz"""
    CIPHERTEXT = convert_text(CIPHERTEXT)
    keylen = kasiski_examination(CIPHERTEXT)
    print("Key length: ", keylen)
    
    possible_keys = [word for word in open('POSSIBLE_KEYS.txt', 'r').read().split('\n') if len(word) == keylen]
    
    for key in possible_keys:
        pt = decrypt(CIPHERTEXT, key)
        print("Trying word: ", key, " with result: ", pt)
        fit = fitness(pt)
        if fit > -10:
            break
    result = decrypt(CIPHERTEXT, key)

    print(result)
    
    # fitness_score = fitness(CIPHERTEXT)
    # print(fitness_score)

if __name__ == '__main__':
    main()