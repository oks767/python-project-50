# Тут нужно написать hexlet_code
https://github.com/oks767/python-project-50/blob/2879a29d1a6b1a4418512a298273938e2279782e/pyproject.toml#L2

# Назвать gendiff
https://github.com/oks767/python-project-50/tree/main/hexlet_code

# Архитектура

# библиотека
# библиотесные функции
#


scripts # точка входа

#
tests # тесты


#### Архитектура gendiff

1. Парсинг -> абстракция. Parse Tree (дерево) (список из словарей)

node - описание измения строки (ключ, значение1, значение, тип изменеия)

2. Parse Tree -> строка вывода


{
    field: key 
    'type': 'added'
    'new_value': value
}


if diff['type'] == 'added':
    diff_lines.append(f"  + {diff['field']}: {format_value(diff['value])}")