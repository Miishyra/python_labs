import pytest
import json
import csv
from pathlib import Path
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.lib.json_csv import json_to_csv, csv_to_json


def test_json_to_csv_simple(tmp_path):
    """Простая конвертация JSON → CSV"""
    json_file = tmp_path / "test.json"
    csv_file = tmp_path / "test.csv"

    test_data = [{"name": "Alice", "age": 22}, {"name": "Bob", "age": 25}]

    json_file.write_text(json.dumps(test_data), encoding="utf-8")
    json_to_csv(str(json_file), str(csv_file))

    assert csv_file.exists()

    with csv_file.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

        assert len(rows) == 2
        assert {"name", "age"} == set(rows[0].keys())
        assert rows[0]["name"] == "Alice"


def test_csv_to_json_simple(tmp_path):
    """Простая конвертация CSV → JSON"""
    csv_file = tmp_path / "test.csv"
    json_file = tmp_path / "test.json"

    csv_content = "name,age,city\nAlice,22,London\nBob,25,Paris"
    csv_file.write_text(csv_content, encoding="utf-8")

    csv_to_json(str(csv_file), str(json_file))

    assert json_file.exists()

    with json_file.open(encoding="utf-8") as f:
        data = json.load(f)

        assert len(data) == 2
        assert set(data[0].keys()) == {"name", "age", "city"}
        assert data[0]["name"] == "Alice"


def test_json_to_csv_roundtrip(tmp_path):
    """Полный цикл конвертации"""
    original_data = [{"name": "Alice", "age": 22}, {"name": "Bob", "age": 25}]

    original_json = tmp_path / "original.json"
    converted_csv = tmp_path / "converted.csv"
    final_json = tmp_path / "final.json"

    original_json.write_text(json.dumps(original_data), encoding="utf-8")
    json_to_csv(str(original_json), str(converted_csv))
    csv_to_json(str(converted_csv), str(final_json))

    with final_json.open(encoding="utf-8") as f:
        final_data = json.load(f)

    assert final_data == original_data


def test_file_not_found():
    """Тестируем ошибку когда файл не существует"""
    with pytest.raises(FileNotFoundError):
        json_to_csv("nonexistent.json", "output.csv")
    with pytest.raises(FileNotFoundError):
        csv_to_json("nonexistent.csv", "output.json")


def test_invalid_cases(tmp_path):
    """Тестируем различные ошибочные случаи"""
    # Некорректный JSON
    json_file = tmp_path / "broken.json"
    json_file.write_text("{ invalid json }", encoding="utf-8")
    with pytest.raises(ValueError):
        json_to_csv(str(json_file), "output.csv")

    # Пустые файлы
    empty_file = tmp_path / "empty.json"
    empty_file.write_text("", encoding="utf-8")
    with pytest.raises(ValueError):
        json_to_csv(str(empty_file), "output.csv")

    # Неправильная структура JSON
    json_file.write_text(json.dumps(["not", "a", "dict"]), encoding="utf-8")
    with pytest.raises(ValueError):
        json_to_csv(str(json_file), "output.csv")

    # Пустой список в JSON
    json_file.write_text(json.dumps([]), encoding="utf-8")
    with pytest.raises(ValueError):
        json_to_csv(str(json_file), "output.csv")

    # CSV только с заголовками
    csv_file = tmp_path / "headers.csv"
    csv_file.write_text("name,age\n", encoding="utf-8")
    with pytest.raises(ValueError):
        csv_to_json(str(csv_file), "output.json")


def test_json_to_csv_different_fields(tmp_path):
    """Тестируем JSON с разными полями в записях"""
    json_file = tmp_path / "test.json"
    csv_file = tmp_path / "test.csv"

    test_data = [
        {"name": "Alice", "age": 25},
        {"name": "Bob", "age": 30, "city": "London"},
        {"name": "Charlie", "city": "Paris"},
    ]

    json_file.write_text(json.dumps(test_data), encoding="utf-8")
    json_to_csv(str(json_file), str(csv_file))

    assert csv_file.exists()

    with csv_file.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert len(rows) == 3
        assert {"name", "age", "city"} == set(rows[0].keys())


def test_csv_to_json_number_conversion(tmp_path):
    """Тестируем преобразование чисел из строк"""
    csv_file = tmp_path / "test.csv"
    json_file = tmp_path / "test.json"

    csv_content = "name,age,score\nAlice,25,95.5\nBob,30,87.0"
    csv_file.write_text(csv_content, encoding="utf-8")
    csv_to_json(str(csv_file), str(json_file))

    with json_file.open(encoding="utf-8") as f:
        data = json.load(f)
        assert data[0]["age"] == 25
        assert data[0]["score"] == 95.5


def test_wrong_extensions(tmp_path):
    """Тестируем неправильные расширения файлов"""
    wrong_file = tmp_path / "file.txt"
    wrong_file.write_text("some content", encoding="utf-8")

    with pytest.raises(ValueError):
        json_to_csv(str(wrong_file), "output.csv")
    with pytest.raises(ValueError):
        csv_to_json(str(wrong_file), "output.json")


def test_special_cases(tmp_path):
    """Тестируем специальные случаи"""
    # Одна запись в JSON
    json_file = tmp_path / "single.json"
    json_file.write_text(json.dumps([{"name": "Alice", "age": 25}]), encoding="utf-8")
    json_to_csv(str(json_file), tmp_path / "single.csv")

    # Юникод символы
    json_file = tmp_path / "unicode.json"
    test_data = [{"name": "Анна", "city": "Москва"}, {"name": "Böb", "city": "München"}]
    json_file.write_text(json.dumps(test_data, ensure_ascii=False), encoding="utf-8")
    json_to_csv(str(json_file), tmp_path / "unicode.csv")

    # Специальные символы в CSV
    csv_file = tmp_path / "special.csv"
    csv_content = 'name,comment\nAlice,"Text, with, commas"'
    csv_file.write_text(csv_content, encoding="utf-8")
    csv_to_json(str(csv_file), tmp_path / "special.json")
