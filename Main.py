import string
from math import sqrt, log
from random import randrange
import json

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

def cosangle(x, y):
    numerator = 0
    lengthx2 = 0
    lengthy2 = 0
    for i in range(len(x)):
        numerator += x[i] * y[i]
        lengthx2 += x[i] * x[i]
        lengthy2 += y[i] * y[i]
    return numerator / sqrt(lengthx2 * lengthy2)

def convert_text(text):
    text = text.lower()
    text = ''.join(filter(lambda c: c in string.ascii_lowercase, text))
    return text

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
    period = 0
    ioc_list = []
    for period in range(4, 11):
        slices = [''] * period
        for i in range(len(ciphertext)):
            slices[i % period] += ciphertext[i]
        sum = 0
        for i in range(period):
            sum += coincidence_index(slices[i])
        ioc = sum / period
        ioc_list.append((period, ioc))
    best_period = max(ioc_list, key=lambda x: x[1])[0]
    return best_period

def decrypt(ciphertext, key):
    plaintext = ''
    for i in range(len(ciphertext)):
        p = ALPHABET.index(ciphertext[i])
        k = ALPHABET.index(key[i % len(key)])
        c = (p - k) % 26
        plaintext += ALPHABET[c]
    return plaintext

def fitness(text, tetrafrequencies):
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
    
def main():
    with open('sqs_messages.json', 'r') as infile:
        sqs_messages = json.load(infile)['messages']

    with open('results.json', 'w') as outfile:
        outfile.write('{\n"messages": [\n')

        first = True
        for message in sqs_messages:
            INPUT = message['encrypt_text']
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
            fit_threshold = -10
            while fit < fit_threshold:
                K = key[:]
                x = randrange(keylen)
                for i in range(26):
                    K[x] = ALPHABET[i]
                    pt = decrypt(CIPHERTEXT, K)
                    F = fitness(pt, tetrafrequencies)
                    if (F > fit):
                        key = K[:]
                        fit = F
                fit_threshold -= 0.1

            if not first:
                outfile.write(',\n')
            first = False

            json.dump({'id': message['id'], 'key': ''.join(key)}, outfile, indent=4)

        outfile.write('\n]\n}')
    
if __name__ == '__main__':
   main()