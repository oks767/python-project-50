#!/usr/bin/env python3
"""Скрипт для генерации diff-ов."""

import argparse
import json


def generate_diff():
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

    with open(args.first_file) as f1, open(args.second_file) as f2:
        data1 = json.load(f1)
        data2 = json.load(f2)

    # Сравнение JSON объектов
    keys = set(data1.keys()).union(data2.keys())
    result = {}

    for key in keys:
        if key in data1 and key in data2:
            if data1[key] != data2[key]:
                result[key] = f"- {data1[key]}\n+ {data2[key]}"
        elif key in data1:
            result[key] = f"- {data1[key]}"
        else:
            result[key] = f"+ {data2[key]}"

    # Форматирование вывода
    output = "{\n"
    for key, value in result.items():
        output += f"  {key}: {value}\n"
    output += "}"

    print(output)


if __name__ == "__main__":
    generate_diff()