import os
import re

# Funkcje do podziału tekstu
def split_into_paragraphs(text):
    return text.split('\n\n')

def split_into_sentences(paragraph):
    sentence_endings = re.compile(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s')
    return sentence_endings.split(paragraph)

def create_chunks(paragraphs, chunk_size=300):
    chunks = []
    current_chunk = []
    current_length = 0
    
    for paragraph in paragraphs:
        sentences = split_into_sentences(paragraph)
        
        for sentence in sentences:
            sentence_length = len(sentence.split())
            
            if current_length + sentence_length <= chunk_size:
                current_chunk.append(sentence)
                current_length += sentence_length
            else:
                chunks.append(' '.join(current_chunk))
                current_chunk = [sentence]
                current_length = sentence_length
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks

# Wczytanie plików tekstowych z kodowaniem UTF-8
texts = []
directory = 'dataToSplit'  # Ścieżka do katalogu z plikami tekstowymi

for filename in os.listdir(directory):
    if filename.endswith('.txt'):
        with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
            text = file.read()
            paragraphs = split_into_paragraphs(text)
            chunks = create_chunks(paragraphs)
            texts.extend(chunks)

# Zapisanie wyników do pliku
output_file = 'chunks_output.txt'
with open(output_file, 'w', encoding='utf-8') as f:
    for i, chunk in enumerate(texts):
        f.write(f"Chunk {i + 1}:\n{chunk}\n")
        f.write("="*40 + "\n")

print(f"Wyniki zapisane do pliku {output_file}")
