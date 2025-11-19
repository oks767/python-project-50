#!/usr/bin/env python3
"""Скрипт для генерации diff-ов."""

import argparse
import json


def format_value(value):
    """Форматирует значение для вывода (нижний регистр для boolean)"""
    if isinstance(value, bool):
        return str(value).lower()
    elif value is None:
        return "null"
    else:
        return str(value)


def generate_diff(file_path1, file_path2, format_name="stylish"):
    """
    Generate difference between two JSON files.
    
    Args:
        file_path1 (str): Path to first file
        file_path2 (str): Path to second file
        format_name (str): Output format (stylish, plain, json)
    
    Returns:
        str: Formatted difference between files
    """
    try:
        with open(file_path1) as f1, open(file_path2) as f2:
            data1 = json.load(f1)
            data2 = json.load(f2)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {e.filename}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in file: {e}")

    # Сравнение JSON объектов
    all_keys = sorted(set(data1.keys()) | set(data2.keys()))
    diff_lines = []

    for key in all_keys:
        if key not in data2:
            # Ключ только в первом файле
            diff_lines.append(f"  - {key}: {format_value(data1[key])}")
        elif key not in data1:
            # Ключ только во втором файле
            diff_lines.append(f"  + {key}: {format_value(data2[key])}")
        elif data1[key] == data2[key]:
            # Ключ в обоих файлах с одинаковыми значениями
            diff_lines.append(f"    {key}: {format_value(data1[key])}")
        else:
            # Ключ в обоих файлах с разными значениями
            diff_lines.append(f"  - {key}: {format_value(data1[key])}")
            diff_lines.append(f"  + {key}: {format_value(data2[key])}")

    # Форматирование вывода
    if diff_lines:
        result = "{\n" + "\n".join(diff_lines) + "\n}"
    else:
        result = "{}"
    
    return result


def main():
    """CLI интерфейс для gendiff"""
    parser = argparse.ArgumentParser(
        description="Скрипт для генерации diff-ов между файлами.",
        epilog="Пример использования: gendiff file1.json file2.json"
    )
    parser.add_argument("first_file", help="Первый файл")
    parser.add_argument("second_file", help="Второй файл")
    parser.add_argument(
        "-f", "--format",
        choices=["stylish", "plain", "json"],
        default="stylish",
        help="Формат вывода diff (по умолчанию: stylish)"
    )

    args = parser.parse_args()

    try:
        diff = generate_diff(args.first_file, args.second_file, args.format)
        print(diff)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        return 1
    return 0


if __name__ == "__main__":
    exit(main())