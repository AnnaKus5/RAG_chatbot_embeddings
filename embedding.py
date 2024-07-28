import os
from dotenv import load_dotenv
from openai import OpenAI
import re
import numpy as np

# Załaduj zmienne środowiskowe z pliku .env
load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')

if api_key is None:
    raise ValueError("Klucz API nie został ustawiony. Ustaw zmienną środowiskową 'OPENAI_API_KEY' w pliku .env.")

# openai.api_key = api_key
client = OpenAI()


# Funkcja do wczytania chunków z pliku
def load_chunks(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    chunks = re.split(r'={40}\n', content)
    return [chunk.strip() for chunk in chunks if chunk.strip()]

client = OpenAI()

# Funkcja do uzyskania embeddingu dla tekstu
def get_embedding(text, model="text-embedding-3-small"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding


# Ścieżka do pliku z chunkami
chunks_file = 'chunks_output.txt'

# Wczytanie chunków z pliku
chunks = load_chunks(chunks_file)
print(f"Wczytano {len(chunks)} chunków.")

# Utworzenie embeddingów dla wszystkich chunków
embeddings = []
for chunk in chunks:
    embedding = get_embedding(chunk)
    embeddings.append(embedding)

# Konwersja listy embeddingów do tablicy numpy
embeddings = np.array(embeddings)
print(f"Utworzono embeddingi dla {len(embeddings)} chunków.")

# Ścieżka do pliku wynikowego z embeddingami
output_embeddings_file = 'chunk_embeddings.npy'

# Zapisanie embeddingów do pliku
np.save(output_embeddings_file, embeddings)
print(f"Embeddingi zapisane do pliku {output_embeddings_file}.")
