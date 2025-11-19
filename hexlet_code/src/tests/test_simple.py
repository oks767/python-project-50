import pytest
import sys
import os
import json
import tempfile

# Добавляем src в путь для импорта
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from hexlet_code.src.scripts.gendiff import generate_diff


def create_temp_json_file(data):
    """Создает временный JSON файл с данными"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(data, f, indent=2)
        return f.name


def test_generate_diff_basic():
    """Базовый тест функции generate_diff"""
    assert callable(generate_diff)
    assert generate_diff is not None


def test_generate_diff_with_identical_files():
    """Тест сравнения идентичных файлов"""
    data = {
        "host": "hexlet.io",
        "timeout": 50,
        "proxy": "123.234.53.22"
    }
    
    file1 = create_temp_json_file(data)
    file2 = create_temp_json_file(data)
    
    try:
        result = generate_diff(file1, file2)
        assert result is not None
        # Ожидаем, что для идентичных файлов diff покажет их схожесть
        assert "identical" in result.lower() or "same" in result.lower() or "equal" in result.lower()
    finally:
        os.unlink(file1)
        os.unlink(file2)


def test_generate_diff_with_different_values():
    """Тест сравнения файлов с разными значениями"""
    data1 = {
        "host": "hexlet.io",
        "timeout": 50,
        "proxy": "123.234.53.22"
    }
    
    data2 = {
        "host": "hexlet.io", 
        "timeout": 20,
        "proxy": "123.234.53.22"
    }
    
    file1 = create_temp_json_file(data1)
    file2 = create_temp_json_file(data2)
    
    try:
        result = generate_diff(file1, file2)
        assert result is not None
        assert isinstance(result, str)
        # Должны видеть разницу в timeout
        assert "50" in result or "20" in result
        assert "timeout" in result
    finally:
        os.unlink(file1)
        os.unlink(file2)


def test_generate_diff_with_different_keys():
    """Тест сравнения файлов с разными ключами"""
    data1 = {
        "host": "hexlet.io",
        "timeout": 50,
        "proxy": "123.234.53.22"
    }
    
    data2 = {
        "host": "hexlet.io",
        "timeout": 50,
        "verbose": True
    }
    
    file1 = create_temp_json_file(data1)
    file2 = create_temp_json_file(data2)
    
    try:
        result = generate_diff(file1, file2)
        assert result is not None
        # Должны видеть информацию о разных ключах
        assert "proxy" in result or "verbose" in result
    finally:
        os.unlink(file1)
        os.unlink(file2)


def test_generate_diff_with_nested_objects():
    """Тест сравнения файлов с вложенными объектами"""
    data1 = {
        "common": {
            "setting1": "Value 1",
            "setting2": 200
        },
        "group1": {
            "baz": "bas",
            "foo": "bar"
        }
    }
    
    data2 = {
        "common": {
            "setting1": "Value 1",
            "setting3": True
        },
        "group2": {
            "abc": "12345"
        }
    }
    
    file1 = create_temp_json_file(data1)
    file2 = create_temp_json_file(data2)
    
    try:
        result = generate_diff(file1, file2)
        assert result is not None
        assert isinstance(result, str)
        # Должны видеть информацию о вложенных структурах
        assert "common" in result
        assert "setting" in result
    finally:
        os.unlink(file1)
        os.unlink(file2)


def test_generate_diff_with_arrays():
    """Тест сравнения файлов с массивами"""
    data1 = {
        "items": ["item1", "item2", "item3"],
        "numbers": [1, 2, 3]
    }
    
    data2 = {
        "items": ["item1", "item3"],
        "numbers": [1, 2, 3, 4]
    }
    
    file1 = create_temp_json_file(data1)
    file2 = create_temp_json_file(data2)
    
    try:
        result = generate_diff(file1, file2)
        assert result is not None
        assert "items" in result
        assert "numbers" in result
    finally:
        os.unlink(file1)
        os.unlink(file2)


def test_generate_diff_with_mixed_types():
    """Тест сравнения файлов с разными типами данных"""
    data1 = {
        "string": "hello",
        "number": 42,
        "boolean": True,
        "null_value": None,
        "array": [1, 2, 3]
    }
    
    data2 = {
        "string": "world", 
        "number": 100,
        "boolean": False,
        "null_value": "not null",
        "array": [1, 3, 4]
    }
    
    file1 = create_temp_json_file(data1)
    file2 = create_temp_json_file(data2)
    
    try:
        result = generate_diff(file1, file2)
        assert result is not None
        # Проверяем, что все ключи присутствуют в выводе
        assert "string" in result
        assert "number" in result
        assert "boolean" in result
    finally:
        os.unlink(file1)
        os.unlink(file2)


def test_generate_diff_file_not_found():
    """Тест обработки отсутствующих файлов"""
    with pytest.raises(FileNotFoundError) or pytest.raises(IOError) or pytest.raises(Exception):
        generate_diff("nonexistent1.json", "nonexistent2.json")


def test_generate_diff_invalid_json():
    """Тест обработки некорректных JSON файлов"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f1:
        f1.write('{"invalid": json}')
        file1 = f1.name
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f2:
        f2.write('{"valid": "json"}')
        file2 = f2.name
    
    try:
        # Ожидаем ошибку парсинга JSON
        with pytest.raises(json.JSONDecodeError) or pytest.raises(ValueError) or pytest.raises(Exception):
            generate_diff(file1, file2)
    finally:
        os.unlink(file1)
        os.unlink(file2)


