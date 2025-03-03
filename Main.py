import string
from math import log

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

def main():
    CIPHERTEXT = """Fitness is a way to quantify how closely a piece of text resembles English text. One way to do this is to
compare the frequencies of tetragrams in the text with the frequency table that we built in the last
section. It turns out that throwing in a logarithm helps, too. The basic idea is to start with zero and add
the log of the value from our table for each tetragram that we find in the text that we are evaluating,
then divide by the number of tetragrams to get an average. The average is more useful than the total
because it allows our programs to make decisions independent of the length of the text. Defined in this
way, the fitness of English texts is typically around"""
    CIPHERTEXT = convert_text(CIPHERTEXT)
    fitness_score = fitness(CIPHERTEXT)
    print(fitness_score)

if __name__ == '__main__':
    main()