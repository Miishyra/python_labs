import csv, json, os
import os
import json


def is_csv_file(file_path):
    return file_path.lower().endswith(".csv")


def is_json_file(file_path):
    return file_path.lower().endswith(".json")


def check_json_file(file_path: str) -> bool:
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл '{file_path}' не существует")

        if not is_json_file(file_path):
            raise ValueError(f"Файл '{file_path}' не является JSON файлом")

        if os.path.getsize(file_path) == 0:
            raise ValueError(f"Файл '{file_path}' пустой")

        with open(file_path, "r", encoding="utf-8") as file:
            json_data = json.load(file)

        if not isinstance(json_data, list):
            raise ValueError("JSON должен быть списком")

        if len(json_data) == 0:
            raise ValueError("Список JSON пустой")

        if not all(isinstance(item, dict) for item in json_data):
            raise ValueError("Не все элементы в списке являются словарями")

        return True

    except (json.JSONDecodeError, UnicodeDecodeError, ValueError) as e:
        if isinstance(e, UnicodeDecodeError):
            raise ValueError(f"Ошибка кодировки файла: {e}")
        else:
            raise ValueError(f"Ошибка при проверке JSON файла: {e}")
    except FileNotFoundError:
        raise
    except Exception as e:
        raise ValueError(f"Неожиданная ошибка: {e}")


def check_csv_file(file_path: str) -> bool:
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл '{file_path}' не существует")

        if not is_csv_file(file_path):
            raise ValueError(f"Файл '{file_path}' не является CSV файлом")

        if os.path.getsize(file_path) == 0:
            raise ValueError(f"Файл '{file_path}' пустой")

        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            header = next(reader, None)

            if len(header) == 0:
                raise ValueError("Заголовок CSV файла пустой")

            if any(not column.strip() for column in header):
                raise ValueError("Заголовок CSV содержит пустые колонки")

        return True

    except (UnicodeDecodeError, ValueError) as e:
        if isinstance(e, UnicodeDecodeError):
            raise ValueError(f"Ошибка кодировки файла: {e}")
        else:
            raise ValueError(f"Ошибка при проверке CSV файла: {e}")
    except FileNotFoundError:
        raise
    except Exception as e:
        raise ValueError(f"Неожиданная ошибка: {e}")


def json_to_csv(json_path: str, csv_path: str) -> None:
    check_json_file(json_path)

    with open(json_path, "r", encoding="utf-8") as json_file:
        json_data = json.load(json_file)

    with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=json_data[0].keys())
        writer.writeheader()
        writer.writerows(json_data)


def csv_to_json(csv_path: str, json_path: str) -> None:
    check_csv_file(csv_path)

    with open(csv_path, "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)

    with open(json_path, "w", encoding="utf-8") as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, indent=4)
