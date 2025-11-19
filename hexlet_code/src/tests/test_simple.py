import pytest
import sys
import os
import json
import tempfile

# Добавляем src в путь для импорта
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from gendiff import generate_diff


def create_temp_json_file(data):
    """Создает временный JSON файл с данными"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(data, f, indent=2)
        return f.name


def test_generate_diff_basic():
    """Базовый тест функции generate_diff"""
    assert callable(generate_diff)
    

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
        assert isinstance(result, str)
        # Проверяем что все ключи присутствуют без изменений
        assert "host: hexlet.io" in result
        assert "timeout: 50" in result
        assert "proxy: 123.234.53.22" in result
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
        assert "  - timeout: 50" in result
        assert "  + timeout: 20" in result
        # Общие ключи без изменений
        assert "    host: hexlet.io" in result
        assert "    proxy: 123.234.53.22" in result
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
        assert "  - proxy: 123.234.53.22" in result
        assert "  + verbose: true" in result  # true в нижнем регистре
        # Общие ключи без изменений
        assert "    host: hexlet.io" in result
        assert "    timeout: 50" in result
    finally:
        os.unlink(file1)
        os.unlink(file2)


def test_generate_diff_example_from_task():
    """Тест примера из задачи"""
    data1 = {
        "host": "hexlet.io",
        "timeout": 50,
        "proxy": "123.234.53.22",
        "follow": False
    }
    
    data2 = {
        "timeout": 20,
        "verbose": True,
        "host": "hexlet.io"
    }
    
    file1 = create_temp_json_file(data1)
    file2 = create_temp_json_file(data2)
    
    try:
        result = generate_diff(file1, file2)
        assert result is not None
    
        # Проверяем ожидаемый вывод из задачи (с правильным регистром)
        expected_lines = [
            "  - follow: false",      # false в нижнем регистре
            "    host: hexlet.io",
            "  - proxy: 123.234.53.22",
            "  - timeout: 50",
            "  + timeout: 20",
            "  + verbose: true"       # true в нижнем регистре
        ]
    
        for line in expected_lines:
            assert line in result
            
    finally:
        os.unlink(file1)
        os.unlink(file2)


def test_generate_diff_file_not_found():
    """Тест обработки отсутствующих файлов"""
    with pytest.raises(FileNotFoundError):
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
        with pytest.raises(ValueError):
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
        assert result == "{}"  # Пустые файлы должны возвращать просто {}
    finally:
        os.unlink(file1)
        os.unlink(file2)


def test_generate_diff_alphabetical_order():
    """Тест алфавитного порядка ключей"""
    data1 = {
        "zebra": 1,
        "apple": 2, 
        "banana": 3
    }
    
    data2 = {
        "apple": 2,
        "cherry": 4,
        "banana": 5
    }
    
    file1 = create_temp_json_file(data1)
    file2 = create_temp_json_file(data2)
    
    try:
        result = generate_diff(file1, file2)
        # Проверяем что ключи идут в алфавитном порядке
        lines = result.strip().split('\n')
        key_lines = [line for line in lines if ':' in line and line.strip()]
        
        keys_in_order = []
        for line in key_lines:
            key = line.split(':')[0].strip().lstrip('+- ')
            keys_in_order.append(key)
        
        # Проверяем алфавитный порядок
        assert keys_in_order == sorted(keys_in_order)
        
    finally:
        os.unlink(file1)
        os.unlink(file2)


def test_generate_diff_boolean_formatting():
    """Тест форматирования boolean значений"""
    data1 = {
        "enabled": True,
        "active": False,
        "none_value": None
    }
    
    data2 = {
        "enabled": False,
        "active": True,
        "none_value": "not null"
    }
    
    file1 = create_temp_json_file(data1)
    file2 = create_temp_json_file(data2)
    
    try:
        result = generate_diff(file1, file2)
        assert "enabled: true" in result
        assert "enabled: false" in result
        assert "active: false" in result
        assert "active: true" in result
        assert "none_value: null" in result
    finally:
        os.unlink(file1)
        os.unlink(file2)