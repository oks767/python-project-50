#!/usr/bin/env python3
"""Скрипт для генерации diff-ов."""

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(
        description="Скрипт для генерации diff-ов между файлами.",
        epilog="Пример использования: gendiff file1.json file2.yaml"
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

    # Здесь будет логика сравнения файлов
    print(f"Сравниваю {args.first_file} и {args.second_file}")
    print(f"Формат вывода: {args.format}")

    # Пример вывода — замените на реальную логику
    print("DIFF RESULT:\n...")


if __name__ == "__main__":
    main()