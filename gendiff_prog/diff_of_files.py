# tests/diff_of_yaml_files.py
import os
from gendiff import generate_diff


def test_compare_yaml_files():
    """Тест сравнения двух YAML-файлов."""
    file1_path = os.path.join(os.path.dirname(__file__), '..', 'file1.yml')
    file2_path = os.path.join(os.path.dirname(__file__), '..', 'file2.yml')

    expected_output = """{
  - follow: false
    host: hexlet.io
  - proxy: 123.234.53.22
  - timeout: 50
  + timeout: 20
  + verbose: true
}"""

    result = generate_diff(file1_path, file2_path, "stylish")
    assert result.strip() == expected_output.strip()


def test_compare_json_and_yaml_files():
    """Тест сравнения JSON и YAML файлов."""
    json_path = os.path.join(os.path.dirname(__file__), '..', 'file1.json')
    yaml_path = os.path.join(os.path.dirname(__file__), '..', 'file2.yml')

    # Предположим, что file1.json и file2.yml содержат одинаковые данные,
    # но в разных форматах. Тогда diff должен быть пустым.
    expected_output = "{}"

    result = generate_diff(json_path, yaml_path, "stylish")
    assert result.strip() == expected_output.strip()