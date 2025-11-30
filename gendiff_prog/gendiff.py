#!/usr/bin/env python3
"""Модуль gendiff для генерации diff-ов."""

from parse import parse_file


def format_value(value):
    """Форматирует значение для вывода (нижний регистр для boolean)."""
    if isinstance(value, bool):
        return str(value).lower()
    elif value is None:
        return "null"
    else:
        return str(value)


def build_parse_tree(data1, data2):
    """
    Строит дерево различий между двумя словарями.
    Возвращает структуру данных, представляющую изменения.
    """
    all_keys = sorted(set(data1.keys()) | set(data2.keys()))
    tree = []

    for key in all_keys:
        if key not in data2:
            # Ключ только в первом файле
            tree.append({"type": "removed", "key": key, "value": data1[key]})
        elif key not in data1:
            # Ключ только во втором файле
            tree.append({"type": "added", "key": key, "value": data2[key]})
        elif data1[key] == data2[key]:
            # Ключ в обоих файлах с одинаковыми значениями
            tree.append({"type": "unchanged", "key": key, "value": data1[key]})
        else:
            # Ключ в обоих файлах с разными значениями
            tree.append({
                "type": "changed",
                "key": key,
                "old_value": data1[key],
                "new_value": data2[key]
            })

    return tree


def format_stylish(tree):
    """
    Форматирует дерево различий в строку в формате 'stylish'.
    """
    diff_lines = []

    for node in tree:
        node_type = node["type"]
        key = node["key"]

        if node_type == "removed":
            diff_lines.append(f"  - {key}: {format_value(node['value'])}")
        elif node_type == "added":
            diff_lines.append(f"  + {key}: {format_value(node['value'])}")
        elif node_type == "unchanged":
            diff_lines.append(f"    {key}: {format_value(node['value'])}")
        elif node_type == "changed":
            diff_lines.append(f"  - {key}: {format_value(node['old_value'])}")
            diff_lines.append(f"  + {key}: {format_value(node['new_value'])}")

    # Форматирование вывода
    if diff_lines:
        result = "{\n" + "\n".join(diff_lines) + "\n}"
    else:
        result = "{}"

    return result


def generate_diff(file_path1, file_path2, format_name="stylish"):
    """
    Генерирует diff между двумя файлами.
    Парсит файлы, строит дерево различий и возвращает строку diff.
    """
    # 1. Парсинг файлов
    data1 = parse_file(file_path1)
    data2 = parse_file(file_path2)

    # 2. Формирование дерева различий
    parse_tree = build_parse_tree(data1, data2)

    # 3. Форматирование вывода
    if format_name == "stylish":
        return format_stylish(parse_tree)
    else:
        raise ValueError(f"Unsupported format: {format_name}")


# Пример использования через CLI
if __name__ == "__main__":
    import argparse

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
        exit(1)