### Hexlet tests and linter status:
[![Actions Status](https://github.com/oks767/python-project-50/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/oks767/python-project-50/actions)

# JSON Comparator

![CI](https://github.com/your-username/your-repo/actions/workflows/ci.yml/badge.svg)
![SonarQube Quality Gate](https://sonarcloud.io/api/project_badges/measure?project=your-username_your-repo&metric=alert_status)
![SonarQube Coverage](https://sonarcloud.io/api/project_badges/measure?project=your-username_your-repo&metric=coverage)
![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=your-username_your-repo&metric=sqale_rating)
![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=your-username_your-repo&metric=reliability_rating)

## Описание
Утилита для сравнения JSON файлов с тестовым покрытием и анализом качества кода.

## Функциональность
- Сравнение структуры JSON файлов
- Выявление различий в значениях
- Генерация отчетов о различиях

## Запуск тестов
```bash
pytest tests/ -v --cov=src --cov-report=html