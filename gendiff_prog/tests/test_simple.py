import json
import os
import sys
import tempfile
import pytest
import yaml

# Добавляем src в путь для импорта
sys.path.insert(0, os.path.join(
    os.path.dirname(__file__), '..', 'scripts'
))

from gendiff import generate_diff


def create_temp_json_file(data):
    """Создает временный JSON файл с данными"""
    with tempfile.NamedTemporaryFile(
        mode='w', suffix='.json', delete=False
    ) as f:
        json.dump(data, f, indent=2)
        return f.name


def create_temp_yaml_file(data):
    """Создает временный YAML файл с данными"""
    with tempfile.NamedTemporaryFile(
        mode='w', suffix='.yaml', delete=False
    ) as f:
        yaml.dump(data, f, default_flow_style=False)
        return f.name


@pytest.mark.parametrize("create_file", [create_temp_json_file, create_temp_yaml_file])
def test_generate_diff_basic(create_file):
    """Базовый тест функции generate_diff (JSON и YAML)"""
    assert callable(generate_diff)


@pytest.mark.parametrize("create_file", [create_temp_json_file, create_temp_yaml_file])
def test_generate_diff_with_identical_files(create_file):
    """Тест сравнения идентичных файлов (JSON и YAML)"""
    data = {
        "host": "hexlet.io",
        "timeout": 50,
        "proxy": "123.234.53.22"
    }

    file1 = create_file(data)
    file2 = create_file(data)

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


@pytest.mark.parametrize("create_file", [create_temp_json_file, create_temp_yaml_file])
def test_generate_diff_with_different_values(create_file):
    """Тест сравнения файлов с разными значениями (JSON и YAML)"""
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

    file1 = create_file(data1)
    file2 = create_file(data2)

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


@pytest.mark.parametrize("create_file", [create_temp_json_file, create_temp_yaml_file])
def test_generate_diff_with_different_keys(create_file):
    """Тест сравнения файлов с разными ключами (JSON и YAML)"""
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

    file1 = create_file(data1)
    file2 = create_file(data2)

    try:
        result = generate_diff(file1, file2)
        assert result is not None
        # Должны видеть информацию о разных ключах
        assert "  - proxy: 123.234.53.22" in result
        assert "  + verbose: true" in result
        # Общие ключи без изменений
        assert "    host: hexlet.io" in result
        assert "    timeout: 50" in result
    finally:
        os.unlink(file1)
        os.unlink(file2)


def test_generate_diff_yaml_example():
    """Тест примера из задачи (YAML)"""
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

    file1 = create_temp_yaml_file(data1)
    file2 = create_temp_yaml_file(data2)

    try:
        result = generate_diff(file1, file2)
        assert result is not None

        # Проверяем ожидаемый вывод из задачи
        expected_lines = [
            "  - follow: false",
            "    host: hexlet.io",
            "  - proxy: 123.234.53.22",
            "  - timeout: 50",
            "  + timeout: 20",
            "  + verbose: true"
        ]

        for line in expected_lines:
            assert line in result

    finally:
        os.unlink(file1)
        os.unlink(file2)


def test_generate_diff_yaml_and_json():
    """Тест сравнения YAML и JSON файлов"""
    data1 = {
        "host": "hexlet.io",
        "timeout": 50,
        "proxy": "123.234.53.22"
    }

    data2 = {
        "host": "hexlet.io",
        "timeout": 50,
        "proxy": "123.234.53.22"
    }

    file1 = create_temp_yaml_file(data1)
    file2 = create_temp_json_file(data2)

    try:
        result = generate_diff(file1, file2)
        assert result == "{}"  # Файлы идентичны, diff пустой
    finally:
        os.unlink(file1)
        os.unlink(file2)


def test_generate_diff_invalid_yaml():
    """Тест обработки некорректных YAML файлов"""
    with tempfile.NamedTemporaryFile(
        mode='w', suffix='.yaml', delete=False
    ) as f1:
        f1.write('invalid: yaml')
        file1 = f1.name

    with tempfile.NamedTemporaryFile(
        mode='w', suffix='.yaml', delete=False
    ) as f2:
        yaml.dump({"valid": "yaml"}, f2)
        file2 = f2.name

    try:
        with pytest.raises(ValueError):
            generate_diff(file1, file2)
    finally:
        os.unlink(file1)
        os.unlink(file2)


def test_generate_diff_empty_files():
    """Тест сравнения пустых файлов (JSON и YAML)"""
    data1 = {}
    data2 = {}

    file1 = create_temp_yaml_file(data1)
    file2 = create_temp_json_file(data2)

    try:
        result = generate_diff(file1, file2)
        assert result == "{}"  # Файлы пустые, diff пустой
    finally:
        os.unlink(file1)
        os.unlink(file2)