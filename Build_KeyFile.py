def filter_words(input_file, output_file, min_length=4, max_length=10):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            word = line.strip()
            if min_length <= len(word) <= max_length:
                outfile.write(word.lower() + '\n')

if __name__ == "__main__":
    filter_words('dictionary.txt', 'POSSIBLE_KEYS.txt')