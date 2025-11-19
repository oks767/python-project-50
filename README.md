### Hexlet tests and linter status:
[![Actions Status](https://github.com/oks767/python-project-50/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/oks767/python-project-50/actions)

# JSON Comparator

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=oks767_python-project-50&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=oks767_python-project-50)

## Описание
Утилита для сравнения JSON файлов с тестовым покрытием и анализом качества кода.

## Функциональность
- Сравнение структуры JSON файлов
- Выявление различий в значениях
- Генерация отчетов о различиях

## Запуск тестов
```bash
pytest tests/ -v --cov=src --cov-report=html

## SonarQube

