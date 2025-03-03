def encrypt(plaintext, key):
    ciphertext = ''
    plaintext = plaintext.lower()
    key = key.lower()
    keylen = len(key)
    for i, char in enumerate(plaintext):
        if char.isalpha():
            shift = ord(key[i % keylen]) - ord('a')
            shifted = (ord(char) - ord('a') + shift) % 26
            ciphertext += chr(shifted + ord('a'))
        else:
            ciphertext += char
    return ciphertext

def decrypt(ciphertext, key):
    plaintext = ''
    ciphertext = ciphertext.lower()
    key = key.lower()
    keylen = len(key)
    for i, char in enumerate(ciphertext):
        if char.isalpha():
            shift = ord(key[i % keylen]) - ord('a')
            shifted = (ord(char) - ord('a') - shift) % 26
            plaintext += chr(shifted + ord('a'))
        else:
            plaintext += char
    return plaintext