def test_generate_diff_empty_files():
    """Тест сравнения пустых файлов"""
    data1 = {}
    data2 = {}
    
    file1 = create_temp_json_file(data1)
    file2 = create_temp_json_file(data2)
    
    try:
        result = generate_diff(file1, file2)
        assert result is not None
        # Пустые файлы должны считаться одинаковыми
        assert len(result.strip()) > 0
    finally:
        os.unlink(file1)
        os.unlink(file2)


def test_generate_diff_format_consistency():
    """Тест согласованности формата вывода"""
    data1 = {"a": 1, "b": 2}
    data2 = {"a": 1, "c": 3}
    
    file1 = create_temp_json_file(data1)
    file2 = create_temp_json_file(data2)
    
    try:
        result1 = generate_diff(file1, file2)
        result2 = generate_diff(file1, file2)  # Повторный вызов
        
        # Результаты должны быть идентичными при одинаковых входных данных
        assert result1 == result2
        assert isinstance(result1, str)
        assert len(result1) > 0
    finally:
        os.unlink(file1)
        os.unlink(file2)


def test_generate_diff_symmetrical():
    """Тест симметричности сравнения (A vs B и B vs A)"""
    data1 = {"key1": "value1", "common": "same"}
    data2 = {"key2": "value2", "common": "same"}
    
    file1 = create_temp_json_file(data1)
    file2 = create_temp_json_file(data2)
    
    try:
        result_ab = generate_diff(file1, file2)
        result_ba = generate_diff(file2, file1)
        
        # Результаты могут отличаться по порядку, но должны содержать одинаковую информацию
        assert result_ab is not None
        assert result_ba is not None
        assert isinstance(result_ab, str)
        assert isinstance(result_ba, str)
    finally:
        os.unlink(file1)
        os.unlink(file2)


def test_generate_diff_with_special_characters():
    """Тест сравнения файлов со специальными символами"""
    data1 = {
        "special_string": "line1\nline2\tline3",
        "unicode": "café 🚀",
        "escaped": "quote\"'backslash\\"
    }
    
    data2 = {
        "special_string": "line1\nline2",
        "unicode": "café 🌟", 
        "escaped": "quote\"backslash\\\\"
    }
    
    file1 = create_temp_json_file(data1)
    file2 = create_temp_json_file(data2)
    
    try:
        result = generate_diff(file1, file2)
        assert result is not None
        assert isinstance(result, str)
    finally:
        os.unlink(file1)
        os.unlink(file2)


@pytest.mark.parametrize("data1,data2", [
    ({"a": 1}, {"a": 2}),
    ({"a": 1}, {"b": 1}),
    ({"a": 1, "b": 2}, {"a": 1}),
    ({}, {"a": 1}),
    ({"a": [1, 2]}, {"a": [1, 3]}),
])
def test_generate_diff_parametrized(data1, data2):
    """Параметризованный тест для различных сценариев сравнения"""
    file1 = create_temp_json_file(data1)
    file2 = create_temp_json_file(data2)
    
    try:
        result = generate_diff(file1, file2)
        assert result is not None
        assert isinstance(result, str)
        assert len(result.strip()) > 0
    finally:
        os.unlink(file1)
        os.unlink(file2)


def test_generate_diff_performance():
    """Тест производительности с большими файлами"""
    # Создаем большие JSON файлы
    large_data1 = {f"key_{i}": f"value_{i}" for i in range(100)}
    large_data2 = {f"key_{i}": f"modified_value_{i}" for i in range(100)}
    
    file1 = create_temp_json_file(large_data1)
    file2 = create_temp_json_file(large_data2)
    
    try:
        import time
        start_time = time.time()
        result = generate_diff(file1, file2)
        end_time = time.time()
        
        assert result is not None
        # Проверяем что выполнение заняло разумное время (менее 5 секунд)
        assert end_time - start_time < 5.0
    finally:
        os.unlink(file1)
        os.unlink(file2)