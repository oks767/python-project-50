import json
import pytest
import os
import sys

# Добавляем src в путь для импорта
sys.path.append('src')

from json_comparator import JSONComparator


def read_json(filepath):
    """Читает JSON файл и возвращает словарь"""
    with open(filepath, 'r') as f:
        return json.load(f)


def test_json_files_comparison():
    """Тест сравнения двух JSON файлов"""
    file1 = read_json('file1.json')
    file2 = read_json('file2.json')
    
    # Проверяем, что оба файла содержат определенные ключи
    assert 'host' in file1
    assert 'host' in file2
    assert 'timeout' in file1
    assert 'timeout' in file2
    
    # Проверяем конкретные значения
    assert file1['host'] == 'hexlet.io'
    assert file2['host'] == 'hexlet.io'
    assert file1['host'] == file2['host']
    
    # Проверяем разные значения timeout
    assert file1['timeout'] == 50
    assert file2['timeout'] == 20
    assert file1['timeout'] != file2['timeout']
    
    # Проверяем уникальные ключи
    assert 'proxy' in file1
    assert 'verbose' in file2
    assert 'proxy' not in file2
    assert 'verbose' not in file1


def test_json_structure():
    """Тест структуры JSON файлов"""
    file1 = read_json('file1.json')
    file2 = read_json('file2.json')
    
    assert isinstance(file1, dict)
    assert isinstance(file2, dict)
    assert isinstance(file1['host'], str)
    assert isinstance(file2['host'], str)
    assert isinstance(file1['timeout'], int)
    assert isinstance(file2['timeout'], int)


def test_file_existence():
    """Тест существования файлов"""
    assert os.path.exists('file1.json')
    assert os.path.exists('file2.json')


def test_comparator_class():
    """Тест класса JSONComparator"""
    comparator = JSONComparator()
    result = comparator.compare_files('file1.json', 'file2.json')
    
    assert 'common_keys' in result
    assert 'unique_to_first' in result
    assert 'unique_to_second' in result
    assert 'different_values' in result
    
    assert 'host' in result['common_keys']
    assert 'timeout' in result['common_keys']
    assert 'proxy' in result['unique_to_first']
    assert 'verbose' in result['unique_to_second']


def test_comparator_static_method():
    """Тест статического метода сравнения"""
    result = JSONComparator.compare_dicts(
        {'a': 1, 'b': 2},
        {'a': 1, 'c': 3}
    )
    
    assert result['common_keys'] == {'a'}
    assert result['unique_to_first'] == {'b'}
    assert result['unique_to_second'] == {'c'}
    assert 'different_values' in result