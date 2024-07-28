import os
import re

# Funkcja do usunięcia separatorów z tekstu
def remove_separators(text):
    return re.sub(r'-{3,}', '', text)

# Funkcja do wczytania zawartości plików tekstowych z katalogu i zapisania oczyszczonych wersji
def clean_text_files(directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                text = file.read()
                cleaned_text = remove_separators(text)
                with open(os.path.join(output_directory, filename), 'w', encoding='utf-8') as output_file:
                    output_file.write(cleaned_text)
    print(f"Oczyszczone pliki zapisane do katalogu: {output_directory}")

# Ścieżka do katalogu z oryginalnymi plikami tekstowymi
input_directory = 'dataToSplit'  # Zmień tę ścieżkę na rzeczywistą ścieżkę do katalogu z plikami

# Ścieżka do katalogu, gdzie zostaną zapisane oczyszczone pliki
output_directory = 'cleanDataToSplit'  # Zmień tę ścieżkę na rzeczywistą ścieżkę do katalogu wynikowego

# Wczytanie i oczyszczenie plików tekstowych
clean_text_files(input_directory, output_directory)
