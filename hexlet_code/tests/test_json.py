import json
import pytest_lazyfixture
import os

def read_json(filepath):
    with open (filepath, 'r') as f:
        return json.load(f)
    
def test_json_files_comprassion():
    file1 = read_json('file1.json')
    file2 = read_json('file2.json')

    assert 'host' in file1
    assert 'host' in file2
    assert 'timeout' in file1
    assert 'timeout' in file2
    
    # Проверяем конкретные значения
    assert file1['host'] == 'hexlet.io'
    assert file2['host'] == 'hexlet.io'
    assert file1['host'] == file2['host']  # Одинаковые значения
    
    # Проверяем разные значения timeout
    assert file1['timeout'] == 50
    assert file2['timeout'] == 20
    assert file1['timeout'] != file2['timeout']  # Разные значения
    
    # Проверяем уникальные ключи
    assert 'proxy' in file1
    assert 'verbose' in file2
    assert 'proxy' not in file2
    assert 'verbose' not in file1

def test_json_structure():
    """Тест структуры JSON файлов"""
    file1 = read_json('file1.json')
    file2 = read_json('file2.json')
    
    # Проверяем типы данных
    assert isinstance(file1, dict)
    assert isinstance(file2, dict)
    
    # Проверяем, что все значения имеют правильные типы
    assert isinstance(file1['host'], str)
    assert isinstance(file2['host'], str)
    assert isinstance(file1['timeout'], int)
    assert isinstance(file2['timeout'], int)
    assert isinstance(file1.get('follow'), bool)


def test_file_existence():
    """Тест существования файлов"""
    assert os.path.exists('file1.json')
    assert os.path.exists('file2.json')


def test_json_syntax():
    """Тест синтаксиса JSON файлов"""
    # Если файлы читаются без ошибок - синтаксис корректен
    file1 = read_json('file1.json')
    file2 = read_json('file2.json')
    
    # Дополнительные проверки валидности данных
    assert len(file1) > 0
    assert len(file2) > 0