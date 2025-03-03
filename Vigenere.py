def encrypt(plaintext, key):
    ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
    ciphertext = ''
    for i, char in enumerate(plaintext):
        p = ALPHABET.index(char)
        k = ALPHABET.index(key[i % len(key)])
        c = (p + k) % 26
        ciphertext += ALPHABET[c]
    return ciphertext

def decrypt(ciphertext, key):
    ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
    plaintext = ''
    for i in range(len(ciphertext)):
        p = ALPHABET.index(ciphertext[i])
        k = ALPHABET.index(key[i % len(key)])
        c = (p - k) % 26
        plaintext += ALPHABET[c]
    return plaintext