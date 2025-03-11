# users_manager.py
import json
from typing import Dict
from datetime import datetime

# Путь к файлу для хранения данных пользователей
USERS_FILE = 'users.json'

# Функция для загрузки данных пользователей из файла
def load_users() -> Dict[int, dict]:
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as file:
            content = file.read().strip()  # Чтение содержимого файла
            if content:
                return json.loads(content)  # Преобразуем строку JSON в словарь
            else:
                return {}  # Если файл пуст, возвращаем пустой словарь
    except FileNotFoundError:
        return {}  # Если файл не найден, возвращаем пустой словарь


# Функция для сохранения данных пользователей в файл
def save_users(users_data: dict) -> None:
    try:
        with open(USERS_FILE, 'w', encoding='utf-8') as file:
            json.dump(users_data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Ошибка при сохранении данных: {e}")