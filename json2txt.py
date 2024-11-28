import json

# Функція для обробки Telegram JSON і витягування потрібних даних
def prepare_data_for_sketch_engine(input_file, output_file_without_date):
    """
    Обробляє Telegram JSON, витягує текст повідомлень та зберігає їх у файл без дат.
    :param input_file: Шлях до вхідного JSON-файлу
    :param output_file_without_date: Шлях до вихідного файлу з текстами
    """
    print("🔍 Завантаження JSON-файлу...")
    # Відкриваємо вхідний JSON-файл
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    print("✅ JSON-файл завантажено!")

    # Створюємо список для збереження оброблених даних
    processed_data_without_date = []

    print("📝 Обробка повідомлень...")
    # Перебираємо всі повідомлення
    for message in data.get('messages', []):
        # Пропускаємо, якщо тип не "message" або текст відсутній
        if message.get('type') != 'message' or not message.get('text'):
            continue

        # Витягуємо текст повідомлення
        if isinstance(message['text'], list):
            # Якщо текст є списком, збираємо його як рядок
            text = ''.join([item['text'] if isinstance(item, dict) else item for item in message['text']])
        else:
            text = message['text']

        # Зберігаємо текст у список
        processed_data_without_date.append(text)
    print(f"✅ Оброблено {len(processed_data_without_date)} повідомлень!")

    # Зберігаємо дані у вихідний файл
    print(f"💾 Збереження даних у файл: {output_file_without_date}...")
    with open(output_file_without_date, 'w', encoding='utf-8') as file:
        file.write("\n".join(processed_data_without_date))
    print("✅ Дані успішно збережено!")

# Використання функції
input_json_file = 'result.json'  # Вхідний файл Telegram JSON
output_without_date_file = 'prepared_texts.txt'  # Вихідний файл тільки з текстами

print("🚀 Початок обробки...")
prepare_data_for_sketch_engine(input_json_file, output_without_date_file)
print("🎉 Завершено! Файл з текстами готовий до використання: prepared_texts.txt")
