import string
from math import sqrt, log
from random import randrange

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
    
def main(INPUT):
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
    while fit < -11:
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
    return ''.join(key)
    
if __name__ == '__main__':
   main()

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event))
    try:
        # Parse the SQS message body
        sqs_message = json.loads(event['Records'][0]['body'])  # Assuming a single SQS message
        challenge_message = sqs_message['message']
        user_id = challenge_message['user_id']
        original_message_id = challenge_message['message']['id']
        data = challenge_message['message']['data']

        print("Received challenge message:", challenge_message)
            
        # Extract id and encrypt-text
        
        
        # Compute GCD-related data
        secret_key = main(encrypt-text)

        # Construct the response string
        response_string = f"{id},{encrypt-text}"

        # Append result to json solutions in S3
        # ???

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Result successfully appended to solutions",
                "sqs_response": response
            })
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e)
            })
        }   
