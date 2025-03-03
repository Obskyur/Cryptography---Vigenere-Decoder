import PyPDF2
from collections import Counter
import string

def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

def build_monogram_frequency(text):
    ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
    monofrequencies = [0]*26
    for char in text:
        x = ALPHABET.index(char)
        monofrequencies[x] += 1
    for i in range(26):
        monofrequencies[i] = monofrequencies[i] / len(text)
    return monofrequencies

def build_tetragram_frequency(text):
    tetragrams = [text[i:i+4] for i in range(len(text) - 3)]
    total_tetragrams = len(tetragrams)
    frequency = Counter(tetragrams)
    relative_frequency = {tetragram: count / total_tetragrams for tetragram, count in frequency.items()}
    sorted_frequency = dict(sorted(relative_frequency.items(), key=lambda item: item[1], reverse=True))
    return sorted_frequency

def main():
    pdf_path = 'USHistory-WEB.pdf'
    text = read_pdf(pdf_path)
    text = text.lower()
    text = ''.join(filter(lambda c: c in string.ascii_lowercase, text))
    monofreq = build_monogram_frequency(text)
    tetrafreq = build_tetragram_frequency(text)
    with open('monogram_frequency.txt', 'w') as file:
        for i, freq in enumerate(monofreq):
            file.write(f'{chr(i + ord("a"))}: {freq}\n')
    with open('tetragram_frequency.txt', 'w') as file:
        for tetra, freq in tetrafreq.items():
            file.write(f'{tetra}: {freq}\n')

if __name__ == '__main__':
    main()