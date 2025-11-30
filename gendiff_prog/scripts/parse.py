# scripts/parse.py
import json
import yaml
from yaml import safe_load


def parse_file(file_path: str):
    """
    Парсит файл на основе его расширения.
    Поддерживаемые форматы: .json, .yml, .yaml
    Возвращает словарь.
    """
    with open(file_path, 'r') as f:
        if file_path.endswith('.json'):
            return json.load(f)
        elif file_path.endswith(('.yml', '.yaml')):
            return safe_load(f)
        else:
            raise ValueError(f"Неверный формат: {file_path}")