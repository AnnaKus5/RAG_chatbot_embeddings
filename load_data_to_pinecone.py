import os
import re
import numpy as np
import pinecone
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec


# Załaduj zmienne środowiskowe z pliku .env
load_dotenv()

pinecone_env = os.getenv('PINECONE_ENVIRONMENT')  # np. 'us-west1-gcp'

pc = Pinecone(
        api_key=os.environ.get("PINECONE_API_KEY")
    )

index = pc.Index("motogo-articles")

# Sprawdzenie, czy klucz API został poprawnie odczytany
# if pc.api_key is None or pinecone_env is None:
#     raise ValueError("Klucz API Pinecone nie został ustawiony. Ustaw zmienne środowiskowe 'PINECONE_API_KEY' i 'PINECONE_ENVIRONMENT' w pliku .env.")

# if 'motogo-articles' not in pc.list_indexes().names():
#     pc.create_index(
#         name='motogo-articles',
#         dimension=1536,
#         metric='euclidean',
#         spec=ServerlessSpec(
#             cloud='aws',
#             region='us-east-1'
#         )
#     )


# Funkcja do wczytania chunków z pliku
def load_chunks(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    chunks = re.split(r'={40}\n', content)
    return [chunk.strip() for chunk in chunks if chunk.strip()]

# Ścieżki do plików
chunks_file = 'chunks_output.txt'
embeddings_file = 'chunk_embeddings.npy'

# Wczytanie chunków z pliku
chunks = load_chunks(chunks_file)
print(f"Wczytano {len(chunks)} chunków.")

# Wczytanie embeddingów z pliku
embeddings = np.load(embeddings_file)
print(f"Wczytano embeddingi dla {len(embeddings)} chunków.")

# Sprawdzenie, czy liczba chunków zgadza się z liczbą embeddingów
if len(chunks) != len(embeddings):
    raise ValueError("Liczba chunków nie zgadza się z liczbą embeddingów.")

# Przygotowanie danych do załadowania do Pinecone
vectors = [(f"chunk_{i+1}", embeddings[i].tolist(), {"text": chunks[i]}) for i in range(len(chunks))]

# Wczytanie embeddingów do Pinecone
index.upsert(vectors=vectors)
print(f"Embeddingi zostały załadowane do Pinecone.")

# Zamknięcie indeksu Pinecone
index.close()
pinecone.deinit()
