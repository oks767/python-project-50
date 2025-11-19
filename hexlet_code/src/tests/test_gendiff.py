import pytest
import sys
import os

# Добавляем src в путь для импорта
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.gendiff import generate_diff


def test_generate_diff_basic():
    """Базовый тест функции generate_diff"""
    # Здесь будут ваши тесты, когда реализуете функциональность
    assert True


def test_generate_diff_with_files():
    """Тест сравнения файлов"""
    # Временный тест, пока не реализована основная функциональность
    result = generate_diff(None, None)
    assert result is None


def test_json_comparison():
    """Тест сравнения JSON структур"""
    data1 = {"key": "value1"}
    data2 = {"key": "value2"}
    assert data1 != data2