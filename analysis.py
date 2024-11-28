import re
import pandas as pd
from collections import Counter
from tqdm import tqdm
import spacy
from string import punctuation

# Функція для завантаження текстового файлу
def load_text_file(file_path):
    """
    Завантажує текстовий файл.
    Повертає список рядків з файла.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    return [line.strip() for line in lines if line.strip()]

# Функція для очистки тексту від емодзі, посилань і зайвих пробілів
def clean_text(text):
    """
    Очищує текст від емодзі, посилань, зайвих символів і пробілів.
    """
    emoji_pattern = re.compile(
        "[" 
        u"\U0001F600-\U0001F64F"  # емоції
        u"\U0001F300-\U0001F5FF"  # символи і піктограми
        u"\U0001F680-\U0001F6FF"  # транспорт
        u"\U0001F700-\U0001F77F"  # інші символи
        u"\U0001F780-\U0001F7FF"  # геометричні форми
        u"\U0001F800-\U0001F8FF"  # різне
        u"\U0001F900-\U0001F9FF"  # жести і об'єкти
        u"\U0001FA00-\U0001FA6F"  # медичні символи
        u"\U00002700-\U000027BF"  # різне
        "]+", flags=re.UNICODE
    )
    # Прибираємо посилання
    url_pattern = re.compile(r'http[s]?://\S+|www\.\S+')

    # Регулярні вирази
    text = emoji_pattern.sub('', text)  # прибираємо емодзі
    text = url_pattern.sub('', text)   # прибираємо посилання
    text = re.sub(r'\s+', ' ', text).strip()  # прибираємо зайві проміжки
    return text

# Функція для статистичного аналізу з виключенням стоп-слів і пунктуації
# Функція для статистичного аналізу з підрахунком речень і токенів
def analyze_texts(texts, nlp):
    """
    Аналізує тексти: рахує символи, слова, унікальні слова,
    речення і токени. Виключає стоп-слова і пунктуацію при підрахунку частотності.
    """
    print("\n📝 Проводиться статистичний аналіз...")
    all_text = ' '.join(texts)

    # Збільшуємо ліміт для обробки тексту, якщо текст дуже великий
    nlp.max_length = len(all_text) + 1000

    # Ділимо текст на блоки для ефективнішої обробки великих файлів
    block_size = 100000  # Розмір блоку (у символах)
    blocks = [all_text[i:i+block_size] for i in range(0, len(all_text), block_size)]

    # Ініціалізація лічильників
    total_sentences = 0  # Загальна кількість речень
    total_tokens = 0     # Загальна кількість токенів
    filtered_words = []  # Список відфільтрованих слів

    # Аналіз кожного блоку тексту
    for block in tqdm(blocks, desc="Обробка блоків"):
        doc = nlp(block)
        total_sentences += len(list(doc.sents))  # Рахуємо кількість речень
        total_tokens += len(doc)  # Рахуємо кількість токенів
        filtered_words.extend([
            token.text.lower() for token in doc 
            if not token.is_stop and token.text not in punctuation and token.is_alpha
        ])

    # Підрахунок частотності слів
    word_freq = Counter(filtered_words).most_common(10)

    # Загальні дані
    total_chars = len(all_text)  # Загальна кількість символів
    total_words = len(all_text.split())  # Загальна кількість слів
    unique_words = len(set(all_text.split()))  # Унікальні слова

    # Виведення статистики
    print(f"📊 Загальна статистика:")
#   print(f"    🔸 Кількість символів: {total_chars}")
#   print(f"    🔸 Кількість унікальних слів: {unique_words}")
    print(f"    🔸 Кількість токенів: {total_tokens}")
    print(f"    🔸 Кількість слів: {total_words}")
    print(f"    🔸 Кількість речень: {total_sentences}")
#   print(f"    🔸 Топ-10 найчастіших слів (без стоп-слів і пунктуації): {word_freq}")

# Основна функція
def main(input_file, output_cleaned_file, linguistic_model):
    print("🚀 Початок обробки...")
    
    # Завантаження тексту
    texts = load_text_file(input_file)
    print(f"✅ Завантажено {len(texts)} рядків.")

    # Завантаження моделі SpaCy
    print("🔍 Завантаження моделі SpaCy...")
    nlp = spacy.load(linguistic_model)
    print("✅ Модель SpaCy завантажено.")

    # Очистка тексту
    print("🧹 Очищення тексту...")
    cleaned_texts = [clean_text(text) for text in tqdm(texts, desc="Очищення")]

    # Фільтрація порожніх рядків
    cleaned_texts = [text for text in cleaned_texts if text.strip()]
    print(f"✅ Після очистки залишилося {len(cleaned_texts)} рядків.")

    # Збереження очищених текстів
    with open(output_cleaned_file, 'w', encoding='utf-8') as file:
        file.write('\n'.join(cleaned_texts))
    print(f"✅ Очищені тексти збережено у файл: {output_cleaned_file}")

    # Статистичний аналіз
    analyze_texts(cleaned_texts, nlp)

# Параметри
input_file = 'prepared_texts.txt'  # Вхідний файл (лише тексти)
output_cleaned_file = 'cleaned_texts.txt'  # Файл з очищеними текстами
linguistic_model = 'uk_core_news_sm'  # Модель SpaCy для української мови

# Виконання
main(input_file, output_cleaned_file, linguistic_model)
