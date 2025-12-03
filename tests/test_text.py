import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Теперь импортируем функции ПРАВИЛЬНО
from src.lib.text import normalize, tokenize, count_freq, top_n


# Тесты для normalize
@pytest.mark.parametrize(
    "source, expected",
    [
        ("ПрИвЕт\nМИр\t", "привет мир"),
        ("ёжик, Ёлка", "ежик, елка"),
        ("Hello\r\nWorld", "hello world"),
        ("  двойные   пробелы  ", "двойные пробелы"),
        ("", ""),  # пустая строка
        ("   ", ""),  # только пробелы
    ],
)
def test_normalize(source, expected):
    assert normalize(source) == expected


# Тесты для tokenize
@pytest.mark.parametrize(
    "text, expected",
    [
        ("привет мир", ["привет", "мир"]),
        ("hello world test", ["hello", "world", "test"]),
        ("", []),  # пустая строка
        ("   ", []),  # только пробелы
        ("знаки, препинания! тест.", ["знаки", "препинания", "тест"]),
    ],
)
def test_tokenize(text, expected):
    assert tokenize(text) == expected


# Тесты для count_freq
@pytest.mark.parametrize(
    "tokens, expected",
    [
        (["a", "b", "a", "c", "b", "a"], {"a": 3, "b": 2, "c": 1}),
        ([], {}),  # пустой список
        (["word"], {"word": 1}),  # один элемент
    ],
)
def test_count_freq(tokens, expected):
    assert count_freq(tokens) == expected


# Тесты для top_n - ВАЖНО: проверяем сортировку при равной частоте!
@pytest.mark.parametrize(
    "freq_dict, n, expected",
    [
        # Обычный случай
        ({"a": 3, "b": 2, "c": 1}, 3, [("a", 3), ("b", 2), ("c", 1)]),
        # Одинаковые частоты → сортировка по алфавиту
        (
            {"яблоко": 2, "апельсин": 2, "банан": 2},
            3,
            [("апельсин", 2), ("банан", 2), ("яблоко", 2)],
        ),
        # Пустой словарь
        ({}, 5, []),
        # Больше элементов чем n
        (
            {"a": 5, "b": 4, "c": 3, "d": 2, "e": 1, "f": 1},
            3,
            [("a", 5), ("b", 4), ("c", 3)],
        ),
        # n = 0
        ({"a": 1, "b": 2}, 0, []),
    ],
)
def test_top_n(freq_dict, n, expected):
    assert top_n(freq_dict, n) == expected
